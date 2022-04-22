## Senetence Bert
- SentenceTransformers는 최첨단 문장, 텍스트 및 이미지 임베딩을 위한 Python 프레임워크로, 이를 이용하여 Sentence Bert 모델을 만들고 훈련할수 있음
- 자세한 내용은 [sbert.net 사이트](https://www.sbert.net/) 참고 바람
 ```
# sentenceTransformers 라이브러리 설치
pip install -U sentence-transformers
```
### 1. Sentence Bert(이하: S-BERT)
- 기존 사전 훈련된 BERT 모델을 가지고, Bi-Encoder 방식으로 훈련한 모델로, semantic 분야에 BERT보다 매우 높은 성능을 보인다.
- 적용범위 : semantic textual similar, semantic search,  semantic classification, paraphrase mining 등

### 2. Bi-Encoder vs. Cross-Encoder


