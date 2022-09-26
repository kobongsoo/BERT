## BERT를 이용한 sementic 검색 모델 제작 과정 
<img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white"/><img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fkobongsoo%2FBERT&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)

- 아래 과정을 통해 제작된 [sentencebert 모델](https://huggingface.co/bongsoo/moco-sentencedistilbertV2.1) 을 이용해 Sementic 문장 유사도 테스트 해볼 수 있음.

### ![image](https://user-images.githubusercontent.com/93692701/162686553-7d1b46e2-fdf2-4cd7-b842-a5ade3f9cda6.png)



### 1) 사전 학습 모델 선정
- 다국어 지원 BERT-based-multilingual-case 혹은 처음부터 distilbert-base-multilingual-cased 선정할 수도 있음
- **distilbert 선정하는 경우, 3) DistilBERT 제작 과정이 필요 없음.**

### 2) 한국어 추가 사전 학습(Further Pre-Train) 
- Special domain 을 가진 corpora(말뭉치들)을 가지고, vocab 생성하고, 생성된 vocab을 기존 사전 학습 vocab에 추가하여, 새로운 vocab 생성함.
- Vocab 만들때 mecab 형태소 분석기를 이용하고, word만 뽑아내서 vocab을 만듬 
- mecab에는 명사만 추출하는 nouns 와 형태소도 추출하는 morphs 2가지 방법이 있다.
<br>nouns는 한국어 명사들만 vocab에 추가하는 방식이므로, 한국어 이외 말뭉치에는 적용이 힘들다.
<br>morphs는 형태소(조사, 부사,어미등)도 vocab에 추가하는 방식으로, 한국어이외 영어등도 vocab에 추가할수 있다.

  ex) [make_mecab_vocab.ipynb](https://github.com/kobongsoo/BERT/blob/master/tokenizer_sample/make_mecab_vocab.ipynb)

```
[vocab 생성 과정]

1. 도메인 말뭉치(예:kowiki.txt)에서 mecab을 이용하여 형태소 분석하여 단어들을 추출함.
  - mecab으로 형태소 혹은 명사만 분할하면서, 
    subword 앞에는 '##' prefix 추가함(**Bertwordpiece subword와 동일하게)

2. NLTK 빈도수 계산하는 FreqDist()를 이용하여, 단어들이 빈도수 계산 후,
   상위 빈도수(예:30000)를 가지는 단어들만 add_vocab.txt 로 만듬

3. 기존 bert vocab.txt 파일에 직접, add_vocab.txt 토큰들 추가(*이때 중복 제거함)

4. 추가한 vocab을 가지고, tokenizer 생성하고, special 토큰 추가 후, vocab.txt 파일에 저장
  - 원래 tokenizer.add_tokens() 으로 추가하면, added_tokens.json 파일에 추가되는데, 
    이때 BertTokenizer.from_pretrained() 함수로 호출할때,호출이 안됨
    (*이유 모름:엄청 느려지는것 같음) 따라서 직접 vocab.txt에 추가하는 방법을 사용함
```

- Special domain 을 가진 copora(말뭉치들)을 가지고 기존 BERT 모델에 MLM 추가학습 시킴
- Random seed 값을 변경하면서, 여러 번 학습 시킴

  ex)[bert-MLM-Trainer-V1.2.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-MLM-Trainer-V1.2.ipynb) 
  ,[bert-further-pretrain-BertForMaskedLM.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-further-pretrain-BertForMaskedLM.ipynb)
  , [bert-further-pretrain_trainer.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-further-pretrain_trainer.ipynb)

[참고 : Hugging Face-Transformers](https://huggingface.co/docs/transformers/index)

### 3) DistilBERT 제작
- **반드시 교사, 학생 모델의 tokenizer vocab은 같아야 함**
- **학생 모델은 빈껍데기 (distil)BERT 생성 해서 이용해야 함**

  ex) [distilbert-model-create.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/distilbert-model-create.ipynb)

- MLM + NLI 방식(MLM 하고 나서 NLI로 다시 Fine-Tuning) 혹은 NLI로만  Fine-Tuning 하여 Distilling  함
- Loss 함수의 Tempature(기본=10)와 alpha(기본=0.1)값을 조절하여 학습하면서,최적이 값을 찾아야 함

  ex) [bert-Task-specific-knowledge-distillation.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/distillation/bert-Task-specific-knowledge-distillation.ipynb)
  , [bert-Task-specific-knowledge-distillation2.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/distillation/bert-Task-specific-knowledge_distillation2.ipynb)
```
[증류 과정(Knowledge-distillaton)]

1. 교사모델 구조->학생 모델로 복사
 - 교사모델이 bert-base 이고, 학생 모델이 distilbert 라면, 교사 bert 모델 12개 hiddenlayer
  에 wegiht와 bias 값들을 학생모델 distilbert 6개 hiddenlayer로 복사함.
  (* 이때 교사모델이 어떤 hiddenlayer를 학생모델로 복사할때는,
   [0, 2, 4, 7, 9, 11] 식으로  한칸씩 건너 띄면서, 레이어를 복사 하는데 좋다고 함)

2. 교사모델, 학생모델 fine-tuning 사전준비
 - 각 교사, 학생모델을 classifcation이나 maksedlm 모델중 선택해서 Fine-Tuning 함
  (*Huggingface transformers 모델이용하면 쉬움)

3. loss 함수 정의
 - loss 함수는 학생모델이 loss(1), 교사.학생모델간 cross-entropy loss(2), 
   교사.학생모델간 cosine-loss(3) 3가지 인데, 이때 (2)와 (3) loss는 
   torch.nn.KLDivLoss 함수로 보통 대체 된다.
   즉 증류 손실함수 = alpha * 학생모델이 loss(1) 
                  + (1-alpah)*교사.학생모델간 torch.nn.KLDivLoss(2)(3) 함수

 - 이때 KLDivLoss 함수는 교사와 학생간 Dark Knowledge(어둠지식)도 학습되도록,
   교사loss/Temperture와 학생loss/Temperture 식으로, Temperture를 지정하는데, 
   보통 학습할때는 2~10으로 하고, 평가시에는 반드시 1로 해야 한다.
   (*Temperture==1 이면, softmax와 동일, 1보다 크면 확률이 평활화 되어서, 
    어둠 지식 습득이 많이됨)
   
 - 또한 학생모델loss는 전체 loss에 0.1이 되도록 alpha값은 0.1이 좋다고 한다.

4. 학습
 - 교사모델은 평가(eval)만 하고, 학생모델만 학습(train)한다.
```

### 4) Sentence Bert(S-BERT) 제작
- DistilBERT를 가지고 STS 데이터 혹은 NLI 데이터를 이용하여 S-BERT을 만듬
- NLI 데이터로 만든  S-BERT는 반드시 한번 더 STS로 학습시킴. **NLI만 학습한 S-BERT는 STS로 학습한 S-BERT에 비해 성능이 많이 떨어짐.**

  ex) [sentence-bert-nli.ipynb](https://github.com/kobongsoo/BERT/blob/master/sbert/sentence-bert-nli.ipynb)
    , [sentence-bert-sts.ipynb](https://github.com/kobongsoo/BERT/blob/master/sbert/sentece-bert-sts.ipynb)
    , [sentence-bert-nli-sts.ipynb](https://github.com/kobongsoo/BERT/blob/master/sbert/sentence-bert-nli-sts.ipynb)

[참고: SentenceTransformers](https://www.sbert.net/)
  
### 5) S-BERT 지식 증류 학습
![image](https://user-images.githubusercontent.com/93692701/175485631-ab223288-b99d-4179-8497-73b860f3847b.png)
<br> 참고 : https://sbert.net/examples/training/multilingual/README.html


- 교사모델은 **paraphrase-multilingual-mpnet-base-v2 혹은 distiluse-base-multilingual-cased-v2 둘중 하나 선택**, 학생모델은 제작한 S-BERT 모델로 설정 하여 학습시킴.<br>
자체 테스트시, 위 2개의 모델이 가장 성능이 좋았음(*아래표 참조)

 다운로드 : [paraphrase-multilingual-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2)
,[distiluse-base-multilingual-cased-v2](https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v2)
 
- **교사모델과 학생모델의 word_embedding_dimension(예: Dim=768)은 반드시 같아야함. 다르면 훈련시,'The size of tensor a (768) must match the size of tensor b (384) at non-singleton dimension 1' 에러 발생함**
- 이때 말뭉치는 **영어-한글 쌍으로 이루어진 말뭉치**를 이용함(TED2020-en-ko-train.tsv)
- 아래 표는 [S-BERT Pretrain 모델들](https://www.sbert.net/docs/pretrained_models.html)에 대해 영어-한글 쌍 말뭉치(TED2020-en-ko-train.tsv) 로 학습 후, korsts, klue-sts 로 평가해본 결과임

|교사모델명(S-BERT)|설명|korsts|Klue-sts|korsts+Klue-sts 평균|기존성능평가|
|:-------------:|:---------------------------|:-----:|:-----:|:-----:|:-----------------------------|
|all-mpnet-base-v2|base 모델: microsoft/mpnet-base, size:420MB, max_seq_len: 384|74.2%|74.7%|74.7%|embedding:69.57%, search:57.0%,GPU Speed(sentence/sec):2,800|
|multi-qa-distilbert-cos-v1|base 모델: distill-base, size:250MB, max_seq_len: 512|73.2%|73.4%|73.3%|embedding:69.98%, search:52.83%,GPU Speed:4,000|
|paraphrase-multilingual-mpnet-base-v2|교사/학생 모델: paraphrase-mpnet-base2/xlm-reberta-base, size:970MB, max_seq_len: 128, +50개 추가 언어 지원(한국어포함)|78.8%|78.2%|78.5%|embedding:65.83%, search:41.68%,GPU Speed:2,500|
|distiluse-base-multilingual-cased-v1|교사/학생 모델: mUSE/distilbert-base-multilingual, size:480MB, max_seq_len: 128, +15개 언어 지원(한국어포함)|74.2%|80.1%|77.15%|embedding:61.3%, search:29.87%,GPU Speed:4,000|
|distiluse-base-multilingual-cased-v2|교사/학생 모델: mUSE/distilbert-base-multilingual, size:480MB, max_seq_len: 128, +50개 추가 언어 지원(한국어포함)|75.0%|80.5%|77.75%|embedding:60.18%, search:27.35%,GPU Speed:4,000|

  ex) [sbert-distillation.ipynb](https://github.com/kobongsoo/BERT/blob/master/sbert/sbert-distillaton.ipynb)


### 6) Semantic 검색 모델 구축
- S-BERT + Elastic Serch  + Faiss 이용하여 검색  모델 구축

  ex) [sbert-Faiss-embedding.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/faiss/sbert-Faiss-embedding.ipynb)
     , [sbert-Faiss-embedding2.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/faiss/sbert-Faiss-embedding2.ipynb)
    , [elasticsearch_text_embedding.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/elasticsearch_text_embedding.ipynb)
    
[참고 : Faiss 라이브러리](https://github.com/facebookresearch/faiss)
