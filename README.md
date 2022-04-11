# BERT

### BERT를 이용한 sementic 검색 모델 제작 과정 



![image](https://user-images.githubusercontent.com/93692701/162662241-1cb73079-c582-494c-8c25-0563589acb5f.png)




### 1) 사전 학습 모델 선정
- 다국어 지원 BERT-based-multilingual-case 혹은 처음부터 distilbert-base-multilingual-cased 선정할 수도 있음
- distilbert 선정하는 경우, 3) DistilBERT 제작 과정이 필요 없음.

### 2) 한국어 추가 사전 학습(Further Pre-Train) 
- Special domain 을 가진 corpora(말뭉치들)을 가지고, vocab 생성하고, 생성된 vocab을 기존 사전 학습 vocab에 추가하여, 새로운 vocab 생성함.
- Vocab 만들때 mecab 형태소 분석기를 이용하고, word만 뽑아내서 vocab을 만듬 
  ##### ex) make_mecab_vocab.ipynb
- Special domain 을 가진 copora(말뭉치들)을 가지고 기존 BERT 모델에 MLM 추가학습 시킴
- Random seed 값을 변경하면서, 여러 번 학습 시킴
  ##### ex) bert-further-pretrain-BertForMaskedLM.ipynb,  bert-further-pretrain_trainer.ipynb 

### 3) DistilBERT 제작
- #### 반드시 교사, 학생 모델의 tokenizer vocab은 같아야 함
- #### 학생 모델은 빈껍데기 (distil)BERT 생성 해서 이용해야 함
  ##### ex: distilbert-model-create.ipynb
- MLM + NLI 방식(MLM 하고 나서 NLI로 다시 Fine-Tuning) 혹은 NLI로만  Fine-Tuning 하여 Distilling  함
- Loss 함수의 Tempature(기본=10)와 alpha(기본=0.1)값을 조절하여 학습하면서, 최적이 값을 찾아야 함
  ##### ex) bert-Task-specific-knowledge-distillation.ipynb,  bert-Task-specific-knowledge-distillation2.ipynb

### 4) Sentence Bert(S-BERT) 제작
- DistilBERT를 가지고 STS 데이터 혹은 NLI 데이터를 이용하여 S-BERT을 만듬
- NLI 데이터로 만든  S-BERT는 반드시 한번 더 STS로 학습시킴. NLI만 학습한 S-BERT는 STS로 학습한 S-BERT에 비해 성능이 많이 떨어짐.
  ##### ex) sentence-bert-nli.ipynb, sentence-bert-sts.ipynb , sentence-bert-nli-sts.ipynb
  
### 5) S-BERT 지식 증류 학습
- 교사모델은 distiluse-base-multilingual-cased-v2, 학생모델은 제작한 S-BERT 모델로 설정 하여 학습시킴.
- 이때 말뭉치는 영어-한글 쌍으로 이루어진 말뭉치를 이용함(TED2020-en-ko-train.tsv)
  ##### ex) sbert-distillation.ipynb

### 6) Semantic 검색 모델 구축
- S-BERT + Elastic Serch  + Faiss 이용하여 검색  모델 구축
  ##### ex) sbert-Faiss-embedding.ipynb, sbert-Faiss-embedding2.ipynb, elasticsearch_text_embedding.ipynb



