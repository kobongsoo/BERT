## Pruning(가지치기)
### 1. 개요

- 모델이 파라메터 수를 줄이는 방법 중 하나 (다른 방법으로, [양자화](https://github.com/kobongsoo/BERT/tree/master/Quantization), [Distillation](https://github.com/kobongsoo/BERT/tree/master/distilbert) 등이 있다)
- 뉴런간에 쓸모없는 연결을 끊어서, 모델이 훈련과 경량화에 효율적으로 적용할수 있도록 하는 방법
- 가중치 값이 L1, L2 노름을 기준으로 뉴런의 중요도에 따라, 낮은 중요도를 갖는 뉴런이 가중치를 0(제로)로 함으로써, 훈련 및 추론속도를 높인다.
- Pytorch에 **nn.utils.prune** 모듈을 이용한다.
- 로컬 Pruning 과 글로벌 Pruning 이 있는데, 글로벌 Pruning를 보통 사용 함.(아래 예제 참조)
 
![image](https://user-images.githubusercontent.com/93692701/171798008-5c8423c0-cfac-4e31-bb12-b91d2e23cd6d.png)


참고 
<br>https://huffon.github.io/2020/03/15/torch-pruning/
<br>https://github.com/Huffon/nlp-various-tutorials/blob/master/pruning-bert.ipynb

### 2 .코드
- 테스트시 추론 속도와 용량은 얼마 줄지 않았음.(많은 테스트 필요)

|소스      | 설명          | 기타  |
|:---------|:--------------|-------|
|[local_pruning1](https://github.com/kobongsoo/BERT/blob/master/pruning/local_pruning1.ipynb)| 로컬 Puring 예제||
|[local_pruning2](https://github.com/kobongsoo/BERT/blob/master/pruning/local_pruning2.ipynb)| 로컬 Puring 예제||
|[global_pruning](https://github.com/kobongsoo/BERT/blob/master/pruning/global_pruning.ipynb)| 글로벌 Puring 예제||

- 모듈 별로 Pruning 하므로, 전체 모델이 구조를 보고 Pruning 할 모듈을 설정해야 함
```
# 모델 구조에서 pruning 할 모듈들만 지정해서 처리함
# => ****모델 구조에 맞게 모듈들을 재정의 해야 함.

# 튜플 자료형
parameters_to_prune = (
    (model.distilbert.embeddings.word_embeddings, "weight"),                  # embeddings 모듈에는 bias는 없음
                      ) 

for i in range(encoder_layer_num):
    parameters_to_prune += (
        (model.distilbert.transformer.layer[i].attention.q_lin, "weight"),     # attention.self.key 모듈
        (model.distilbert.transformer.layer[i].attention.k_lin, "weight"),   # attention.self.query 모듈
        (model.distilbert.transformer.layer[i].attention.v_lin, "weight"),   # attention.self.value 모듈
          
        (model.distilbert.transformer.layer[i].attention.q_lin, "bias"),     # attention.self.key 모듈
        (model.distilbert.transformer.layer[i].attention.k_lin, "bias"),   # attention.self.query 모듈
        (model.distilbert.transformer.layer[i].attention.v_lin, "bias"),   # attention.self.value 모듈
    )
```
- 글로벌 Pruning 시작 
```
# global_unstructured 로 적용
prune.global_unstructured(
    parameters_to_prune,
    pruning_method=prune.L1Unstructured,
    amount=0.2
```

- 영구 적용
```
prune.remove(model.distilbert.embeddings.word_embeddings, "weight")

for i in range(encoder_layer_num):
    prune.remove(model.distilbert.transformer.layer[i].attention.q_lin, "weight")     # attention.self.key 모듈
    prune.remove(model.distilbert.transformer.layer[i].attention.k_lin, "weight")   # attention.self.query 모듈
    prune.remove(model.distilbert.transformer.layer[i].attention.v_lin, "weight")   # attention.self.value 모듈
           
    prune.remove(model.distilbert.transformer.layer[i].attention.q_lin, "bias")     # attention.self.key 모듈
    prune.remove(model.distilbert.transformer.layer[i].attention.k_lin, "bias")   # attention.self.query 모듈
    prune.remove(model.distilbert.transformer.layer[i].attention.v_lin, "bias")   # attention.self.value 모듈
   
```

