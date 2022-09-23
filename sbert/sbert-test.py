#!/usr/bin/env python
# coding: utf-8

# In[1]:


import sys
from sentence_transformers import SentenceTransformer, InputExample
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator

sys.path.append('..')
from myutils import seed_everything, GPU_info, mlogging

logger = mlogging(loggername="s-bert-test", logfilename="../../log/s-bert-test")
device = GPU_info()


# In[ ]:


import os

# 평가할 s-bert 모델 경로
#smodel_path = "../model/sbert/distiluse-base-multilingual-cased-v2"

#smodel_path = "bongsoo/moco-sentencebertV1.0"
smodel_path = "../../data11/model/sbert/out-mbertV2.0-distil-2022-09-14"
#smodel_path = 'paraphrase-multilingual-mpnet-base-v2'
#smodel_path = "distiluse-base-multilingual-cased-v2"


# 평가시 cosine 유사도등 측정 결과값 파일 (similarity_evaluation_xxxx.xls) 저장될 경로
output_path = 'eval'
os.makedirs(output_path, exist_ok=True)

# 평가 sts 형태의 test 파일 
test_file_type = 2 # 0이면 korsts .tsv, 1이면 kluests.json 파일, 2이면 통합
use_en_sts = True   # true이면 영문 sts 데이터셋 추가하여 평가시킴.

# tsv 파일 인 경우
if test_file_type == 0 or test_file_type == 2:
    test_file1 = '../../data11/korpora/korsts/tune_test.tsv'

# json 파일 인 경우
if test_file_type == 1 or test_file_type == 2:
    test_file2 = '../../data11/korpora/klue-sts/klue-sts-v1.1_dev.json'

train_batch_size = 32


# In[ ]:


from datasets import load_dataset
test_samples = []


# /korsts/tune_test.tsv 파일을 불러옴
if test_file_type == 0 or test_file_type == 2:
    with open(test_file1, 'rt', encoding='utf-8') as fIn1:
        lines = fIn1.readlines()
        for line in lines:
            s1, s2, score = line.split('\t')
            score = score.strip()
            score = float(score) / 5.0
            test_samples.append(InputExample(texts=[s1,s2], label=score))


# /klue-sts/klue-sts-v1.1_dev.json 파일을 불러옴
if test_file_type == 1 or test_file_type == 2:
    import json

    with open(test_file2, "r") as fIn2:
        data = json.load(fIn2)
        for el in data:
            s1 = el["sentence1"]
            s2 = el["sentence2"]
            score = el["labels"]['label']
            test_samples.append(InputExample(texts=[s1,s2], label=score))
        
# 영문 stsb_multi_mt test 버전 파일 로딩함
if use_en_sts == True:
    en_sts_dataset = load_dataset("stsb_multi_mt", name="en", split="test")
    for data in en_sts_dataset:
        text_a = data["sentence1"]
        text_b = data["sentence2"]
        score = data["similarity_score"]
        score = float(score) / 5.0  #5로 나눠서 0~1 사이가 되도록 함
        test_samples.append(InputExample(texts= [text_a,text_b], label=score))
   
    #glue stsb valildation 데이터셋 불러옴(subset : "stsb" = 1,500)
    glue_stsb_dataset = load_dataset("glue","stsb", split="validation")
    for data in glue_stsb_dataset:
        text_a = data["sentence1"]
        text_b = data["sentence2"]
        score = data["label"]
        score = float(score) / 5.0  #5로 나눠서 0~1 사이가 되도록 함
        test_samples.append(InputExample(texts= [text_a,text_b], label=score))
    
print(test_samples[0:3])
print(f'*test_samples_len: {len(test_samples)}')


# In[ ]:


##############################################################################
# sentence bert 를 불러옴
# => 훈련되어서 저장된 s-bert 모델을 불러와서 성능 평가 해봄
# => 평가 내용은 해당 모델 경로에 'similarity_evaluation_korstr_tune_test_results.csv' 파일에 기록됨
# => 모델 다운로드 폴더 지정 : cache_folder=경로 
##############################################################################

logger.info("\n")
logger.info("======================TEST===================")

model = SentenceTransformer(smodel_path)
#model = SentenceTransformer(smodel_path, device='cpu')
#model = SentenceTransformer(smodel_path, cache_folder=output_path)
#model.to(device)
logger.info(f'{model}')


# In[ ]:


from sentence_transformers.evaluation import SimilarityFunction
import time

# 유사도 측정방식(COSINE, EUCLIDEAN, MANHATTAN, DOT_PRODUCT 중 선택 , 모두 spearman 방식임)
# => None 이면 아래 값들중 MAX 값 추력함
#main_similarity = None
main_similarity = SimilarityFunction.COSINE
#main_similarity = SimilarityFunction.EUCLIDEAN
#main_similarity = SimilarityFunction.MANHATTAN
#main_similarity = SimilarityFunction.DOT_PRODUCT

logger.info(f"main_similarity: {main_similarity}")

start = time.time()

test_evaluator = EmbeddingSimilarityEvaluator.from_input_examples(test_samples, main_similarity=main_similarity, batch_size=train_batch_size, name='korstr_tune_test', show_progress_bar=True)
result = test_evaluator(model, output_path=output_path)
logger.info(f"\n")
logger.info(f"model path: {smodel_path}")

if test_file_type == 0 or test_file_type == 2:
    logger.info(f"test_file1 path: {test_file1}")

if test_file_type == 1 or test_file_type == 2:
    logger.info(f"test_file2 path: {test_file2}")
    
if use_en_sts == True:
    logger.info(f"stsb_multi_mt")
    
logger.info(f'=== result: {result} ===')
logger.info(f'=== 처리시간: {time.time() - start:.3f} 초 ===')
logger.info("=====================================================")
logger.info("\n")


# In[ ]:




