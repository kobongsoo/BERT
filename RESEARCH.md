## Sentence BERT Further-Pretrain Test
- 한국어 형태소 분석기 mecab을 이용하여, 전문(IT관련:mocomsys nlp_corpus 약 3M 문장이용) 말뭉치를 가지고, 
 <br> distilbert-multilingual-cased 모델에 아래와 같은 vocab을 추가하여 훈련시켜서, 최종적으로 s-bert를 만들어서 성능을  비교해 봄.
<br> **sbert-nouns : nouns(명사만) vocab 추가한 모델**
<br> **sbert-morphs: morphs(형태소=명사+조사+부사등) 추가한 모델**
- MLM 훈련시 Hyperparameter: 추가 vocab 사이즈는 32,000, batch_size: 32, epochs: 4, lr:3e-5
- 증류훈련시 Hyperparameter: 교사모델은 paraphrase-multilingual-mpnet-base-v2 이용,batch_size:32, epochs: 40, lr:3e-5
- 성능 측정을 위한 말뭉치는, korsts(tune_test.tsv)와 klue-sts(klue-sts-v1.1_dev.json) 를 이용함.

|모델     |korsts|klue-sts|korsts+klue-sts|기타          |
|:--------|------:|--------:|--------------:|:-----------------|
|sbert-nouns|0.810|0.754|0.638|증류훈련 echo:40|
|sbert-morphs|0.798|0.751|0.632|증류훈련 echo:40|
|bongsoo/sentencebert_v1.0|0.743|0.799|0.638||
|distiluse-base-multilingual-cased-v2|0.747|0.785|0.644||
|paraphrase-multilingual-mpnet-base-v2|0.820|0.799|0.721||
