## 유사도 측정 예제
- 문장들의 유사도는 모델의 출력 임베딩 값들을 가지고, 코사인 유사도를 가지고 측정한다.

### 1. BERT 예제

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[bert-embedding.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/bert-embedding.ipynb)|last_hidden_state 평균값만으로 유사도 측정하는 예제||
|[bert-sentence-embedding.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/bert-sentence-embedding.ipynb)|pooled_out 값 혹은 last_hidden_state 평균값 혹은 hidden_state의 마지막 2번째 레이어 평균값으로 유사도 측정 하는 예제|모델 불러올때 **output_hidden_states=True** 해줘야 함|
|[bert-sentence-embedding-long-text.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/bert-sentence-embedding-long-text.ipynb)|입력 문장이 토큰이 512보다 큰 문장인 경우, input_id_chunks 토큰(512 계수)들로 분할하여 처리하는 예제|tokenizer 불러올때, **add_special_tokens=False**로 해야 함, 모델 불러올때 **output_hidden_states=True** 해줘야 함|
|[bert-zero-shot-nlp.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/bert-zero-shot-nlp.ipynb)|NLI 모델 예제 : 각 문장과 labels를 가지고, 문장(전제)과 labels(가설)간 관계가 최대 참(entailment) 일 확률을 구하는 예제|BertForSequenceClassification 모델 불러올때 **output_hidden_states=True, num_labels=3** 해줘야 함|
|[bert-word-embedding.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/bert-word-embedding.ipynb)|한 문장에서 중복 단어들간 유사도 측정하는 예제|모델 불러올때 **output_hidden_states=True** 해줘야 함|
|[kobert-word-embedding.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/kobert-word-embedding.ipynb)|한 문장에서 중복 단어들간 유사도 측정하는 예제|모델 불러올때 **output_hidden_states=True** 해줘야 함, **Kobert 모델/SentencePieceTokenzier** 이용|

### 2. Sentence Bert 예제

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[sentence-bert-embedding.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/sentence-bert-embedding.ipynb)|sentence-bert를 가지고 유사도 측정하는 예제|**Sentence Bert 모델** 이용|
|[sentence-bert-embedding-by-bert.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/sentence-bert-embedding-by-bert.ipynb)|BERT 모델을 Sentence Bert로 만들고(훈련은 안시킴) 유사도 측정하는 예제|**BERT 모델** 이용|
|[sentence-bert-clustering.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/sentence-bert-clustering.ipynb)|sentence-bert를 가지고 클러스터링 하는 예제|**Sentence Bert 모델** 이용|

### 3. FAISS 예제

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[sbert-Faiss-embedding.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/faiss/sbert-Faiss-embedding.ipynb)|FAISS를 이용한 Sementic Search 예제 |**Sentence Bert 모델** 이용|
|[sbert-Faiss-embedding2.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/faiss/sbert-Faiss-embedding2.ipynb)|FAISS를 이용한 Sementic Search 예제+데이터 추가 예제|**Sentence Bert 모델** 이용|
