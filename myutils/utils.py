import os
import random
import numpy as np
import torch
import logging

from torch.utils.data.dataset import Dataset
from torch import Tensor, device
from transformers.tokenization_utils import PreTrainedTokenizer
from transformers import set_seed
from typing import Dict, List, Optional
import json
import pickle
import time
import warnings
from filelock import FileLock
#from transformers.utils import logging
from tqdm.notebook import tqdm
#import gluonnlp as nlp                  # GluonNLP는 버트를 간단하게 로딩하는 인터페이스를 제공하는 API 임

from transformers import BertTokenizer
from typing import Dict, List

#logger = logging.get_logger(__name__)

#------------------------------------------------------------------------------------------------------------------------------
# dataframe 랜덤하게 샘플링하는 함수
# =>IN: df=dataframe, num=샘플링계수, seed=seed 값
#------------------------------------------------------------------------------------------------------------------------------
def df_sampling(df, num:int=3, seed: int=111):
    df_sample = df.sample(num, random_state=seed)
    df_sample = df_sample.reset_index(drop=True)  # index는 0부터 
    
    return df_sample
    
#------------------------------------------------------------------------------------------------------------------------------
# 2차원배열 입력받아서 각 배렬의 최대값 혹은 최소값 합을 리턴하는 함수
# 예: [[2,3,4],[5,3,1]] 입력 => 4+5=9 리턴
# => IN : array=2차원 배열, bmax=True이면 최대값 합 리턴, False=이면 최소값 합 리턴
#------------------------------------------------------------------------------------------------------------------------------
def sum_of_array_2d(array, bmin: bool=False):
    if bmin == False:
        values = np.amax(array, axis=1) # 2차원 배열 => np.array([[2,3,4],[4,3,2]])에서 최대값을 구함.
    else:
        values = np.amin(array, axis=1) # 2차원 배열 => np.array([[2,3,4],[4,3,2]])에서 최소값을 구함.
    
    sum_of_values = np.sum(values)
    
    return sum_of_values

#------------------------------------------------------------------------------------------------------------------------------
# 1차원리스트를 입력받아서 각 배열에서 max 혹은 min 값을 갖는 indext번지를 k개 출력하는 함수
# 예: listdata=[2,3,5,4,2,3,4,1], k= 3입력 => [2,3,6] 리턴
# => IN : listdata=1차원 리스트, k=출력계수, bmax=True이면 최대값 목록 리턴, False=이면 최소값 목록 리턴
#------------------------------------------------------------------------------------------------------------------------------
def index_of_list(listdata, k: int=1, bmin: bool=False):

    arr = np.array(listdata) # list를 배열로 변환

    if bmin == False:
        indexs = np.argsort(-arr)[:k]# 배열에서 max 값을 갖는 index를  k개 출력함
    else:
        indexs = np.argsort(arr)[:k] # 배열에서 min 값을 갖는 index를  k개 출력함

    return indexs

#------------------------------------------------------------------------------------------------------------------------------
# 리스트 중복 제거 (순서유지 안함)
#------------------------------------------------------------------------------------------------------------------------------
def remove_duplicate_lists_not_order(lst):
    return list(set(lst))

#------------------------------------------------------------------------------------------------------------------------------
# 리스트 중복 제거 (순서유지함)
#------------------------------------------------------------------------------------------------------------------------------
def remove_duplicate_lists_order(lst):
    return list(dict.fromkeys(lst))

#########################################################################################
# 폴더(서브폴더포함)에 있는 파일들의 풀경로를 얻어오는 함수
# 출처 : https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
#########################################################################################
def getListOfFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isdir(fullPath):
            allFiles = allFiles + getListOfFiles(fullPath)
        else:
            allFiles.append(fullPath)
                
    return allFiles

#########################################################################################
# wordpiece vocab에 special 토큰 추가
# : vocab.txt, tokenizer_config.json, special_tokens_map.json, added_tokens.json 등이 생성됨
# - input_wpfpath : 입력 wordpiece vocab 파일 경로
# - output_folder : special 토큰 추가된 파일 생성 폴더 경로 
#########################################################################################
def AddWPVocabSpecialToken(input_wpfpath:str, output_folder:str):
    
     # 입력 파일경로가 없으면 에러
    assert os.path.isfile(input_wpfpath), f"Input file path {input_fpath} not found" 
    
    # 정의할 speical toeken : **필요에 따라 수정 가능
    special_tokens=['[BOS]', '[EOS]', '[UNK0]', '[UNK1]', '[UNK2]', '[UNK3]', '[UNK4]', '[UNK5]', '[UNK6]', '[UNK7]', '[UNK8]', '[UNK9]',
                '[unused0]', '[unused1]', '[unused2]', '[unused3]', '[unused4]', '[unused5]', '[unused6]', '[unused7]', '[unused8]', '[unused9]',]
    
    tokenizer = BertTokenizer(vocab_file=input_wpfpath, 
                          strip_accents=False, # 한국어 일때는 false(true이면, 문서 => ㅁ ㅜ ㄴ ㅅ ㅓ 식으로 형태소 분할됨)
                          do_lower_case=False) # 대.소문자 구분 안하므로, false
    
    # special token 추가
    special_tokens_dict = {'additional_special_tokens': special_tokens}
    tokenizer.add_special_tokens(special_tokens_dict)
    
    # special token 추가한 special vocab을 저장함
    # - 해당 폴더에 vocab.txt, tokenizer_config.json, special_tokens_map.json, added_tokens.json 등이 생성됨
    tokenizer.save_pretrained(output_folder)
    
    print("speicaltoken: '{}' create!!".format(output_folder))

#########################################################################################
# sentencepiece vocab(kobert) 을 wordpiecevocab으로 변환 
# : kobert 와 같은 sententcepiece vocab 모델을 
# huggingface API 사용을 위한 wordpiece vocab 파일로 변환 함
#
# - input_fpath : 입력 sententcepiece 모델 파일 경로
# - output_folder : 출력 wordpiece vocat 파일 경로
# - first_special_token : 처음 special_token 이 있다면, 해당 리스트 순서대로 먼저 추가함.
#
#    * Kobert specialtoken은 원래 [UNK], [PAD], [CLS], [SEP], [MASK] 순서인데,
#      아래처럼 [UNK], [CLS], [SEP], [MASK], [PAD] 순서대로 [PAD]가 맨뒤에 출력됨
#      따라서 first_special_token 지정해 주는 경우에는 먼저 special_token을 파일에 추가함
#              k:[UNK], idx:0
#              k:[CLS], idx:2
#              k:[SEP], idx:3
#              k:[MASK], idx:4
#              k:[PAD], idx:1
#########################################################################################
'''
def SPVocabToWPVocab(input_fpath:str, output_fpath:str, first_special_token:list):
    
    # 입력 파일경로가 없으면 에러
    assert os.path.isfile(input_fpath), f"Input file path {input_fpath} not found" 
    
    # 출력 디렉토리가 없으면 디렉토리 생성
    directory, filename = os.path.split(output_fpath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    
    vocab = nlp.vocab.BERTVocab.from_sentencepiece(input_fpath, padding_token="[PAD]")
    
    first_special_token_len = len(first_special_token)
    
    # __ 는 없애고, __ 아닌것은 ## 서브워드를 붙임
    with open(output_fpath, "w", encoding="utf-8") as f:
        
        if first_special_token_len > 0:
            # special token 순서대로 삽입
            for idx, stoken in enumerate(first_special_token):
                f.writelines(stoken + "\n")
                print('sp:{}, idx:{}'.format(idx,stoken))
                
        for k, v in vocab.token_to_idx.items():
            print('k:{}, idx:{}'.format(k,v))
            if k[0] == '▁':
                k = k.replace('▁', '')
                f.writelines(k + "\n")
            elif k in ["[UNK]", "[PAD]", "[CLS]", "[SEP]", "[MASK]"]:
                if first_special_token_len == 0:
                    f.f.writelines(stoken + "\n")  
                pass
            else:
                k = '##' + k
                f.writelines(k + "\n")
        
    print("spvocap:'{}' -> wpvocab: '{}' change success!!".format(input_fpath, output_fpath))
'''
#########################################################################################    
# mlogging 설정
#########################################################################################
def mlogging(
    loggername: str = 'mlogger',  #logger 구분자
    logfilename: str = None       #log 저장 파일명
):
    import time
    
    # logfilepath가 None이면 현재날짜로 로그파일 생성
    if logfilename is None:
        logfilepath = time.strftime('mlog_%Y-%m-%d.log', time.gmtime())
    else:   
        logfilepath = logfilename + time.strftime('_%Y-%m-%d.log', time.gmtime()) 
        
    print('logfilepath:{}'.format(logfilepath))

    # 로그 생성
    logger = logging.getLogger(loggername)

    # 로그의 출력 기준 설정(INFO, ERROR, WARNING 출력함)
    logger.setLevel(logging.INFO)

    # log 출력 형식
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # log 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # log를 파일에 출력
    file_handler = logging.FileHandler(logfilepath)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

#MYLOGGER = mlogging()

#def mylogger(message: str):
#    MYLOGGER.info(message)
#    pass;
    

#########################################################################################
# cos simulate(유사도) 측정 함수
#########################################################################################
def pytorch_cos_sim(a: Tensor, b: Tensor):
    """
    Computes the cosine similarity cos_sim(a[i], b[j]) for all i and j.
    This function can be used as a faster replacement for 1-scipy.spatial.distance.cdist(a,b)
    :return: Matrix with res[i][j]  = cos_sim(a[i], b[j])
    """
    if not isinstance(a, torch.Tensor):
        a = torch.tensor(a)

    if not isinstance(b, torch.Tensor):
        b = torch.tensor(b)

    if len(a.shape) == 1:
        a = a.unsqueeze(0)

    if len(b.shape) == 1:
        b = b.unsqueeze(0)

    a_norm = a / a.norm(dim=1)[:, None]
    b_norm = b / b.norm(dim=1)[:, None]
    return torch.mm(a_norm, b_norm.transpose(0, 1))

#########################################################################################
# GPU 정보
#########################################################################################
def GPU_info():
    biscuda = torch.cuda.is_available()
    print(biscuda)
    
    device = torch.device('cuda:0' if biscuda else 'cpu')
    print('device:',device)
    
    if biscuda:
        print('cuda index:', torch.cuda.current_device())
        print('gpu 개수:', torch.cuda.device_count())
        print('graphic name:', torch.cuda.get_device_name())
        #cuda = torch.device('cuda')
       
    return device

#########################################################################################
# seed 설정
#########################################################################################
def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    set_seed(seed)

#########################################################################################
# NSP(next sentence predict) 문장 만들기    
#########################################################################################
class TextDatasetForNextSentencePrediction(Dataset):
    """
    This will be superseded by a framework-agnostic approach soon.
    """

    def __init__(
        self,
        tokenizer: PreTrainedTokenizer,
        file_path: str,
        block_size: int,
        overwrite_cache=False,
        short_seq_probability=0.1,
        nsp_probability=0.5,
    ):
               
        # 여기 부분은 학습 데이터를 caching하는 부분입니다 :-)
        assert os.path.isfile(file_path), f"Input file path {file_path} not found"

         
        self.block_size = block_size - tokenizer.num_special_tokens_to_add(pair=True)
        self.short_seq_probability = short_seq_probability
        self.nsp_probability = nsp_probability
    
        directory, filename = os.path.split(file_path)
        cached_features_file = os.path.join(
            directory,
            "cached_nsp_{}_{}_{}".format(
                tokenizer.__class__.__name__,
                str(block_size),
                filename,
            ),
        )

        # [bong] 경로 호출
        print('init=>File: {}, block_size:{}, cached_features_file: {}'.format(file_path, self.block_size, cached_features_file))
        
        self.tokenizer = tokenizer

        lock_path = cached_features_file + ".lock"

        # Input file format:
        # (1) One sentence per line. These should ideally be actual sentences, not
        # entire paragraphs or arbitrary spans of text. (Because we use the
        # sentence boundaries for the "next sentence prediction" task).
        # (2) Blank lines between documents. Document boundaries are needed so
        # that the "next sentence prediction" task doesn't span between documents.
        #
        # Example:
        # I am very happy.
        # Here is the second sentence.
        #
        # A new document.

        with FileLock(lock_path):
            if os.path.exists(cached_features_file) and not overwrite_cache:
                start = time.time()
                
                print("Loading start cashed file %s [starttime: %.3f s]=>wait 30 min...", cached_features_file, start)
                
                with open(cached_features_file, "rb") as handle:
                    self.examples = pickle.load(handle)
                print(f"Loading features from cached file {cached_features_file} [took %.3f s]", time.time() - start)
            else: # 캐시가 없는 경우
                print(f"Creating features from dataset file at {directory}")
                
                # [bong] total_line 수를 구함
                with open(file_path, encoding="utf-8") as f:
                    total_line = len(f.readlines())
                    # [bong] 총 라인수 출력
                    print('* total_line: {}'.format(total_line))
                    
                # 여기서부터 본격적으로 dataset을 만듭니다.
                self.documents = [[]] # document 단위로 학습이 이뤄짐
                with open(file_path, encoding="utf-8") as f:
                    #scount = 0
                    #while True: # 일단 문장을 읽고
                    # [bong] tqdm 사용을 위해 while문을 for문으로 변경
                    for idx in tqdm(range(total_line)): 
                        
                        #if scount % 1000000 == 0:
                        #    print('*readline=>count: {}'.format(scount))
                            
                        line = f.readline()
                        if not line:
                             # [bong] 총 라인수 읽기 끝
                            print('*readline=>count: {} End!'.format(scount))
                            break
                        line = line.strip() # 필수!!!!
                        #scount += 1
                        # 이중 띄어쓰기가 발견된다면, 나왔던 문장들을 모아 하나의 문서로 묶어버립니다.
                        # 즉, 문단 단위로 데이터를 저장합니다.
                        if not line and len(self.documents[-1]) != 0:
                            self.documents.append([])
                        tokens = tokenizer.tokenize(line)
                        tokens = tokenizer.convert_tokens_to_ids(tokens)
                        if tokens:
                            self.documents[-1].append(tokens)
                # 이제 코퍼스 전체를 읽고, 문서 데이터를 생성했습니다! :-)
                print(f"Creating examples from {len(self.documents)} documents.")
                self.examples = []
                # 본격적으로 학습을 위한 데이터로 변형시켜볼까요?
                for doc_index, document in enumerate(tqdm(self.documents)):
                    self.create_examples_from_document(document, doc_index) # 함수로 가봅시다.
                    #if doc_index % 1000000 == 0:
                    #    print('*create_doc: doc_index:{}'.format(doc_index))

                #print('*create_doc End')
                
                # pickle 를 이용하여, python 바이너리 형태로 캐쉬 파일 저장함(한 20분 이상 걸림)
                start = time.time()
                print("Save start cashed file %s [starttime: %.3f s]=>wait 30 min...", cached_features_file, start)
                
                with open(cached_features_file, "wb") as handle:
                    pickle.dump(self.examples, handle, protocol=pickle.HIGHEST_PROTOCOL)
                print("Saving features into cached file %s [took %.3f s]", cached_features_file, time.time() - start)

    def create_examples_from_document(self, document: List[List[int]], doc_index: int):
        """Creates examples for a single document."""
        # 문장의 앞, 뒤에 [CLS], [SEP] token이 부착되기 때문에, 내가 지정한 size에서 2 만큼 빼줍니다.
        # 예를 들어 128 token 만큼만 학습 가능한 model을 선언했다면, 학습 데이터로부터는 최대 126 token만 가져오게 됩니다.
        max_num_tokens = self.block_size - self.tokenizer.num_special_tokens_to_add(pair=True)

        # We *usually* want to fill up the entire sequence since we are padding
        # to `block_size` anyways, so short sequences are generally wasted
        # computation. However, we *sometimes*
        # (i.e., short_seq_prob == 0.1 == 10% of the time) want to use shorter
        # sequences to minimize the mismatch between pretraining and fine-tuning.
        # The `target_seq_length` is just a rough target however, whereas
        # `block_size` is a hard limit.

        # 여기가 재밌는 부분인데요!
        # 위에서 설명했듯이, 학습 데이터는 126 token(128-2)을 채워서 만들어지는게 목적입니다.
        # 하지만 나중에 BERT를 사용할 때, 126 token 이내의 짧은 문장을 테스트하는 경우도 분명 많을 것입니다 :-)
        # 그래서 short_seq_probability 만큼의 데이터에서는 2-126 사이의 random 값으로 학습 데이터를 만들게 됩니다.
        target_seq_length = max_num_tokens
        if random.random() < self.short_seq_probability:
            target_seq_length = random.randint(2, max_num_tokens)

        current_chunk = []  # a buffer stored current working segments
        current_length = 0
        i = 0

        # 데이터 구축의 단위는 document 입니다
        # 이 때, 무조건 문장_1[SEP]문장_2 이렇게 만들어지는 것이 아니라,
        # 126 token을 꽉 채울 수 있게 문장_1+문장_2[SEP]문장_3+문장_4 형태로 만들어질 수 있습니다.
        while i < len(document):
            segment = document[i]
            current_chunk.append(segment)
            current_length += len(segment)
            if i == len(document) - 1 or current_length >= target_seq_length:
                if current_chunk:
                    # `a_end` is how many segments from `current_chunk` go into the `A`
                    # (first) sentence.
                    a_end = 1
                    # 여기서 문장_1+문장_2 가 이루어졌을 때, 길이를 random하게 짤라버립니다 :-)
                    if len(current_chunk) >= 2:
                        a_end = random.randint(1, len(current_chunk) - 1)
                    tokens_a = []
                    for j in range(a_end):
                        tokens_a.extend(current_chunk[j])
                    # 이제 [SEP] 뒷 부분인 segmentB를 살펴볼까요?
                    tokens_b = []
                    # 50%의 확률로 랜덤하게 다른 문장을 선택하거나, 다음 문장을 학습데이터로 만듭니다.
                    if len(current_chunk) == 1 or random.random() < self.nsp_probability:
                        is_random_next = True
                        target_b_length = target_seq_length - len(tokens_a)

                        # This should rarely go for more than one iteration for large
                        # corpora. However, just to be careful, we try to make sure that
                        # the random document is not the same as the document
                        # we're processing.
                        for _ in range(10):
                            random_document_index = random.randint(0, len(self.documents) - 1)
                            if random_document_index != doc_index:
                                break
                        # 여기서 랜덤하게 선택합니다 :-)
                        random_document = self.documents[random_document_index]
                        random_start = random.randint(0, len(random_document) - 1)
                        for j in range(random_start, len(random_document)):
                            tokens_b.extend(random_document[j])
                            if len(tokens_b) >= target_b_length:
                                break
                        # We didn't actually use these segments so we "put them back" so
                        # they don't go to waste.
                        num_unused_segments = len(current_chunk) - a_end
                        i -= num_unused_segments
                    # Actual next
                    else:
                        is_random_next = False
                        for j in range(a_end, len(current_chunk)):
                            tokens_b.extend(current_chunk[j])

                    # 이제 126 token을 넘는다면 truncation을 해야합니다.
                    # 이 때, 126 token 이내로 들어온다면 행위를 멈추고,
                    # 만약 126 token을 넘는다면, segmentA와 segmentB에서 랜덤하게 하나씩 제거합니다.
                    def truncate_seq_pair(tokens_a, tokens_b, max_num_tokens):
                        """Truncates a pair of sequences to a maximum sequence length."""
                        while True:
                            total_length = len(tokens_a) + len(tokens_b)
                            if total_length <= max_num_tokens:
                                break
                            trunc_tokens = tokens_a if len(tokens_a) > len(tokens_b) else tokens_b
                            assert len(trunc_tokens) >= 1
                            # We want to sometimes truncate from the front and sometimes from the
                            # back to add more randomness and avoid biases.
                            if random.random() < 0.5:
                                del trunc_tokens[0]
                            else:
                                trunc_tokens.pop()

                    truncate_seq_pair(tokens_a, tokens_b, max_num_tokens)

                    assert len(tokens_a) >= 1
                    assert len(tokens_b) >= 1

                    # add special tokens
                    input_ids = self.tokenizer.build_inputs_with_special_tokens(tokens_a, tokens_b)
                    # add token type ids, 0 for sentence a, 1 for sentence b
                    token_type_ids = self.tokenizer.create_token_type_ids_from_sequences(tokens_a, tokens_b)
                    
                    # 드디어 아래 항목에 대한 데이터셋이 만들어졌습니다! :-)
                    # 즉, segmentA[SEP]segmentB, [0, 0, .., 0, 1, 1, ..., 1], NSP 데이터가 만들어진 것입니다 :-)
                    # 그럼 다음은.. 이 데이터에 [MASK] 를 씌워야겠죠?
                    example = {
                        "input_ids": torch.tensor(input_ids, dtype=torch.long),
                        "token_type_ids": torch.tensor(token_type_ids, dtype=torch.long),
                        "next_sentence_label": torch.tensor(1 if is_random_next else 0, dtype=torch.long),
                    }

                    self.examples.append(example)

                current_chunk = []
                current_length = 0

            i += 1

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i):
        return self.examples[i]    
