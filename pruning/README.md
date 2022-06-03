## Pruning(가지치기)
- 모델이 파라메터 수를 줄이는 방법 중 하나 (다른 방법으로, [양자화](https://github.com/kobongsoo/BERT/tree/master/Quantization), [Distillation](https://github.com/kobongsoo/BERT/tree/master/distilbert) 등이 있다)
- 뉴런간에 쓸모없는 연결을 끊어서, 모델이 훈련과 경량화에 효율적으로 적용할수 있도록 하는 방법
- 일반적으로 가중치 값이 L1, L2 노름을 기준으로 뉴런의 중요도에 따라, 낮은 중요도를 갖는 뉴런이 가중치를 0(제로)로 함으로써, 훈련 및 추론속도를 높인다.
- Pytorch에 **nn.utils.prune** 모듈을 이용한다.

![image](https://user-images.githubusercontent.com/93692701/171798008-5c8423c0-cfac-4e31-bb12-b91d2e23cd6d.png)


참고 : https://huffon.github.io/2020/03/15/torch-pruning/
