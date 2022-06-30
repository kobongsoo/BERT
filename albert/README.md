# Albert

## 1. 기존 모델 문제점
- Training speed (훈련속도) 저하, memory limitation ( GPU 메모리 한계)
<br>BERT base 인 경우 16개 V100(32G) GPU 사용시 ,5일 이상 소요.
<br>BERT large 인 경우 64개 V100(32G) GPU 사용시 ,8일 이상 소요.
<br> 참고 : https://timdettmers.com/2018/10/17/tpus-vs-gpus-for-transformers-bert/

## 2. ALBERT: A LITE BERT FOR SELF-SUPERVISED LEARNING OF LANGUAGE REPRESENTATIONS 
- 모델이 크기는 줄이고 성능은 높이기 위해 3가지 훈련 방식 사용함.
- 훈련시에는 **MLM(Masked Language Model) + SOP(Sentence Order Prediction)** 말뭉치로 훈련함.
<br> Batch size = 4096, 125,000 Steps 학습, 모델의 크기에 따라 TPUv3를 64~1024 chips 활용
<br> Wiki, Book Corpus - 16GB 학습 데이터, Layer 간 모든 Parameter 공유
- **SentencePiece** Tokenizer 사용

### ALBERT vs BERT

|모델|파라미터|레이어수|Hidden Layer 차원|임베딩 차원|
|:---|-------:|-------:|---------------:|----------:|
|BERT-base|110M|12|768|768|
|BERT-large|334M|24|1024|1024|
|Albert-base|12M|12|768|128|
|Albert-large|18M|24|1024|128|
|Albert-xlarge|60M|24|2048|128|
|Albert-xxlarge|235M|12|4096|128|

### 1. Factorized embedding layer parameterization (임베딩 벡터 파라메터 줄이기)
- 기존 임베딩 사이즈과 Hidden layer 사이즈는 동일(BERT인 경우 768) 하게 하지 않고, **임베딩 사이즈를 128**로 줄임
- 즉 기존 임베딩 V * H 를 V *E + E * H 로 맞추어 임베딩 사이즈를 줄임
  
![image](https://user-images.githubusercontent.com/93692701/172548603-884c8ca8-cf14-40a1-94c9-d805ba67a148.png)

### 2. Cross-layer parameter sharing (인코더 레이어 공유)
- 첫 번째 인코더 레이어의 변수만 학습한 다음, **첫 번째 인코더 레이어의 변수를 다른 모든 인코더 레이어와 공유**하는 방식(Universal Transformer에서도 레이어 공유 방식 사용함)
- 논문 실험결과 Self Attention Layer 만 공유 했을때는 성능이 떨어지지 않음. FFN(Feed Forward Network) 공유시에는 다소 떨어짐.
![image](https://user-images.githubusercontent.com/93692701/172551010-a204eaf8-dfd0-47fc-8134-be8c97efd353.png)

- 아래 그림처럼 Layer가 Recursive Transformer 형태로 동작한다고 할수 있음.

![image](https://user-images.githubusercontent.com/93692701/172562693-ea9bf420-1fe3-49b7-a3e6-bd067beed543.png)

### 3. Sentence Order Prediction(SOP)(문장 순서 훈련)
- 연속적인 두문장(positive)과 두문장의 순서를 앞뒤로 바꾼 문장(negative)으로 문장이 순서가 옳은지 예측 하는 학습 방식.
- 이진 분류로 sentence_order_label 이용함.
<br>햄버거를 만들었다. 맛있었다. => positive(0)
<br>맛있었다. 햄버거를 만들었다  => negative(1)

![image](https://user-images.githubusercontent.com/93692701/172563354-600e9c4b-376d-4415-94ee-96d5c7714cf7.png)

## 예제

|소스명|설명|기타|
|:-----------------|:-----------------------------------------------------------|:---------------------|
|[insert_vocab](https://github.com/kobongsoo/BERT/blob/master/albert/insert_vocab.ipynb)|albert-base-v2 토큰(sentenctpiece)에 신규 vocab을 추가하는 예||
|[albert-further-pretrain-mlm](https://github.com/kobongsoo/BERT/blob/master/albert/albert-further-pretrain-mlm.ipynb)|albert-base-v2에 MLM Further Pretrain 예||
|[albert-further-pretrain-sop-mlm](https://github.com/kobongsoo/BERT/blob/master/albert/albert-further-pretrain-sop-mlm.ipynb)|albert-base-v2에 MLM+SOP Further Pretrain 예||
|[albert-sts-to-sbert](https://github.com/kobongsoo/BERT/blob/master/albert/albert-sts-to-sbert.ipynb)|Albert를 sentenceBERT로 제작하는 예||
|[albert-model-create](https://github.com/kobongsoo/BERT/blob/master/albert/albert-model-create.ipynb)|빈껍데기albert 제작 예||

## Albert 구조
```
model_path = 'albert-base-v2'
model = AlbertModel.from_pretrained(model_path)
print(model)

AlbertModel(
  (embeddings): AlbertEmbeddings(
    (word_embeddings): Embedding(30000, 128, padding_idx=0)
    (position_embeddings): Embedding(512, 128)
    (token_type_embeddings): Embedding(2, 128)
    (LayerNorm): LayerNorm((128,), eps=1e-12, elementwise_affine=True)
    (dropout): Dropout(p=0, inplace=False)
  )
  (encoder): AlbertTransformer(
    (embedding_hidden_mapping_in): Linear(in_features=128, out_features=768, bias=True)
    (albert_layer_groups): ModuleList(
      (0): AlbertLayerGroup(
        (albert_layers): ModuleList(
          (0): AlbertLayer(
            (full_layer_layer_norm): LayerNorm((768,), eps=1e-12, elementwise_affine=True)
            (attention): AlbertAttention(
              (query): Linear(in_features=768, out_features=768, bias=True)
              (key): Linear(in_features=768, out_features=768, bias=True)
              (value): Linear(in_features=768, out_features=768, bias=True)
              (attention_dropout): Dropout(p=0, inplace=False)
              (output_dropout): Dropout(p=0, inplace=False)
              (dense): Linear(in_features=768, out_features=768, bias=True)
              (LayerNorm): LayerNorm((768,), eps=1e-12, elementwise_affine=True)
            )
            (ffn): Linear(in_features=768, out_features=3072, bias=True)
            (ffn_output): Linear(in_features=3072, out_features=768, bias=True)
            (dropout): Dropout(p=0, inplace=False)
          )
        )
      )
    )
  )
  (pooler): Linear(in_features=768, out_features=768, bias=True)
  (pooler_activation): Tanh()
)
```
## AlbertTokenizer
- Albert 의 special token들중 pad_token과 unk_token은 BERT와 다르므로, 만약 BERT와 동일한 token으로 지정하려면 아래처럼 하면 됨.

```
# 원래 기본 ALBERT에 PAD 토큰 = <pad>, UNK 토큰 = <unk> 인데, 
# BERT와 동일하게 만들었다면 [PAD], [UNK] 지정해 주면 됨.

tokenizer = AlbertTokenizer.from_pretrained(vocab_path, unk_token='[UNK]', pad_token='[PAD]')
```
## Albert from Scratch
- 한국어 Albert 모델 만들기

### 1. Tokenizer 생성
- 한국어 말뭉치(kowiki-2019-mecab)를 이용하여, sentencepiece vocab 생성.
- vocab 크기 : **32,000개** 가 적당
- kowiki 말뭉치를 mecab 형태로소 한번 돌린 **kowiki-2019-mecab.txt 로 tokenizer 생성**함.
- 실제 **훈련할때는 kowiki-2019.txt로 훈련**하는게 효과적임.
<br> 참고 : [scratch tokenizer 생성](https://github.com/kobongsoo/BERT/blob/master/tokenizer_sample/sp_scratch.ipynb1)

### 2. 빈 albert 모델 생성
-  hidden_size = 768, num_attention_heads=12, intermediate_size=768*4=3072 
<br> 참고 : [빈껍데기albert 제작](https://github.com/kobongsoo/BERT/blob/master/albert/albert-model-create.ipynb)

### 3. 훈련
- sop 훈련용 말뭉치를 만들기 힘들어서, MLM 훈련만 시킴.
- 반드시 해당 말뭉치는 tokenizer 만들때 사용한 원본 **kowiki-2019.txt** 로 훈련시킴
<br> 참고: [MLM Further Pretrain](https://github.com/kobongsoo/BERT/blob/master/albert/albert-further-pretrain-mlm.ipynb)

### 4. sbert 생성
- sentence-albert 만들기
<br> 참고: [s-albert 만들기](https://github.com/kobongsoo/BERT/blob/master/albert/albert-sts-to-sbert.ipynb)

### 5. STS 테스트

|모델|설명|klue-sts-v1.1|kor-sts(tune_test.tsv)|
|:---|:-------|-------:|---------------:|
|s-albert-1|위 방식대로 kowiki-2019로 MLM 훈련시키고 sbert 만든 모델|0.4792|0.6115|
|s-albert-2|위 s-albert-1을 korsts로 100번 훈련시킨 모델|0.4520|0.6116|
|s-albert-3|위 s-albert-2를  TED2020-en-ko-train.tsv 영어-한국어 TS Distilation 훈련 시킨 모델|0.1837|0.4188|

### 결론
- 한국어만 있는 vocab에서는 [영어-한국어 TS Distilation 훈련](https://github.com/kobongsoo/BERT/blob/master/sbert/sbert-distillaton.ipynb)은 오히려 성능 저하만 불러옴
- 한국어 sts 를 훈련시켜도 데이터가 적어서인지 별 효과 없음.
<br> MLM 훈련시킨 kowiki-2019로 [증강: Silver STS 말뭉치 제작](https://github.com/kobongsoo/BERT/blob/master/sbert/Augmented/sbert-no-dataset.ipynb)해서 훈련시켜봐야 겠음.

