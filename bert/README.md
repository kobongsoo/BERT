## BERT 예제
- [Hugging Face](https://huggingface.co/)의 [Transformers 라이브러리](https://huggingface.co/docs/transformers/index)를 이용하였음
- [설치방법](https://huggingface.co/docs/transformers/installation)
```
pip install transformers
```
- 주로 다국어 BERT 모델(bert-base-multilingual-cased)을 이용하였음
- 주요 document는 [여기](https://huggingface.co/docs/transformers/model_doc/bert) 참조 바람

### 1. 훈련 예제
- 훈련을 시키기 위해서는 말뭉치와 추가할 vocab, 기존 훈련된 BERT 모델과 vocab 파일 필요함
- 추가 vocab 만드는 방법은 [여기](https://github.com/kobongsoo/BERT/tree/master/tokenizer_sample) 참조 바람
- 기존 모델과 vocab 파일들은 HuggingFace 모델(bert-base-multilingual-cased)들 불러와서, **save_pretrained 이용하여, 파일로 저장**할 수 있음
- 혹은 **cache_dir='저장할 폴더명'** 해서 파일로 저장할수도 있음(**단 이때는 저장 파일명이 랜덤한 파일로 생성되므로, 수동으로 이름변경해줘야함**)
```
# save_pretrained 이용하여, 파일로 저장 방법
from transformers import BertTokenizer, BertConfig, BertForMaskedLM

tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased')
model = BertForMaskedLM.from_pretrained('bert-base-multilingual-cased')    

### 전체모델 저장
os.makedirs(TMP_OUT_PATH, exist_ok=True)
# save_pretrained 로 저장하면 config.json, pytorch_model.bin 2개의 파일이 생성됨
model.save_pretrained(TMP_OUT_PATH)

# tokeinizer 파일 저장(vocab)
VOCAB_PATH = TMP_OUT_PATH
tokenizer.save_pretrained(VOCAB_PATH)    
```

```
# cache_dir 이용하여, 파일로 저장 방법
tokenizer = BertTokenizer.from_pretrained('bert-base-multilingual-cased', cache_dir='저장폴더')
model = BertForMaskedLM.from_pretrained('bert-base-multilingual-cased' ,cache_dir='저장폴더')    
```

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[bert-further-pretrain-BertForMaskedLM.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-further-pretrain-BertForMaskedLM.ipynb)|기존 훈련된 BERT 에, **추가 MLM만 훈련** 시키는 예제 | 훈련 코드는 pytorch로 구현되었음, 추가 vocab 이 필요함|
|[bert-further-pretrain-nsp-mlm.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-further-pretrain-nsp-mlm.ipynb)|기존 훈련된 BERT에, **추가 MLM 과 NLP 훈련** 시키는 예제 | 훈련 코드는 pytorch로 구현되었음, 추가 vocab 이 필요함|
|[bert-further-pretrain_trainer.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-further-pretrain_trainer.ipynb)|기존 훈련된 BERT에, **추가 MLM 과 NLP 훈련** 시키는 예제 | 훈련은 **HuggingFace Trainer를 이용**함, 추가 vocab 이 필요함|
|[bert_pretrain.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert_pretrain.ipynb)|**처음부터 MLM 과 NLP 훈련** 시키는 예제 | 훈련은 **HuggingFace Trainer를 이용**함, **새로운 Vocab 필요**|
|[sentencepiece-further-pretrain.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/sentencepiece-further-pretrain.ipynb)|**sentencepiecetokenizer로 MLM 훈련** 시키는 예제 | 훈련은 **HuggingFace Trainer를 이용**함, **새로운 Vocab 필요**|

### 2. Fine-Tuning 예제
- 사전훈련 시킨 모델들에 대해 Fine-Tuning 하는 예제임
- 기존 사전 훈련 시킨 모델과 vocab, 그리고 훈련/평가 말뭉치(예:NSMC, kornli 등)가 필요함
- 말뭉치들은 [여기](https://github.com/kobongsoo/BERT/tree/master/corpus_sample) 참조 바람

|구분|소스명|설명|기타|
|:-------:|:-----------------|:-------------------------------------------------------|:---------------------|
|훈련|[bert-finetuning-multiclassi-train.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-finetuning-multiclassi-train.ipynb)|분류 모델 Fine-Tuning 훈련 예제 | WandB 사용함, 훈련 코드는 pytorch로 구현됨|
|평가|[bert-finetuning-multiclassi-test.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-finetuning-multiclassi-test.ipynb)|훈련된 분류 모델 테스트 예제 | 평가코드는 pytorch로 구현됨|
|훈련|[bert-finetuning-nli-train.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-finetuning-nli-train.ipynb)|NLI 모델 Fine-Tuning 훈련 예제 | 훈련코드는 pytorch로 구현됨|
|평가|[bert-finetuning-nli-test.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-finetuning-nli-test.ipynb)|훈련된 NLI 모델 테스트 예제 | 평가코드는 pytorch로 구현됨|
|평가|[bert-MLM-test.ipynb](https://github.com/kobongsoo/BERT/blob/master/bert/bert-MLM-test.ipynb)|기존 사전 훈련된 모델 MASK 테스트 예제 | 평가코드는 pytorch로 구현됨|

### 3. 기타
- [Perplexity(PPL) 예제](https://github.com/kobongsoo/BERT/blob/master/bert/bert-perplexity-eval.ipynb) 
