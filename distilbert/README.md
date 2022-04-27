## DistilBert 예제

- [Hugging Face](https://huggingface.co/)의 [Transformers 라이브러리](https://huggingface.co/docs/transformers/index)를 이용하였음
- [설치방법](https://huggingface.co/docs/transformers/installation)
```
pip install transformers
```

### 1. 개요
- 사전 학습된 BERT는 매개변수가 많고(사이즈가 크다) 추론에 시간이 오래 걸려 휴대폰과 같은 edge 디바이스에서 사용이 어렵다.
이러한 문제를 완하 하기 위해 사전 학습된 large bert에서 small bert로 지식을 이전하는 **지식 증류(Knowledge distillation)를 사용할 수 있다.**
- DistilBERT의 궁극적인 아이디어는 사전 학습된 대규모 BERT 모델을 기반으로 지식 증류를 통해 지식을 소규모 BERT로 이전하는 것이다.
- DistilBERT는 대형 bert에 비해 **60% 더 빠르며 40% 더 작다**

### 1. 훈련 예제
- 훈련을 시키기 위해서는 말뭉치와 추가할 vocab, 기존 훈련된 BERT 모델과 vocab 파일 필요함
- 추가 vocab 만드는 방법은 [여기](https://github.com/kobongsoo/BERT/tree/master/tokenizer_sample) 참조 바람

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[distilbert-further-pretrain-MaskedLM.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/distilbert-further-pretrain-MaskedLM.ipynb)|기존 훈련된 DistilBERT 에, **추가 MLM만 훈련** 시키는 예제 | 훈련 코드는 pytorch로 구현되었음, 추가 vocab 이 필요함|
|[distilbert-model-create.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/distilbert-model-create.ipynb)|**훈련 안된 빈 껍데기 모델 만드는 예제**|embedding_size, 단어 임베딩 편차등을 설정해야 함|
|[sentence-distilbert-nli.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/sentence-distilbert-nli.ipynb)|**DistilBERT를 SentenceBERT로 만드는 예제**| NLI 학습시킴, sentence-transformers 패키지를 이용|

### 2. 지식증류 예제

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[bert-distillation1.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/distillation/bert-distillation1.ipynb)|훈련은 하지않고, **교사모델 구조->학생 모델로 복사 적용만** 하는 예제| state_dict 이용|
|[bert-Task-specific-knowledge-distillation.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/distillation/bert-Task-specific-knowledge-distillation.ipynb)|**교사모델(BERT)과 학생모델(DistilBert) Fine-tuning 하여 증류**하는 예제|**교사/학생 모델이 tokenizer는 같아야함**, MLM 혹은 Classifcation 모델 사용|
|[bert-Task-specific-knowledge_distillation2.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/sentence-distilbert-nli.ipynb)|**교사 모델(BertModel:12개 hiddenlayer) -> 학생모델(BertModel:6개 hiddenlayer) 로 distillation** 하는 예제| **교사/학생 모델이 tokenizer는 같아야함**, MLM 모델 사용|

### <지식 증류 과정>
![image](https://user-images.githubusercontent.com/93692701/165438557-c55cbd05-7681-4a14-931a-579e25a55228.png)

#### 1. 교사모델 구조->학생 모델로 복사
- 교사모델이 bert-base 이고, 학생 모델이 distilbert 라면, 교사 bert 모델이 12개 hiddenlayer에 wegiht와 bias 값들을 학생모델 distilbert 6개 hiddenlayer로 복사함.
(이때 교사모델이 어떤 hiddenlayer를 학생모델로 복사할때는 **[0, 2, 4, 7, 9, 11] 식으로 건너 띄어서 레이어를 복사 하는데 좋다고 함**)

#### 2. 교사모델, 학생모델 fine-tuning 사전준비
- 각 교사, 학생모델을 classifcation이나 maksedlm 모델중 하나로 파인튜닝함

#### 3. loss 함수 정의
- loss 함수는 학생모델이 loss(1), 교사와 학생모델간 cross-entropy loss(2), 교사와 학생모델간 cosine-loss(3)  3가지 인데, 이때 (2)와 (3) loss는 torch.nn.KLDivLoss 함수로 보통 대체 된다.
- 즉 증류 손실함수 = alpha*학생모델이 loss + (1-alpah)*교사/학생모델간 torch.nn.KLDivLoss 함수
- 이때 KLDivLoss 함수는 교사와 학생간 Dark Knowledge(어둠지식)도 학습되도록 교사loss/Temperture와 학생loss/Temperture 식으로, Temperture를 지정하는데, 보통 학습할때는 2~10으로 하고, 평가시에는 반드시 1로 해야 한다.
- Temperture==1 이면, softmax와 동일, 1보다 크면 확률이 평활화 되어서, 어둠 지식 습득이 많이됨
- 학생모델loss는 전체 loss에 0.1이 되도록 alpha값은 0.1이 좋다고 함

#### 4. 훈련
- 교사모델은 평가(eval)모드로, 학생모델은 학습(train)모드로 설정해서 훈련 함

### 3. Fine-Tuning 예제

|구분|소스명|설명|기타|
|:---|:-----------------|:-----------------------------------------------------------|:---------------------|
|훈련|[distilbert-finetuning-nli-train.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/finetuning/distilbert-finetuning-nli-train.ipynb)|NLI Fine-Tuning 훈련 예제| 훈련코드는 pytorch|
|평가|[distilbert-finetuning-nli-test.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/finetuning/distilbert-finetuning-nli-test.ipynb)|NLI Fine-Tuning 모델 평가 예제| |
|훈련|[distilbert-finetuning-QA-train.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/finetuning/distilbert-finetuning-QA-train.ipynb)|Q&A Fine-Tuning 훈련 예제| 훈련코드는 pytorch|
|평가|[distilbert-finetuning-QA-test.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/finetuning/distilbert-finetuning-QA-test.ipynb)|Q&A Fine-Tuning 모델 평가 예제| |
|테스트|[distilbert-QA-test.ipynb](https://github.com/kobongsoo/BERT/blob/master/distilbert/finetuning/distilbert-QA-test.ipynb)|Q&A 모델 테스트 예제| |
