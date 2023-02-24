############################################################################################
## 아래 패키지들을 설치해야 함
'''
pip install datasets
pip install optimum
pip install optimum[onnxruntime]
pip install optimum[onnxruntime-gpu]  #gpu 사용인 경우
pip install transformers[onnx]
'''    
############################################################################################
import torch
import torch.nn as nn
import numpy as np
from transformers import AutoTokenizer
from optimum.onnxruntime import ORTModelForFeatureExtraction

#----------------------------------------------------------------------------
# onnx 모델 불러오기
# -in : model.onnx, vocab.txt 가 저장된 폴더 경로.
# -out:tokenizer, onnx 모델 인스턴스 
#----------------------------------------------------------------------------
def onnx_model(model_path:str):
    assert model_path is not None, f'model_path is None!'
    
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = ORTModelForFeatureExtraction.from_pretrained(model_path)
    return tokenizer, model
                
#------------------------------------------------------------------------------------------------------------------------------
# 입력 text(리스트)에 대한 embed vector 생성 후 배열로 리턴함
# - in : model=모델 인스턴스, contexts=1차원 text 리스트 예: ['오늘 날씨가 너무 좋다']
# - in : return_tensor=True 이면 tensor값으로 임베딩벡터생성됨.
# - in : token_embeddings=출력을 어떻게 할지 False=>'sentence embeddings'->768 문장 임베딩 값, True=> token_embeddings=>토큰별 임베딩값
# - in : normalize : True=임베딩 정규화 화면 출력벡터이 길이가 1이 된다.
# - out : token_embeddings=True 일때=>토큰별 embedding 으로 출력함=> list[tensor(250,768), tensor(243,768), tensor(111,768),..] tensor 리스트 타입으로 리턴됨.
#          token_embeddings=False 일때 =>1개의 embedding으로 출력함=> array[768, 768, 768,...] float32 array 타입으로 리턴함.
#------------------------------------------------------------------------------------------------------------------------------
def onnx_embed_text(model, tokenizer, paragraphs:list, max_length:int=128, token_embeddings=True, debug=False):
    
    inputs = tokenizer(paragraphs, max_length=max_length, truncation=True, padding="max_length", return_tensors="pt")
        
    outputs = model(**inputs)
    output = outputs.last_hidden_state

    if token_embeddings == True:  # contexts를 토큰별 embedding 으로 출력함.        
        # 한 문장에 대한 attnention_mask에 [1,1,1,1,0,0,0,... ]출력되면 이때 1 카운터 계수만 리스트로 만듬
        # => onnx 모델 outputs은 입력된 padding(0) 값도 출력되므로 128개 배열이 출력됨. 따라서 실제 token들에 계수를 저장해둠.
        attention_mask_list = [list(row).count(1) for row in inputs.attention_mask]
        
        # 한 문단에 대한 문장들에 대해 [tensor(250,768), tensor(243,768), tensor(111,768),..] tensor 리스트 타입으로 벡터 만듬.
        token_embeds = [output[idx][0:attention] for idx, attention in enumerate(attention_mask_list)]
    else:  
        # 평균 구해서 배열로 출력 =>[(768,),(768,),(768,),....]
        tmp = [torch.mean(embeds[1], dim=0).numpy() for embeds in enumerate(output)]
        token_embeds = np.array([embedding for embedding in tmp]) #float32 로 embeddings 타입 변경 =>numpy 타입으로 리턴됨
    
    if debug == True:
        print(f'*[onnx_embed_text] outputs: {outputs}')
        print(f'*[onnx_embed_text] output.shape: {output.shape}')
        print(f'*[onnx_embed_text] token_embeds.shape: {token_embeds.shape}') 
        print(f'*[onnx_embed_text] token_embeds[0]: {token_embeds[0]}')
        
    return token_embeds
     
        
# main    
if __name__ == '__main__':
    main()