#!/usr/bin/env python
# coding: utf-8

# In[1]:


#======================================================================================================
# sentence-bert 를 tearch-student 관계 모델로 구성하여, 영어 sbert 학습을 학국어 모델에 증류학습시키는 예시
# -> 선생님모델은  영어 bert가 되고, 학생모델은 학국어 포함된다국어 bert로 설정
# -> 영어 bert가 다국어 bert를 가리키는 방식으로 학습됨
#
# => sentence-transformers 패키지를 이용하여 구현 함.(*pip install -U sentence-transformers 설치 필요)
#
# => 여기서는 교사모델을 distiluse-base-multilingual-cased-v2 로, 학생모델은 distilbert-base-multilingual 로 하여 학습시캄.
# => distiluse-base-multilingual-cased-v2 는 Teacher: mUSE; Student: distilbert-base-multilingual 로 학습시킨 s-bert 모델임
#     (https://www.sbert.net/docs/pretrained_models.html 참조)
#
# => ** 중요한 것은 교사와 학생모델간 word_embedding dimension은 서로 일치해야 함.(일치하지않으면 훈련시 아래와 같은 에러 발생함)
#     에러 : The size of tensor a (768) must match the size of tensor b (384) at non-singleton dimension 1
#
# [참고 소스] 
# https://towardsdatascience.com/a-complete-guide-to-transfer-learning-from-english-to-other-languages-using-sentence-embeddings-8c427f8804a9
# https://github.com/UKPLab/sentence-transformers/blob/master/examples/training/multilingual/make_multilingual_sys.py
#
# pip install -U sentence-transformers
#======================================================================================================

from torch.utils.data import DataLoader
import math
from sentence_transformers import models, losses
from sentence_transformers import SentencesDataset, LoggingHandler, SentenceTransformer, util, InputExample
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator
from datetime import datetime
import sys
import os
import gzip
import csv

sys.path.append('..')
from myutils import seed_everything, GPU_info, mlogging

logger = mlogging(loggername="s-bert-ts", logfilename="s-bert-ts")
device = GPU_info()
seed_everything(111)


# In[2]:


# 선생님 모델 설정
print("Load teacher model")

#teacher_model_name = 'bert-base-nli-stsb-mean-tokens'
#teacher_model_name = "../../data11/model/sbert/teacher/distiluse-base-multilingual-cased-v2-not-Dense"
teacher_model_name = "../../data11/model/sbert/teacher/paraphrase-multilingual-mpnet-base-v2"

teacher_model = SentenceTransformer(teacher_model_name)
print(teacher_model)


# In[3]:


#==========================================================================================================
# 학생 모델 설정
# => * 학생모델이 이미 sentencebert일지라도, 아래처럼 sbert모델 아닌 것처럼 word_embedding_model, pooling_model 을 각각
#    만들어서 처리하는것이 테스트 시 효율의 좋음
#
# [학생 모델 생성 방법]
# 1) word_embedding 모델 생성
# 2) pooling 모델 생성 : pooling 정책을 설정함 : CLS, 평균, MAX 정책중 택1(*평균 정책이 효율의 가장 좋다고 함)
# 3) 1) + 2) 모델을 연결시켜서 하나의 sbert 모델 만듬
#==========================================================================================================
student_model_name = "../../data11/model/sbert/sbert-mbertV2.0"

print("Load student model")


# === *sbert 모델 아닌 경우 =====
# word embedding 모델 설정(기존 다국어 모델 불러옴)
word_embedding_model = models.Transformer(student_model_name)

# pooling 정책 설정(mean 평균 정책으로 지정)
pooling_model = models.Pooling(word_embedding_model.get_word_embedding_dimension(),
                               pooling_mode_mean_tokens=True,
                               pooling_mode_cls_token=False,
                               pooling_mode_max_tokens=False)

# 학생 SBERT 생성
# -> word_embedding model 과 pooling_model를 연결시켜줌
student_model = SentenceTransformer(modules=[word_embedding_model, pooling_model])


# === *sbert 모델 인 경우 =====
# 기존 s-model 로딩 함
#student_model = SentenceTransformer(student_model_name)

print(student_model)


# In[4]:


# 훈련 및 평가 데이터 불러오고, 손실함수(MSELoss) 설정함(*학생모델에 설정함)
# 원본 소스코드 : 
# https://github.com/UKPLab/sentence-transformers/blob/master/sentence_transformers/datasets/ParallelSentencesDataset.py

from sentence_transformers.datasets import ParallelSentencesDataset

max_seq_length = 128
train_batch_size = 128
num_epochs = 40 

###### Load train sets ######    
#train_file = '../korpora/pair/Tatoeba-eng-kor/Tatoeba-eng-kor-train.tsv'
train_file = '../../data11/korpora/pair/en-ko/en_ko_train.tsv'

train_reader = ParallelSentencesDataset(student_model=student_model, teacher_model=teacher_model)
train_reader.load_data(train_file)
train_dataloader = DataLoader(train_reader, shuffle=True, batch_size=train_batch_size)
train_loss = losses.MSELoss(model=student_model)


# In[5]:


print(len(train_reader))
train_reader.__getitem__(0)
print(train_reader.next_entry(0)) # (source, {traget}) 첫번째 문장을 출력해봄


# In[6]:



###### Load dev sets ######
# 평가 데이터 불러와서 유사도 측정 평가자 설정함
#=>stst 파일 있는 경우에만 지정해줌.

from torch.utils.data import DataLoader
from sentence_transformers import SentencesDataset, losses,readers
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator,MSEEvaluator, SequentialEvaluator

evaluators = []
dev_samples = []

eval_file = '../../data11/korpora/korsts/tune_test.tsv'
with open(eval_file, 'rt', encoding='utf-8') as fIn:
    lines = fIn.readlines()
    for line in lines:
        s1, s2, score = line.split('\t')
        if s1[0] == "" or s1[1] == "":
            continue
        score = score.strip()
        score = float(score) / 5.0  #5로 나눠서 0~1 사이가 되도록 함
        dev_samples.append(InputExample(texts= [s1,s2], label=score))

# 영어 문장, 한국어 문장 유사도 측정을 위한 평가자(Evaluator) 설정
evaluator_sts = EmbeddingSimilarityEvaluator.from_input_examples(dev_samples, 
                                                                 batch_size=train_batch_size, 
                                                                 name='dev')
# evaluators에 추가함(*아래 테스트 데이터 evaluators도 추가함)
evaluators.append(evaluator_sts)
print(len(dev_samples))


# In[7]:


###### Load test sets ######
from torch.utils.data import DataLoader
from sentence_transformers import SentencesDataset, losses,readers
from sentence_transformers.evaluation import EmbeddingSimilarityEvaluator,MSEEvaluator, SequentialEvaluator, TranslationEvaluator
evaluators = []
# 테스트 데이터 불러와서 MSE 평가자 설정함
src_sentences = []
trg_sentences = []

#test_file = '../korpora/pair/Tatoeba-eng-kor/Tatoeba-eng-kor-test.tsv'
test_file = '../../data11/korpora/pair/TED2020-en-ko/TED2020-en-ko-dev.tsv'

# 참고소스: https://texasvaluesaction.org/Foysal87/Bangla-sentence-embedding-transformer/blob/master/Bangla_transformer.py
with open(test_file, 'rt', encoding='utf-8') as fIn:
    for line in fIn:
        splits = line.strip().split('\t')
        if len(splits) != 2:
            continue

        if splits[0] != "" and splits[1] != "":
            src_sentences.append(splits[0])
            trg_sentences.append(splits[1])
        
test_mse = MSEEvaluator(src_sentences, trg_sentences, teacher_model=teacher_model, name='test')
evaluators.append(test_mse)

# TranslationEvaluator computes the embeddings for all parallel sentences. 
# It then check if the embedding of source[i] is the closest to target[i] out of all available target sentences
test_acc = TranslationEvaluator(src_sentences, trg_sentences, batch_size=train_batch_size)
evaluators.append(test_acc)
print(len(src_sentences))


# In[ ]:


###### Train model ######
# 훈련 시작
# 훈련을 시작하면, output_path/eval/ 폴더에 mse 테스트, similarity 테스트 csv 파일에 기록됨
# (mse_evaluation_test_results.csv , similarity_evaluation_dev_results.csv)
import time

#10% of train data for warm-up
warmup_steps = math.ceil(len(train_reader) * num_epochs / train_batch_size * 0.1) 
evaluation_steps = warmup_steps
checkpoint_save_steps = warmup_steps * 2

output_path = "../../data11/model/sbert/out-mbertV2.0-distil-" + datetime.now().strftime("%Y-%m-%d")
check_path = "../../data11/model/sbert/ckp-mbertV2.0-distil-" + datetime.now().strftime("%Y-%m-%d")

logger.info(f"----------------------------------------------------------------------")
logger.info("*Warmup-steps:{}, checkpoint_save_steps:{}, ephocs:{}, train_data_len:{}, train_batch_size: {}".format(warmup_steps, checkpoint_save_steps, num_epochs, len(train_reader), train_batch_size))
logger.info("*teacher_model: {}".format(teacher_model_name))
logger.info("*student_model_name: {}".format(student_model_name))
logger.info(f"----------------------------------------------------------------------")
logger.info("*train_file: {}".format(train_file))
#logger.info("*eval_file: {}".format(eval_file))
logger.info("*test_file: {}".format(test_file))
logger.info(f"----------------------------------------------------------------------")
logger.info("*out_path: {}".format(output_path))
logger.info("*check_path: {}".format(check_path))
logger.info(f"----------------------------------------------------------------------")

start = time.time()

student_model.fit(train_objectives=[(train_dataloader, train_loss)],
          evaluator=SequentialEvaluator(evaluators, main_score_function=lambda scores: scores[-1]),
          epochs=num_epochs,
          evaluation_steps=evaluation_steps,
          warmup_steps=warmup_steps,   # 처음 10%는 아주작게 스탭을 옮김
          scheduler='warmupconstant',
          output_path=output_path,
          save_best_model=True,
          optimizer_params= {'lr': 5e-5, 'eps': 1e-6, 'correct_bias': False},
          checkpoint_path=check_path,
          checkpoint_save_steps=checkpoint_save_steps,
          checkpoint_save_total_limit=5 
          )

logger.info(f'=== 처리시간: {time.time() - start:.3f} 초 ===')
logger.info(f"\n")


# In[ ]:


# 마지막 model 저장
output_path = "../../data11/model/sbert/sbert-mbertV2.0-distil-" + datetime.now().strftime("%Y-%m-%d")
student_model.save(output_path)


# In[ ]:




