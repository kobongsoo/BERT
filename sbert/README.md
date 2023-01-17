# Sentence Bert <img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white"/><img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
- SentenceTransformers는 최첨단 문장, 텍스트 및 이미지 임베딩을 위한 Python 프레임워크로, 이를 이용하여 Sentence Bert 모델을 만들고 훈련할수 있음
- 자세한 내용은 [sbert.net 사이트](https://www.sbert.net/) 참고 바람
- 테스트는 추가 학습한 [sentencebert 모델](https://huggingface.co/bongsoo/sentencebert_v1.0)을 통해 테스트 해볼수 있음 
 ```
# sentenceTransformers 라이브러리 설치
pip install -U sentence-transformers
```
- sentence모델 불러올때, 기본은 GPU를 사용함. 따라서 만약 CPU를 사용하고 싶다면, 아래처럼 **device='cpu'** 해줘야 함.
```
from sentence_transformers import SentenceTransformer, util
embedder = SentenceTransformer(model_path, device='cpu')
```
## 1. Sentence Bert(이하: S-BERT)
- 기존  BERT 모델을 가지고, Bi-Encoder 방식으로 훈련하여 제작된 모델로써,  semantic 응용 분야에 있어서, **기존 BERT보다 성능과 속도가 매우 향상된 BERT 모델임**.
- 응용 분야 : semantic textual similar, semantic search,  text clustering, semantic classification, paraphrase mining 등


## 2. Bi-Encoder vs. Cross-Encoder
![image](https://user-images.githubusercontent.com/93692701/164613754-d475f55a-b2b6-4ce2-bc93-50d30e29b392.png)

### 1. Bi-Encoder
- Bi-Encoder **2개의 문장 A와 B를 각각 BERT에 전달하여 문장 임베딩 u와 v를 생성하고, 이를 코사인 유사도를 사용하여 비교 함**.
- 장점 : 문장이 많더라도 **처리 속도가 빠름**(예로 10,000개 문장을 클러스터링 할때 5초면됨)
- 단점 : **Cross-Encoder에 비해 정확도가 떨어짐**
- 예제 : [STS 훈련 예](https://github.com/kobongsoo/BERT/blob/master/sbert/sentece-bert-sts.ipynb), [NLI 훈련 예](https://github.com/kobongsoo/BERT/blob/master/sbert/sentence-bert-nli.ipynb), [평가 예](https://github.com/kobongsoo/BERT/blob/master/sbert/sbert-test.ipynb)

### 2. Cross-Encoder
- Cross-Encoder는 **2개의 문장을 같이 1개의 문장으로 조합해서 BERT에 전달하고, 입력 문장 쌍의 유사성을 나타내는 0과 1 사이의 값을 출력함**.(NLI 모델과 같음)
- Cross-Encoder는 문장 임베딩을 생성하지 않고, 1개의 문장만 Cross-Encoder에 전달할 수 있음
- 장점 : **Bi-Encoder 방식 보다 정확도가 높음**
- 단점 : 문장이 많으면 **처리 속도가 엄청 느림**(예로 10,000개 문장을 클러스터링 하려면 10,000개 문장쌍인 약 5천만개 문장을 계산해야 함(약 60시간 걸림))
- 주의 : **NLI 모델->STS 모델 혹은 STS 모델->NLI 모델로 훈련시 에러 나므로, 기존 STS/NLI 모델을 아래처럼 기본 bert모델로 만들고 훈련**시켜야 함.
```
from transformers import BertModel, BertTokenizer, DistilBertModel, DistilBertTokenizer, AlbertModel, AlbertTokenizer

tokenizer = BertTokenizer.from_pretrained(model_path, do_lower_case=True, keep_accent=False)
bertmodel = BerttModel.from_pretrained(model_path)
OUTPATH = model_save_path + "/bertmodel"
os.makedirs(OUTPATH, exist_ok=True)
bertmodel.save_pretrained(OUTPATH)
tokenizer.save_pretrained(OUTPATH)
```
- 예제 : [STS 훈련 예](https://github.com/kobongsoo/BERT/blob/master/sbert/cross-encoder/sbert-corossencoder-train-sts.ipynb), [NLI 훈련 예](https://github.com/kobongsoo/BERT/blob/master/sbert/cross-encoder/sbert-corossencoder-train-sts.ipynb), [평가 예](https://github.com/kobongsoo/BERT/blob/master/sbert/cross-encoder/sbert-crossencoder-test3.ipynb)

### 3. Bi-Encder + Corss-Encoder 조합 모델
- 수십만개 문장을 검색하는 모델에 있다면..먼저 **Bi-Encoder 방식으로 100개 정도 가장 유사한 문장들을 검색**한 후, **100개의 문장에 대해 다시 Cross-Encoder를 이용하여 정확도를 측정**하여, 가장 정확한 순서대로 검색 UI에 보여줌



## 3. S-BERT 강화하기(Augmented SBERT)
- S-BERT 훈련을 위해서는 **STS 데이터셋(Semantic Textual Semilarity: 두 문장간 유사도 점수매긴 dataset) 이 많아야 한다**. 하지만 이런 **STS dataset을 일일이 만드는 것은 비용과 시간이 많이 든다**.
- 따라서 [Augmented SBERT](https://towardsdatascience.com/advance-nlp-model-via-transferring-knowledge-from-cross-encoders-to-bi-encoders-3e0fc564f554)는 이런 **STS dataset이 없거나, 적은 경우, 효과적으로 훈련하여 성능을 높이는 방식**에 대해 설명한다.
- STS 데이터셋에 대해 평가 함수는 BI-Encoder는 [EmbeddingSimilarityEvaluator](https://www.sbert.net/docs/package_reference/evaluation.html?highlight=embeddingsimilarityevaluator#) 사용 하고, Cross-Encoder는 [CECorrelationEvaluator](https://www.sbert.net/docs/package_reference/cross_encoder.html#evaluation) 를 사용 한다.

### 1. 도메인 문장쌍 STS dataset 이 없는 경우
#### ![image](https://user-images.githubusercontent.com/93692701/165041185-afc15c97-d85e-4ad4-ba67-4bc14a47f762.png)

- 1단계: **기존 korsts, kluests 등 sts dataset을 가지고,  Cross-Encoder로 BERT 훈련 시킴**
- 2.1단계: 기존 잘 훈련된 S-BERT(예: paraphrase-multilingual-mpnet-base-v2, distiluse-base-multilingual-cased-v2 등)를 이용해, **도메인 말뭉치 문장들에 대해 유사도 측정**해서, 한 문장에 대해 K수만큼 유사한 문장들을 조합하여 문장 쌍을 만듬
- 2.2단계: 1E단계에서 훈련된 BERT 로 2.1단계에서 만든 문장쌍들에 대해 점수를 매김->이를 **silver sts dataset**이라고 함
- 3단계: **기존 korst,kluests등 + silver sts dataset 을 훈련 데이터**로 하여 Bi-Encoder 훈련 시킴
- 예제: [도메인 STS dataset이 없는 경우](https://github.com/kobongsoo/BERT/blob/master/sbert/Augmented/sbert-no-dataset.ipynb)

### 2. 도메인 문장쌍 STS dataset 이 적은 경우
#### ![image](https://user-images.githubusercontent.com/93692701/165041141-1184b135-a532-4e7a-aac1-ddb3e591be08.png)
- 1단계: **적은 도메인 STS dataset(gold sts dataset) 에 대해 Cross-Encoder로 BERT 훈련 시킴**
- 2.1단계: 기존 잘 훈련된 S-BERT(예: paraphrase-multilingual-mpnet-base-v2, distiluse-base-multilingual-cased-v2 등)를 이용해, **gold sts 문장들에 대해 유사도 측정**해서, 한 문장에 대해 K수만큼 유사한 문장들을 조합하여 문장 쌍을 만듬
- 2.2단계: 1E단계에서 훈련된 BERT 로 2.1단계에서 만든 문장쌍들에 대해 점수를 매김->이를 **silver sts dataset**이라고 함
- 3단계: **gold sts dataset + silver sts dataset 을 훈련 데이터**로 하여 Bi-Encoder 훈련 시킴
- 예제: [도메인 STS dataset이 적은 경우](https://github.com/kobongsoo/BERT/blob/master/sbert/Augmented/sbert-limited-dataset.ipynb)

## 4. S-BERT 지식 증류 학습
![image](https://user-images.githubusercontent.com/93692701/175485631-ab223288-b99d-4179-8497-73b860f3847b.png)
<br> 참고 : https://sbert.net/examples/training/multilingual/README.html

### 1. 다국어 모델 증류 
- 교사모델은 **paraphrase-multilingual-mpnet-base-v2 혹은 distiluse-base-multilingual-cased-v2 둘중 하나 선택**, 학생모델은 제작한 S-BERT 모델로 설정 하여 학습시킴.<br>
자체 테스트시, 위 2개의 모델이 가장 성능이 좋았음(*아래표 참조)

 다운로드 : [paraphrase-multilingual-mpnet-base-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-mpnet-base-v2)
,[distiluse-base-multilingual-cased-v2](https://huggingface.co/sentence-transformers/distiluse-base-multilingual-cased-v2)
 
- **교사모델과 학생모델의 word_embedding_dimension(예: Dim=768)은 반드시 같아야함. 다르면 훈련시,'The size of tensor a (768) must match the size of tensor b (384) at non-singleton dimension 1' 에러 발생함**
- 이때 말뭉치는 **영어-한글 쌍으로 이루어진 말뭉치**를 이용함(예: [news_talk_en_ko](https://huggingface.co/datasets/bongsoo/news_talk_en_ko), TED2020-en-ko-train.tsv)
- 아래 표는 [S-BERT Pretrain 모델들](https://www.sbert.net/docs/pretrained_models.html)에 대해 영어-한글 쌍 말뭉치(TED2020-en-ko-train.tsv) 로 학습 후, korsts, klue-sts 로 평가해본 결과임

|교사모델명(S-BERT)|설명|korsts|Klue-sts|korsts+Klue-sts 평균|기존성능평가|
|:-------------:|:---------------------------|:-----:|:-----:|:-----:|:-----------------------------|
|all-mpnet-base-v2|base 모델: microsoft/mpnet-base, size:420MB, max_seq_len: 384|74.2%|74.7%|74.7%|embedding:69.57%, search:57.0%,GPU Speed(sentence/sec):2,800|
|multi-qa-distilbert-cos-v1|base 모델: distill-base, size:250MB, max_seq_len: 512|73.2%|73.4%|73.3%|embedding:69.98%, search:52.83%,GPU Speed:4,000|
|paraphrase-multilingual-mpnet-base-v2|교사/학생 모델: paraphrase-mpnet-base2/xlm-reberta-base, size:970MB, max_seq_len: 128, +50개 추가 언어 지원(한국어포함)|78.8%|78.2%|78.5%|embedding:65.83%, search:41.68%,GPU Speed:2,500|
|distiluse-base-multilingual-cased-v1|교사/학생 모델: mUSE/distilbert-base-multilingual, size:480MB, max_seq_len: 128, +15개 언어 지원(한국어포함)|74.2%|80.1%|77.15%|embedding:61.3%, search:29.87%,GPU Speed:4,000|
|distiluse-base-multilingual-cased-v2|교사/학생 모델: mUSE/distilbert-base-multilingual, size:480MB, max_seq_len: 128, +50개 추가 언어 지원(한국어포함)|75.0%|80.5%|77.75%|embedding:60.18%, search:27.35%,GPU Speed:4,000|

  ex) [sbert-distillation.ipynb](https://github.com/kobongsoo/BERT/blob/master/sbert/sbert-distillaton.ipynb)

### 2. 한국어 모델 증류 
- 여기서는 기존 학습잘 된 한국어 모델(교사모델)을 이용해서 작은 사이즈에 모델(학생모델)에 한국어를 증류하는 방식으로, 위 증류 방법을 참고 하여 증류 해봄
- 교사모델로는 [kpf-sbert-v1.1](https://huggingface.co/bongsoo/kpf-sbert-v1.1), 학생모델은 [albert-small-kor-v1](https://huggingface.co/bongsoo/albert-small-kor-v1) 이용
- 말뭉치는 **한국어-영어 쌍으로 이루어진 말뭉치**를 이용([news_talk_ko_en](https://huggingface.co/datasets/bongsoo/news_talk_ko_en))
- 아래표는 위 방식대로 제작된 [albert-small-kor-sbert-v1.1](https://huggingface.co/bongsoo/albert-small-kor-sbert-v1.1) 모델에 대해 다른 모델과  평가 비교해본 결과

|모델     |korsts|klue-sts|glue(stsb)|stsb_multi_mt(en)|
|:--------|------:|--------:|--------------:|------------:|
|distiluse-base-multilingual-cased-v2   |0.7475    |0.7855    |0.8193           |0.8075|
|paraphrase-multilingual-mpnet-base-v2  |0.8201    |0.7993    |0.8907           |0.8682|
|bongsoo/albert-small-kor-sbert-v1      |0.8305    |0.8588    |0.8419           |0.7965|
|bongsoo/kpf-sbert-v1.1                 |0.8750    |0.8900    |0.8863           |0.8554|
|bongsoo/albert-small-kor-sbert-v1.1    |0.8526    |0.8833    |0.8484           |0.8286|
