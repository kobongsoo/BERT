## 유사도 측정 예제 <img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white"/><img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
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
|[sentence-bert-embedding-optimizer.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/sentence-bert-embedding-optimizer.ipynb)|sentence-bert를 가지고 유사도 측정하는 예제|**최적화 option 설정 추가**|
|[sentence-bert-embedding-by-bert.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/sentence-bert-embedding-by-bert.ipynb)|BERT 모델을 Sentence Bert로 만들고(훈련은 안시킴) 유사도 측정하는 예제|**BERT 모델** 이용|
|[sentence-bert-clustering.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/sentence-bert-clustering.ipynb)|sentence-bert를 가지고 클러스터링 하는 예제|**Sentence Bert 모델** 이용|

### 3. FAISS(Facebook AI Similarity Search) 예제

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[sbert-Faiss-embedding.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/faiss/sbert-Faiss-embedding.ipynb)|FAISS를 이용한 Sementic Search 예제 |**Sentence Bert 모델** 이용|
|[sbert-Faiss-embedding2.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/faiss/sbert-Faiss-embedding2.ipynb)|FAISS를 이용한 Sementic Search 예제+데이터 추가 예제|**Sentence Bert 모델** 이용|

### FAISS 란?
-Faiss는 facebook에서 만든 vector 유사도를 측정하는 라이브러리로, 기존 numpy 나 scikit-learn 에서 제공하는 cosine similarity 보다 강력하며, GPU도 지원한다.
- Documente는 [여기](https://faiss.ai/) , github 소스는 [여기](https://github.com/facebookresearch/faiss) 참조
- 설치
```
!conda install -c conda-forge faiss-gpu
```
- instance index 생성
```
import faiss
index = faiss.IndexFlatL2(embeddings.shape[1])
```
- id를 매핑
```
index = faiss.IndexIDMap(index)
index.add_with_ids(embeddings, df.번호.values)
```
- 유사도 비교
```
distance, idx = index.search(np.array([embeddings[1]]), k=10)
print(distance)
print(idx)
```
### 4. 기타
- [embedding_viewer.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/embedding_viewer.ipynb): 단어 embedding들을 3D 화면으로 보여주는 예제
1. 단어들은 meta.tsv 파일로 저장, 임베딩값들은 vecs.tsv 파일로 저장(**이때 임베딩 각 값들은 탭으로 띄어야 함**)
2. 이후 https://projector.tensorflow.org 접속하여, [load] 버튼 클릭->[Choose file] 버튼 클릭하여, vecs.tsv, meta.tsv 파일 선택 하면 완료

![image](https://user-images.githubusercontent.com/93692701/165455476-477d39cc-a401-4495-b3f4-e95b60ca70b3.png)

