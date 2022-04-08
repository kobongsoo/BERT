import torch
import torch.nn.functional as F
import time

from transformers import BertTokenizer, BertForSequenceClassification
from os import sys
sys.path.append('..')
from myutils import GPU_info, seed_everything, mlogging

device = GPU_info()
seed_everything(111)
#logger = mlogging(loggername="cmodel", logfilename="cmodel")

#=================================================================================================================
# classification 모델과 tokenizer 설정
cassification_model_path = '../../model/classification/bmc-fpt-wiki_20190620_mecab_false_0311-nouns-0327-nscm-0329'
cassification_vocab_path = '../../model/classification/bmc-fpt-wiki_20190620_mecab_false_0311-nouns-0327-nscm-0329/vocab'

cassification_tokenizer = BertTokenizer.from_pretrained(cassification_vocab_path, do_lower_case=False, max_len=128)
#cassification_model = torch.load(cassification_model_path)
cassification_model = BertForSequenceClassification.from_pretrained(cassification_model_path, num_labels=2)
cassification_model.to(device)
cassification_model.eval()

def classification_model_eval(sentence):
    
    starttime = time.time()
    
    inputs = cassification_tokenizer(sentence, return_tensors="pt")
    inputs.to(device)
    
    #logger.info(f'{inputs}')
    
    with torch.no_grad():
        
        cassification_outputs = cassification_model(**inputs)

        logits = cassification_outputs.logits
        #logger.info(f'logits:{logits}')
        
        prob = logits.softmax(dim=1)
        
        positive_prob = round(prob[0][1].item(), 4) # 긍정확률을 소수점 4자리까지 
        nagative_prob = round(prob[0][0].item(), 4) # 부정활률을 소수점 4자리까지
        
        processtime = f"처리시간: {time.time()-starttime:.3f}초"
        
        if torch.argmax(prob) == 1:
            pred = "긍정(positive)"
        else:
            pred = "부정(nagative)"
            
        return {
            'sentence': sentence,
            'prediction' : pred,
            'positive_data' : f"긍정 : {positive_prob}",
            'nagative_data' : f"부정 : {nagative_prob}",
            'positive_width' : f"{positive_prob * 100}%",
            'nagative_width' : f"{nagative_prob * 100}%", 
            'process_time' : processtime
        }
        
#=================================================================================================================

  
#=================================================================================================================
# sentenct-bert를 가지고 문장 유사도를 출력하는 예제임
from sentence_transformers import SentenceTransformer, util
import numpy as np

sbert_model_path = '../../model/sbert/sbert-ts2022-04-01-distiluse-7'
embedder = SentenceTransformer(sbert_model_path)


def sbert_model_eval(querys : str, 
                     labels: str):
    
    starttime = time.time()
        
    # query와 label을 , 구분자로 나눔 
    querylist = querys.split(',')
    labellist = labels.split(',')  
   
    #print(querylist)
    #print(labellist)
  
        
    labels_embeddings = embedder.encode(labellist, convert_to_tensor=True)
    
    query_embedding = embedder.encode(querylist, convert_to_tensor=True)
    cos_scores = util.pytorch_cos_sim(query_embedding, labels_embeddings)[0]
    cos_scores = cos_scores.cpu()

    processtime = f"처리시간: {time.time()-starttime:.3f}초"
        
    #We use np.argpartition, to only partially sort the top_k results
    top_k = len(labellist)
    top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]

    result: str = ""
    for idx in top_results[0:top_k]:
        #print(labellist[idx].strip(), "(Score: %.4f)" % (cos_scores[idx]))
        result += labellist[idx].strip() + "(Score: %.4f)" % (cos_scores[idx]) + "</br>"
    
    return {
        'querys' : querys,
        'result': result,
        'proctime' : processtime
    }
         
#=================================================================================================================
# Summarizer 라이브러리를 이용한 추출 요약 예제임

from summarizer.sbert import SBertSummarizer

# s-bert 이용함
#model_path = '../../model/sbert/sbert-ts2022-04-01-distiluse-7'
model = SBertSummarizer(sbert_model_path)

def summarizer_model_eval(texts):
    start = time.time()
    result = model(texts, ratio=0.1)

    full = ''.join(result)
    processtime = f"처리시간: {time.time()-start:.3f}초"
    # print(full)
    # print('\n')
    # print(texts)
    # 출력 
    return { 
        'summary' : full,  # 요약 문장 
        'proctime' : processtime  #처리시간
    }
    
    