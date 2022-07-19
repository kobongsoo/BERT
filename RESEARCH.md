## Sentence BERT Further-Pretrain Test
- 한국어 형태소 분석기 mecab을 이용하여, 전문(IT관련:mocomsys nlp_corpus 약 3M 문장이용) 말뭉치를 가지고, 
 <br> distilbert-multilingual-cased 모델에 아래와 같은 vocab을 추가하여 훈련시켜서, 최종적으로 s-bert를 만들어서 성능을  비교해 봄.
<br> **sbert-nouns : nouns(명사만) vocab 추가한 모델**
<br> **sbert-morphs: morphs(형태소=명사+조사+부사등) 추가한 모델**
- MLM 훈련시 Hyperparameter: 추가 vocab 사이즈는 32,000, batch_size: 32, epochs: 4, lr:3e-5
- 증류훈련시 Hyperparameter: 교사모델은 paraphrase-multilingual-mpnet-base-v2 이용,batch_size:32, epochs: 40, lr:3e-5, 말뭉치:TED2020-en-ko-dev.tsv
- 성능 측정을 위한 말뭉치는, **korsts(tune_test.tsv(1,379쌍문장))** 와 **klue-sts(klue-sts-v1.1_dev.json(519쌍문장))** 를 이용함.
- 참고로 **mocomsys nlp_corpus + kowiki20200620 말뭉치를 더해서 약 7M 말뭉치로 훈련할때는, 초기에 계속 메모리 오류 남**(원인은모름)
<br>따라서 여기서는 nlp_corpus 만으로 훈련시킴.

|모델     |korsts|klue-sts|korsts+klue-sts|기타          |
|:--------|------:|--------:|--------------:|:-----------------|
|sbert-nouns|0.810|0.754|0.638|증류훈련 echo:40|
|sbert-morphs|0.798|0.751|0.632|증류훈련 echo:40|
|bongsoo/sentencebert_v1.0|0.743|0.799|0.638||
|distiluse-base-multilingual-cased-v2|0.747|0.785|0.644||
|paraphrase-multilingual-mpnet-base-v2|0.820|0.799|0.721||

### sbert-nouns Test
- 명사만 vocab에 추가한 sbert 모델을 가지고 증류훈련만 다르게 시켰을때 결과 
- **echo 40 이후 부터는 acc가 감소함.**
- MAX Acc : echo 40 일때 0.638
 
|echo     |korsts|klue-sts|korsts+klue-sts|기타          |
|:--------|------:|--------:|--------------:|:-----------------|
|0|0.725|0.755|0.565|증류훈련 안시켰을때|
|40|0.810|0.754|0.638|     |
|60|0.807|0.751|0.628||
|80|0.807|0.754|0.626||
|100|0.806|0.752|0.624||
|120|0.806|0.745|0.624||

### sbert-morphs Test
- 형태소(명사+조사+부사등)를 vocab에 추가한 sbert 모델을 가지고 증류훈련만 다르게 시켰을때 결과 
- **echo 80 이후 부터는 acc가 감소함.**
- MAX Acc : echo 80 일때 0.635

|echo     |korsts|klue-sts|korsts+klue-sts|기타          |
|:--------|------:|--------:|--------------:|:-----------------|
|0|0.745|0.787|0.611|증류훈련 안시켰을때|
|40|0.798|0.751|0.632|     |
|60|0.804|0.740|0.632||
|80|0.806|0.740|0.635||
|100|0.804|0.737|0.631||
|120|0.802|0.737|0.626||

