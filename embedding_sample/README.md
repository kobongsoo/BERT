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

#### Sentence Bert 최적화
<br> 검색 처럼 몇천만개 이상 데이터에서 임베딩 값을 구하고 비교할때 널리 사용되는 최적화 기술에는 아래 2가지 방식(임베딩 정규화, 내적 계산)이 있다.
<br> 출처 : https://towardsdatascience.com/multilingual-text-similarity-matching-using-embedding-f79037459bf2

- **임베딩 정규화**
<br> 임베딩 정규화 화면 출력벡터이 길이가 1이 된다.
```
# normalize_embedding = True 설정
corpus_embedding = model.encode(corpus, convert_to_tensor=True, normalize_embeddings =True)
```
또는
```
# util.normalize_embeddings기존 임베딩을 정규화
corpus_embedding = model.encode(corpus, convert_to_tensor=True) 
corpus_embedding = util.normalize_embeddings(corpus_embedding)
```
- **내적 계산**

```
# util.semantic_search 함수 사용
hits = util.semantic_search(query_embedding, corpus_embedding, score_function=util.dot_score)
```

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
# Cosine Similarity 사용인 경우 IndexFlatIP 사용
import faiss
index = faiss.IndexFlatIP(embeddings.shape[1]) # 768 차원 설정=> 유사한 문장(단어)들은 1에 가까움
Faiss.normalize_L2(embeddings) # vector를 add하기 전에 **normalize_L2** 해줘야 함(평활화 처리) 
```
```
# Euclidean Distance 사용인 경우 IndexFlatL2 사용 => 유사한 문장(단어)들은 거리가 0에 가까움
import faiss
index = faiss.IndexFlatL2(embeddings.shape[1]) # 768 차원 설정
```
- id를 매핑
```
index = faiss.IndexIDMap(index)
index.add_with_ids(embeddings, df.번호.values)
```
- 유사도 비교
- Cosine Similarity 사용을 위해 **IndexFlatIP 로 인덱스 만든 경우에는 쿼리문 벡터도 평활화 처리(normalize_L2)** 해줘야함
```
Faiss.normalize_L2(embeddings) # **Cosine Similarity 사용인 경우에만 벡터 평활화 처리(normalize_L2) 함

# Cosine Similarity 인 경우에는 distance가 MAX인게 가장 유사한 벡터임.(distance가 max 순으로 출력됨=[0.9, 0.7, 0.6])
# Euclidean Distance 사용인 경우 경우에는 distance가 MIN인게 가장 유사한 벡터임(distance가 min 순으로 출력됨=[0.6, 0.7, 0.9])
distance, idx = index.search(np.array([embeddings[1]]), k=10)
print(distance)
print(idx)
```
- 저장 및 불러오기
```
# 저장
faiss.write_index(index, "test.index")
```
```
# 불러오기
index2 = faiss.read_index("test.index")
```
### 4. 검색 모델 측정
- 검색 모델 성능을 측정하는 방식에는 word2vec 이용할때는 TF-IDF, **BM25(엘라스틱서치)** 등이 있다.
```
# bm25 pip 설치
pip install rank_bm25
```

- 문장 임베딩을 이용할때 **MRR(Mean Reciprocal Rank)**, MAP, MDCG 방식등의 있다.

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[bm25-test](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/faiss/bm25-test.ipynb)|BM25 샘플 예제||
|[mrr-test](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/faiss/mrr-test.ipynb)|MRR 샘플 예제||
|[sbert-Faiss-MRR-embdding](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/faiss/sbert-Faiss-MRR-embdding-test.ipynb)|korquad-V1.0 및 aihub에 QuA 말뭉치와 Faiss 이용한 MRR 및 BM25 측정 예제|**SBERT와 Cross-encoder 이용**, 말뭉치는 data 폴더에 있음|
|[sbert-Faiss-MRR-vocab-embedding](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/faiss/sbert-Faiss-MRR-vocab-embedding-test.ipynb)|문서에 여러문장들의 단어들에 대해 임베딩 후 Faiss 인덱스를 만들어서 단어별 비교해 검색하는 예시|**SBERT이용. Colbert 검색 방식과 동일. 엘라스틱서치에 적용 어려움**, 말뭉치는 data 폴더에 있음|

![image](https://user-images.githubusercontent.com/93692701/216910548-4d55e6ca-5fdc-4ee4-b92f-89390d71b668.png)

1. 만약 당신이 우선순위(rank)가 없는 IR(정보검색: Information Retrieval) 을 사용한다면 정밀도와 재현율을 같이 사용해보도록 하자. IR에서 선정해준 컨텐츠가 얼마나 관련이 있는지, 관련성 있는 컨텐츠를 놓치지 않고 있는지 평가해줄 것이다.
2. 만약 당신이 추천 시스템과 같이 우선순위가 중요한 IR을 사용한다면 MRR, MAP, NDCG를 고려해보자.
3. 사용자가 잘 알만한 컨텐츠를 추천하고 추천하는 첫 번째 관련 컨텐츠가 중요하다면 MRR을 사용해보자.
4. 추천 컨텐츠의 관련도를 이분법으로 판단할 수 있고, 추천 컨텐츠의 노출 위치가 중요하다면 MAP을 사용해보자.
5. 추천 컨텐츠의 관련도를 여러 가지 값으로 표현할 수 있고, 관련도에 따른 가중치 조정을 하고 싶다면 NDCG을 사용해보자.
</br> 출처 : https://lamttic.github.io/2020/03/20/01.html

###  기타
- [embedding_viewer.ipynb](https://github.com/kobongsoo/BERT/blob/master/embedding_sample/embedding_viewer.ipynb): 단어 embedding들을 3D 화면으로 보여주는 예제
1. 단어들은 meta.tsv 파일로 저장, 임베딩값들은 vecs.tsv 파일로 저장(**이때 임베딩 각 값들은 탭으로 띄어야 함**)
2. 이후 https://projector.tensorflow.org 접속하여, [load] 버튼 클릭->[Choose file] 버튼 클릭하여, vecs.tsv, meta.tsv 파일 선택 하면 완료

![image](https://user-images.githubusercontent.com/93692701/165455476-477d39cc-a401-4495-b3f4-e95b60ca70b3.png)

