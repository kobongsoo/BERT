import os
import random
import numpy as np
import torch
import torch.nn as nn
import logging
import warnings
from tqdm.notebook import tqdm
from torch import Tensor
from typing import Dict, List, Optional

#from sentence_transformers import SentenceTransformer
#from sentence_transformers import models

#------------------------------------------------------------------------------------------------------------------------------
# 임력된 문단을 2048길이만큼씩 나눔. 이때 마침표나 줄바꿈 기준으로 청크나눔
# -in : paragraph : 임력 문단 => str 형식으로 입력 (예: '독도 해역 헬기 추락사고가 발생한 지 열하루가 지났지만 실종자 추가 발견 소식은 들려오지 않고 있다')
# -in : chunk_size : 나눌 토큰 수 (예: 2048=2048길이로 문장나눔)
# -in : max_num_chunks : 최대 청크 수 ( 예: 10000 = 10000개 까지 청크 생성함)
# -out : 한 문단에 대한 청크분리한 문장리스트(1차원) 예: ['독도 해역 헬기 추락사고가 발생한 지 열',  # '가 발생한 지 열하루가 지났지만 실종자', ...,]
#
# 참고 : https://github.com/openai/chatgpt-retrieval-plugin/blob/main/services/chunks.py
#------------------------------------------------------------------------------------------------------------------------------
def get_text_chunks(paragraph: str,
                    chunk_size: Optional[int]=2048, 
                    max_num_chunks: Optional[int]=10000) -> List[str]:

    chunks = []
    num_chunks=0
    while num_chunks < max_num_chunks:
        chunk = paragraph[0:chunk_size] 

        # 길이가 5보다 작으면 chunk 작업 중지
        if len(chunk) < 5:
            break

        last_punctuation = max(
                chunk.rfind("."),
                chunk.rfind("?"),
                chunk.rfind("!"),
                chunk.rfind("\n"),
            )

        if last_punctuation != -1:
            chunk = chunk[: last_punctuation]

        chunks.append(chunk)
        num_chunks += 1
        paragraph = paragraph[last_punctuation:]
        
    return chunks
    
#------------------------------------------------------------------------------------------------------------------------------
# 임력된 문단을 256 토큰 단위로 나누는데, 이때 마침표나 줄바꿈 기준으로 청크를 나눔.
# -in : tokenizer : tokenizer
# -in : paragraph : 임력 문단 => str 형식으로 입력 (예: '독도 해역 헬기 추락사고가 발생한 지 열하루가 지났지만 실종자 추가 발견 소식은 들려오지 않고 있다')
# -in : chunk_token_size : 나눌 토큰 수 (예: 256=토큰 256개 단위로 문장을 나눔)
# -in : max_num_chunks : 최대 청크 수 ( 예: 10000 = 10000개 까지 청크 생성함)
# -in : min_chunk_length_to_embed : 해당 토큰 수보다 작은것은 청크가 아님(예: 5=5보다 작은 토큰은 청크로 추가 안함)
# -out : 한 문단에 대한 청크분리한 문장리스트(1차원) 예: ['독도 해역 헬기 추락사고가 발생한 지 열',  # '가 발생한 지 열하루가 지났지만 실종자', ...,]
#
# 참고 : https://github.com/openai/chatgpt-retrieval-plugin/blob/main/services/chunks.py
#------------------------------------------------------------------------------------------------------------------------------

# Constants
#CHUNK_SIZE = 200  # The target size of each text chunk in tokens
#MIN_CHUNK_SIZE_CHARS = 350  # The minimum size of each text chunk in characters
#MIN_CHUNK_LENGTH_TO_EMBED = 5  # Discard chunks shorter than this
#EMBEDDINGS_BATCH_SIZE = 128  # The number of embeddings to request at a time
#MAX_NUM_CHUNKS = 10000  # The maximum number of chunks to generate from a text


def get_text_chunks_token(tokenizer, 
                        paragraph: str, 
                        chunk_token_size: Optional[int]=256, 
                        max_num_chunks: Optional[int]=10000, 
                        min_chunk_length_to_embed: Optional[int]=5) -> List[str]:
    """
    Split a text into chunks of ~CHUNK_SIZE tokens, based on punctuation and newline boundaries.
    Args:
        text: The text to split into chunks.
        chunk_token_size: The target size of each chunk in tokens, or None to use the default CHUNK_SIZE.
    Returns:
        A list of text chunks, each of which is a string of ~CHUNK_SIZE tokens.
    """
    # Return an empty list if the text is empty or whitespace
    if not paragraph or paragraph.isspace():
        return []

    # Tokenize the text
    #tokens = tokenizer.encode(paragraph) #[CLS]=2, [SEP]=3 포함해 출력
    
    # [CLS]=2, [SEP]=3 빼고 tokeni_id만 출력
    temp = tokenizer.tokenize(paragraph)
    tokens = tokenizer.convert_tokens_to_ids(temp)

    #print(tokens)
        
    # Initialize an empty list of chunks
    chunks = []

    # Use the provided chunk token size or the default one
    #chunk_size = chunk_token_size or CHUNK_SIZE
    chunk_size = chunk_token_size
    
    # Initialize a counter for the number of chunks
    num_chunks = 0

    # Loop until all tokens are consumed
    while tokens and num_chunks < max_num_chunks:
        # Take the first chunk_size tokens as a chunk
        chunk = tokens[0:chunk_size] # 맨앞에 [CLS] 제거 하기 위해 1부터 시작
        
        # 길이가 1보다 작으면 chunk 작업 중지
        if len(chunk) < 1:
            break
        
        #print(chunk)
        #print()
        # Decode the chunk into text
        chunk_text = tokenizer.decode(chunk)

        #print('chunk_text1-------------')
        #print(chunk_text)
        #print()
                      
        # Skip the chunk if it is empty or whitespace
        if not chunk_text or chunk_text.isspace():
            # Remove the tokens corresponding to the chunk text from the remaining tokens
            tokens = tokens[len(chunk) :]
            # Continue to the next iteration of the loop
            continue

        # Find the last period or punctuation mark in the chunk
        last_punctuation = max(
            chunk_text.rfind("."),
            chunk_text.rfind("?"),
            chunk_text.rfind("!"),
            chunk_text.rfind("\n"),
        )
        
        #print(f'last_punctuation: {last_punctuation}')

        # If there is a punctuation mark, and the last punctuation index is before MIN_CHUNK_SIZE_CHARS
        #if last_punctuation != -1 and last_punctuation > MIN_CHUNK_SIZE_CHARS:
        if last_punctuation != -1:
            # Truncate the chunk text at the punctuation mark
            chunk_text = chunk_text[: last_punctuation]

        #print('chunk_text2-------------')
        #print(chunk_text)
        #print()
              
        # Remove any newline characters and strip any leading or trailing whitespace
        chunk_text_to_append = chunk_text.replace("\n", " ").strip()

        if len(chunk_text_to_append) > min_chunk_length_to_embed:
            # Append the chunk text to the list of chunks
            chunks.append(chunk_text_to_append)

        # Remove the tokens corresponding to the chunk text from the remaining tokens
        tokens = tokens[len(tokenizer.encode(chunk_text)):]

        # Increment the number of chunks
        num_chunks += 1

    # Handle the remaining tokens
    if tokens:
        remaining_text = tokenizer.decode(tokens).replace("\n", " ").strip()
        if len(remaining_text) > min_chunk_length_to_embed:
            chunks.append(remaining_text)

    return chunks

#------------------------------------------------------------------------------------------------------------------------------
# 임력된 문단을 510 토큰 단위로 나누고, 100단위로 슬라이딩 윈도우 하면서 나눈 문단을 1차원 배열로 출력
# -in : tokenizer : tokenizer
# -in : paragraph : 임력 문단 => str 형식으로 입력 (예: '독도 해역 헬기 추락사고가 발생한 지 열하루가 지났지만 실종자 추가 발견 소식은 들려오지 않고 있다')
# -in : window_size : 나눌 토큰 수 (예: 10=토큰 10개 단위로 문장을 나눔)
# -in : sliding_size : 슬라이딩 토큰 수 ( 예: 5 이면 5씩 이전문장 포함해서 문장 나눔 : 반드시 windows_size보다는 작아야 함)
# -out : 한 문단에 대한 슬라이딩 처리한 문장리스트(1차원) 예: ['독도 해역 헬기 추락사고가 발생한 지 열',  # '가 발생한 지 열하루가 지났지만 실종자', ...,]
#------------------------------------------------------------------------------------------------------------------------------
def sliding_window_tokenizer(tokenizer, paragraph:str, window_size:int=510, sliding_size:int=100) -> List[str]:

    step_size = window_size - sliding_size    

    assert paragraph != None, f'error!! paragraphs is None' 
    assert window_size > sliding_size, f'error!! window_size({window_size}) < sliding_size({sliding_size})' 
    
    tokens = tokenizer.tokenize(paragraph)
    
    # text가 '독도 해역 헬기 추락사고가 발생한 지 열하루가 지났지만 실종자 추가 발견 소식은 들려오지 않고 있다' 일때
    # 토큰별로 분리하고 아래처럼 2차원 토큰 배열로 출력됨
    # [['독도', '해역', '헬기', '추락', '##사고', '##가', '발생', '##한', '지', '열'], 
    # ['##가', '발생', '##한', '지', '열', '##하루', '##가', '지났', '##지만', '실종자'], 
    # ['##하루', '##가', '지났', '##지만', '실종자', '추가', '발견', '소식', '##은', '들려오'], 
    # ['추가', '발견', '소식', '##은', '들려오', '##지', '않', '##고', '있', '##다'], 
    # ['##지', '않', '##고', '있', '##다']]

    newtokens = []
    for i in range(0, len(tokens), step_size):
        if i + window_size <= len(tokens):
            newtokens.append(tokens[i:i+window_size])
        else:
            newtokens.append(tokens[i:])

    #print(newtokens)

    # 위 2차원 배열 토큰들을 합쳐서 문장으로 만듬.
    # 이때 각 토큰(token)에 대해, ##로 시작하는 경우 ##를 제거하고 new_lst에 추가
    # 첫 번째 토큰인 경우, token을 그대로 new_lst에 추가
    # 첫 번째 토큰이 아닌 경우 , new_lst의 마지막 요소와 token 사이에 띄어쓰기(" ")를 추가하여 new_lst에 추가

    # ['독도 해역 헬기 추락사고가 발생한 지 열', 
    # '가 발생한 지 열하루가 지났지만 실종자', 
    # '하루가 지났지만 실종자 추가 발견 소식은 들려오', 
    # '추가 발견 소식은 들려오지 않고 있다', 
    # '지 않고 있다']

    result = []
    for lst in newtokens:
        new_lst = []
        for token in lst:
            if token.startswith("##"): # 각 토큰(token)에 대해, ##로 시작하는 경우 ##를 제거하고 new_lst에 추가
                new_lst.append(token[2:])
            else:
                if len(new_lst) == 0:  # new_lst가 비어 있는 경우(첫 번째 토큰인 경우), token을 그대로 new_lst에 추가
                    new_lst.append(token)
                else:
                    new_lst.append(" " + token) # 첫 번째 토큰이 아닌 경우 , new_lst의 마지막 요소와 token 사이에 띄어쓰기(" ")를 추가하여 new_lst에 추가
        result.append("".join(new_lst))

    return result


# main    
if __name__ == '__main__':
    main()

    