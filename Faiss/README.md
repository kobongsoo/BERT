# FAISS 란?
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
- embedding 추가
```
index.add(embeddings)
```
- id를 매핑도 하면서 embedding 추가
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

## FAISS(Facebook AI Similarity Search) 예제

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[sbert-Faiss-embedding.ipynb](https://github.com/kobongsoo/BERT/blob/master/Faiss/sbert-Faiss-embedding.ipynb)|FAISS를 이용한 Sementic Search 예제 |**Sentence Bert 모델** 이용|
|[sbert-Faiss-embedding2.ipynb](https://github.com/kobongsoo/BERT/blob/master/Faiss/sbert-Faiss-embedding2.ipynb)|FAISS를 이용한 Sementic Search 예제+데이터 추가 예제|**Sentence Bert 모델** 이용|



## FAISS 훈련
- 벡터를 확보하고 나면, 이 벡터들을 training한다. 그 이유는 FAISS를 사용하기 위해서는 Clustering을 확보해야 한다.
- Clustering을 위해 어떤 벡터가 서로 유사한지 알아야 하고, 이를 위해 index training이 필요하다. 또한 Scalar Quantization(SQ)을 할 때(float32 to int8)도 float의 min, max값을 기반으로 scale, offset을 결정해야하므로 index training이 요구된다. 

![image](https://user-images.githubusercontent.com/93692701/218006362-fff61a31-b689-4825-88ee-b5c975d648e9.png)

- 이렇게 index training이 끝나고 Cluster와 SQ8을 확보하면, 이제 이 Cluster안에 SQ8의 형태로 index들을 넣어준다.
따라서 크게 Train index와 Add index로 나뉜다.

- 이렇게 FAISS index가 만들어지면, Inference단계에서 query가 들어오고 검색을 한 후 가장 가까운 cluster를 방문해서 cluster 내의 vector을 일일이 비교하여 top-k의 문서 벡터를 추출한다.

![image](https://user-images.githubusercontent.com/93692701/218006546-a8899c7b-2051-424e-8006-2e2ce3e34e8f.png)

- FAISS basic
</br> brute-force로 모든 쿼리와 벡터를 비교하는 단순한 인덱스 만들기
![image](https://user-images.githubusercontent.com/93692701/218006645-dd3cddf1-9631-48b4-97ae-72d50c5788ec.png)

- IVF with FAISS
</br>IVF 인덱스 만들기
</br>Clustering을 통해 가까운 Cluster내 벡터들만 비교하여 빠른 검색
</br>Cluster내에는 여전히 전체 벡터와 거리 비교 (Flat)

![image](https://user-images.githubusercontent.com/93692701/218005731-563e1b09-ab9c-4329-8a68-d5514a516f95.png)

- IVF-PQ with FAISS
</br>벡터 압축 기법(PQ) 활용
</br>전체 벡터를 저장하지 않고 압축된 벡터만 저장
</br>메모리 사용량 줄일 수 있음

![image](https://user-images.githubusercontent.com/93692701/218005934-1eb61c56-282f-4509-ab5f-790c6cdf1fae.png)

출처 : https://amber-chaeeunk.tistory.com/109

## 검색 모델 측정
- 검색 모델 성능을 측정하는 방식에는 word2vec 이용할때는 TF-IDF, **BM25(엘라스틱서치)** 등이 있다.
```
# bm25 pip 설치
pip install rank_bm25
```

- 문장 임베딩을 이용할때 **MRR(Mean Reciprocal Rank)**, MAP, MDCG 방식등의 있다.

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[bm25-test](https://github.com/kobongsoo/BERT/blob/master/Faiss/bm25-test.ipynb)|BM25 샘플 예제||
|[mrr-test](https://github.com/kobongsoo/BERT/blob/master/Faiss/mrr-test.ipynb)|MRR 샘플 예제||
|[sbert-Faiss-MRR-embdding](https://github.com/kobongsoo/BERT/blob/master/Faiss/sbert-Faiss-MRR-embdding-test.ipynb)|korquad-V1.0 및 aihub에 QuA 말뭉치와 Faiss 이용한 MRR 및 BM25 측정 예제|**SBERT와 Cross-encoder 이용**, 말뭉치는 data 폴더에 있음|
|[sbert-Faiss-MRR-vocab-embedding](https://github.com/kobongsoo/BERT/blob/master/Faiss/sbert-Faiss-MRR-vocab-embedding-test.ipynb)|문서에 여러문장들의 단어들에 대해 임베딩 후 Faiss 인덱스를 만들어서 단어별 비교해 검색하는 예시|**SBERT이용. Colbert 검색 방식과 동일. 엘라스틱서치에 적용 어려움**, 말뭉치는 data 폴더에 있음|

![image](https://user-images.githubusercontent.com/93692701/216910548-4d55e6ca-5fdc-4ee4-b92f-89390d71b668.png)

1. 만약 당신이 우선순위(rank)가 없는 IR(정보검색: Information Retrieval) 을 사용한다면 정밀도와 재현율을 같이 사용해보도록 하자. IR에서 선정해준 컨텐츠가 얼마나 관련이 있는지, 관련성 있는 컨텐츠를 놓치지 않고 있는지 평가해줄 것이다.
2. 만약 당신이 추천 시스템과 같이 우선순위가 중요한 IR을 사용한다면 MRR, MAP, NDCG를 고려해보자.
3. 사용자가 잘 알만한 컨텐츠를 추천하고 추천하는 첫 번째 관련 컨텐츠가 중요하다면 MRR을 사용해보자.
4. 추천 컨텐츠의 관련도를 이분법으로 판단할 수 있고, 추천 컨텐츠의 노출 위치가 중요하다면 MAP을 사용해보자.
5. 추천 컨텐츠의 관련도를 여러 가지 값으로 표현할 수 있고, 관련도에 따른 가중치 조정을 하고 싶다면 NDCG을 사용해보자.
</br> 출처 : https://lamttic.github.io/2020/03/20/01.html
