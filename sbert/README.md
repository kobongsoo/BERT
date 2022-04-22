## Senetence Bert <img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white"/><img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
- SentenceTransformers는 최첨단 문장, 텍스트 및 이미지 임베딩을 위한 Python 프레임워크로, 이를 이용하여 Sentence Bert 모델을 만들고 훈련할수 있음
- 자세한 내용은 [sbert.net 사이트](https://www.sbert.net/) 참고 바람
 ```
# sentenceTransformers 라이브러리 설치
pip install -U sentence-transformers
```
### 1. Sentence Bert(이하: S-BERT)
- 기존  BERT 모델을 가지고, Bi-Encoder 혹은 Cross-Encoder 방식으로 훈련하여 제작된 모델로써,  semantic 응용 분야에 있어서, **기존 BERT보다 성능과 속도가 매우 향상된 BERT 모델임**.
- 응용 분야 : semantic textual similar, semantic search,  text clustering, semantic classification, paraphrase mining 등

### 2. Bi-Encoder vs. Cross-Encoder
![image](https://user-images.githubusercontent.com/93692701/164613754-d475f55a-b2b6-4ce2-bc93-50d30e29b392.png)

#### 2.1. Bi-Encoder
- Bi-Encoder **2개의 문장 A와 B를 각각 BERT에 전달하여 문장 임베딩 u와 v를 생성하고, 이를 코사인 유사도를 사용하여 비교 함**.
- 장점 : 문장이 많더라도 **처리 속도가 빠름**(예로 10,000개 문장을 클러스터링 할때 5초면됨)
- 단점 : **Cross-Encoder에 비해 정확도가 떨어짐**
- 예제 : [STS 훈련 예](https://github.com/kobongsoo/BERT/blob/master/sbert/sentece-bert-sts.ipynb), [NLI 훈련 예](https://github.com/kobongsoo/BERT/blob/master/sbert/sentence-bert-nli.ipynb), [평가 예](https://github.com/kobongsoo/BERT/blob/master/sbert/sbert-test.ipynb)

#### 2.2. Cross-Encoder
- Cross-Encoder는 **2개의 문장을 같이 1개의 문장으로 조합해서 BERT에 전달하고, 입력 문장 쌍의 유사성을 나타내는 0과 1 사이의 값을 출력함**.(NLI 모델과 같음)
- Cross-Encoder는 문장 임베딩을 생성하지 않고, 1개의 문장만 Cross-Encoder에 전달할 수 없음
- 장점 : **Bi-Encoder 방식 보다 정확도가 높음**
- 단점 : 문장이 많으면 **처리 속도가 엄청 느림**(예로 10,000개 문장을 클러스터링 하려면 10,000개 문장쌍인 약 5천만개 문장을 계산해야 함(약 60시간 걸림))
- 예제 : [STS 훈련 예](https://github.com/kobongsoo/BERT/blob/master/sbert/cross-encoder/sbert-corossencoder-train-sts.ipynb), [NLI 훈련 예](https://github.com/kobongsoo/BERT/blob/master/sbert/cross-encoder/sbert-corossencoder-train-sts.ipynb), [평가 예](https://github.com/kobongsoo/BERT/blob/master/sbert/cross-encoder/sbert-crossencoder-test.ipynb)

#### 3.3 Bi-Encder + Corss-Encoder 조합 모델
- 수십만개 문장을 검색하는 모델에 있다면..먼저 **Bi-Encoder 방식으로 100개 정도 가장 유사한 문장들을 검색**한 후, **100개의 문장에 대해 다시 Cross-Encoder를 이용하여 정확도를 측정**하여, 가장 정확한 순서대로 검색 UI에 보여줌
