# P-Tuning
## 개요
- prompt learning 한 방식으로, Fine-tuning 처럼 모델이 모든 파라메터를 업데이트 하지 않고, 모델이 일부 파라메터만 업데이트 하는 방식중 하나임.
- 원래 처음 GPT 계열의 단점이 NLU 테스크에서 성능이 떨어지고, 좋은 NLU 성능을 내기 위해서는 in context learning(few-shout learning) 하기 위해서 최적의
prompt 조합을 찾는게 쉽지 않다는 문제가 있다.
- 따라서 여기서 말하는 p-tuning은 이 최적의 prompt 조합을 찾는데, 기존 discreate space(분리된 공간) 에서 벗어나, 
continuous space(연속된 공간)에 prompt가 존재하도록 하는 방법이다.
- 아래는 prompt가 조금만 바뀌어도 큰 성능 차이를 보이는 예시임.
![image](https://user-images.githubusercontent.com/93692701/178618230-f1d95ec1-1a4e-474e-9660-3016b85c3b8e.png)
- p-tuning은 2021년 [GPT Understands, Too 논문](https://arxiv.org/pdf/2103.10385.pdf) 에서 처음 제시 되었고, 
이후 [p-tuning-v2](https://github.com/THUDM/P-tuning-v2) 방식도 제안 되었다.


### prefix-tuning
- GPT-2, T5등 LM에서 접두사 prompt를 추가하여 훈련시키는 방식.

### P-tuning
- P-tuning은 prefix-tuning과 같은데, 좀더 개선된 방식으로, 접두사(시작할때)에만 토큰을 삽입하는게 아니라, 중간에도 토큰을 삽입하는 방식.
![image](https://user-images.githubusercontent.com/93692701/178617025-0c87e02c-5f00-4e64-b57d-0a601f52d2f0.png)

### P-tuning-v2
- P-tunin-v2는 새로운 방식이 아니라, NLU(Natual Language Understanding) 향상을 위해 LM 모델(GTP, T5등)뿐만 아니라, MLM 모델(BERT)에도 prefix-tuning을 적용한 방식.
![image](https://user-images.githubusercontent.com/93692701/178617332-95bd50c6-35a1-4a22-9987-fb4a20a14d80.png)

출처 : https://github.com/THUDM/P-tuning / https://github.com/THUDM/P-tuning-v2

## 테스트
- P-tuning-v2의 prefix-tuning 방식으로 BERT-based-multilingual-cased 모델의 NLI(Natual Language Inference:자연어추론) task에 대해 성능 테스트를 해봄.
- prefix_projection=True로 해서, 2-layer MLP 사용함.(Multi-layer perceptron(다중퍼셉트론)). 
  <br> prefix_projection=False일때는 embedding layer만 사용하는데, 이때 성능은 엄청 떨어짐
  ```
  # prefix_projection=True 일때, 2-layer MLP 구조
  
  (prefix_encoder): PrefixEncoder(
    (embedding): Embedding(20, 768)
    (trans): Sequential(
      (0): Linear(in_features=768, out_features=512, bias=True)
      (1): Tanh()
      (2): Linear(in_features=512, out_features=18432, bias=True)
    )
  )
  ```
- prefix_hidden_size=512로 고정함. 테스트시 768로 늘려도 큰 차이(0.004) 정도 향상이 있었음.
- 테스트는 prefix 사이즈를 20, 100, 200 으로 조정하면서 테스트 해봄. 

|소스명                    |설명                          | 기타              |
|:-------------------------|:-----------------------------|:------------------|
|[bert-p-tuningv2-pefix-nli](https://github.com/kobongsoo/BERT/blob/master/p-tuning/bert-p-tuningv2-pefix-nli.ipynb)|P-TUNING NLI 훈련 예제||
|[bert-p-tuningv2-prefix-nli-test](https://github.com/kobongsoo/BERT/blob/master/p-tuning/bert-p-tuningv2-prefix-nli-test.ipynb)|P-TUNING NLI 테스트 예제||


참고 소스 : https://github.com/THUDM/P-tuning-v2

### Hyperparameter
- epoch : 50
- batch_size: 32
- lr: 3e-5
- max_seq_len : 128
- 말뭉치 : klue-nli-v1.1_train.json(훈련), klue-nli-v1.1_dev.json(평가)

|방식                 |prefix 크기|prefix_hidden_size|prefix_projection|ACC            |훈련속도/1epoch(초) | 훈련시 GPU 사용량(MIB)  |
|:--------------------|----------:|:-----------------|:----------------|--------------:|-------------------:|-----------------------:|
|훈련없음(org)        |x          |x                 |x                |0.338          |x                   |x                     |
|Fine-tuning          |x          |x                 |x                |**0.743**      |**110**             |**8,194**             |
|P-tuning-v2(prefix)  | 20        |512               |False            |0.531          |50                  |5,374                 |
|P-tuning-v2(prefix)  |**20**     |512               |**True**         |**0.692**      |**60**              |**5,507**             |
|P-tuning-v2(prefix)  | 100       |512               |False            |0.548          |73                   |6,411                |
|P-tuning-v2(prefix)  |**100**    |512               |**True**         |**0.695**      |**77**               |**6,546**            |
|P-tuning-v2(prefix)  | 200       |512               |True             |0.694          |93                   |7,691                |
|P-tuning-v2(prefix)  | 200       |**768**           |True             |0.698          |95                   |7,791                |

### 결론
- P-tuning-v2 **prefix 크기를 20으로 할때, Fine-tuning 보다는 성능 5%정도 떨어지지만, 훈련속도 및 GPU 사용량에서는 약 40% 정도 향상이 있음.**
- prefix 크기는 100일때 가장 성능이 좋고, prefix_hidden_size는 768로 하더라도 0.5%정도 미미한 성능 향상이 있음.
