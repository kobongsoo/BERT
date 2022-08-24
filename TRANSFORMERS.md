# Transformers
## 1) 개요
- 2017년 구글이 발표한 논문 "**Attention is all you need**" 에서 제시한 모델
- 기존 NLP(자연어 처리) 분야에 사용되던 **인코더-디코더 구조**를 따르면서도, **RNN 레이어를 사용하지 않고**, 엄청 우수한 번역 성능을 보여준 모델임.
- 기존 RNN, LSTM 모델은 인코더에서 정보를 압축하여 디코더에 보낼때, 정보 손실이 있는데, 이를 Transfomer는 Attention 이라는 메커니즘으로 정보 손실을 줄였음.

![image](https://user-images.githubusercontent.com/93692701/171075193-ba6ffe3c-124e-4752-9b54-78b4b14fa8f3.png)
![image](https://user-images.githubusercontent.com/93692701/171075615-14ab5a66-1c7a-4379-b025-2514217902e4.png)

## 2) 장점
- 병렬 프로세싱 처리에 최적화 되도록 설계되어, GPU 환경에서 대량의 데이터셋을 가지고 훈련 가능 함.
- 대량이 데이터 셋은 기존처럼 라벨링된 데이터 셋이 아니라서, 라벨링 하는데 전문인력과 시간이 필요 없음.
- Pre-Training 된 모델을 가지고 task에 맞게 Fine-Tuning 해서 성능 높은 NLP 모델을 손쉽게 만들수 있음.

## 3) 단점
- 요즘 파생된 모델들은, 점점더 모델 SIZE가 커지고 있어서, 웬만한 H/W 로는 훈련 및 추론 불가.
- GPT-2 : 800만개 데이터 셋, 15억개 파라메터
- GTP-3 : 3,000억개 데이터 셋, 1,750억개 파라메터, 
  <br> - 훈련비용 : 50억~150억
  <br> - 훈련 H/W : 이론적으로 32GB GPU에서 355년 걸림
  <br> - 추론 H/W : 대략 적절한 추론을 하려면 총 350GB 메모리가 필요하므로, 32G GPU 11개 필요
![image](https://user-images.githubusercontent.com/93692701/171076762-d4cbf62b-705c-4ef5-86c2-68a30e042562.png)


## 4) 구조

|구분|내용|
|:--------|:---------------|
|임베딩벡터|512|
|인코더/디코더 레이더|6개|
|멀티 헤더 어텐션 수|8개|
|피드포워드 네트워크 입출력 크기|2048|
![image](https://user-images.githubusercontent.com/93692701/171071032-90593545-8842-463e-bedd-8ee3100df88d.png)
![image](https://user-images.githubusercontent.com/93692701/171070996-b2b1d648-42b0-4ebd-8cd0-0fc7b7120694.png)
![image](https://user-images.githubusercontent.com/93692701/171071078-06adff18-85ea-4002-8b92-03c382a7c074.png)

출처 : https://wikidocs.net/31379

***
