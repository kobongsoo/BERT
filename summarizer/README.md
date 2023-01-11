### BERT 추출 요약(Extractive summary)&키워드 추출  <img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white"/><img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>

#### 1.개요
- 문서 요약에는 생성(추상)요약(abstractive summary)과 추출요약(extractive summary)이 있음.
- 생성(추상)요약은 GPT(Transformers 디코더),T5(인/디코더) 처럼 문장을 생성해서 요약하는 것임.
- 추출요약은 BERT(Transformers 인코더)처럼 다수의 문장에서 중요 문장을 추출하여 요약하는 것임.

#### 2.추출 요약 예제
- 기존 bert 모델, sentencebert 모델을 이용하여 문장에 대한 추출 요약하는 예제로,  NeuralCoref(신경참조) 를 이용한다.
- bert 추출 요약을 위해 아래 [bert-extractive-summarizer 패키지](https://github.com/dmmiller612/bert-extractive-summarizer) 설치해야 함
```
!pip install bert-extractive-summarizer
```
- Sentencebert 모델인 경우, SBertSummarizer 이용
```
from summarizer.sbert import SBertSummarizer

# sentence bert 모델인 경우=> sentence bert 모델 경로를 SBertSummarizer 함수 인자로 넘겨줌
model_path = 'sentencebert 모델 경로'
model = SBertSummarizer(model_path)

# min_length : 설정값 이하 길이 문장은 요약에 포함안됨, num_sentences : 요약문장을 몇문자으로 만들지 설정
# - 10이하 길이 문장은 요약문에 포함안됨. 요약문은 3개 문장으로 요약함(원본이 3개 이하면 원본 그대로 출력됨)
result = model(body, min_length=10, num_sentences=3)
```


- BERT 모델인 경우, Summarizer 이용
```
from summarizer.sbert import SBertSummarizer

model_path = 'BERT 모델 경로'

# bert 모델과 tokenizer 로딩
tokenizer = BertTokenizer.from_pretrained(model_path, do_lower_case=False, max_len=128)
bertmodel = BertModel.from_pretrained(model_path, output_hidden_states=True)

# bert 모델을 연결시킴
model = Summarizer(custom_model=bertmodel, custom_tokenizer=tokenizer)
```

#### 3. keyword 추출 예제
- [keybert.ipynb](https://github.com/kobongsoo/BERT/blob/master/summarizer/keybert.ipynb) : doc에서 키워드 등를 추출하는 예
```
pip install keybert
```

```
from keybert import KeyBERT
from transformers import AutoModel

model_path = "bongsoo/albert-small-kor-v1"#"klue/bert-base"
model = AutoModel.from_pretrained(model_path)
model.eval()
text = {TEXT}
kw_model = KeyBERT(model)
keywords = kw_model.extract_keywords(text, keyphrase_ngram_range=(1, 1), stop_words=None, top_n=5)  # top_n= 키워드 출력 계수
print(keywords)
```

#### 4. 참고
- [Bert Extractive Summarizer](https://github.com/dmmiller612/bert-extractive-summarizer)
- [keybert](https://maartengr.github.io/KeyBERT/ )  
