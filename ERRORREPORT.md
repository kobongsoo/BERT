# 에러 리포트

## distilbert 관련 에러
### 1. TypeError: forward() got an unexpected keyword argument 'token_type_ids'
- distilbert에는 token_type_ids 가 없다. 따라서 말뭉치를 tokenizer 할때, token_type_ids가 생성되어 모델 훈련및 예측이 안되는 것이므로, tokenizer가 잘못 설정된 것이다.
<br> tokenizer_config.json 에 "tokenizer_class": "DistilBertTokenizer" 으로 잘 설정되어 있는지 확인해라.


## huggingface 관련 에러
### 1. windows requires developer mode to be activated
- huggingface 모델 혹은 tokenizer를 불러오기 할때, 관리자 권한이 아니거나, 윈도우 10/11에서 개발자 모드가 꺼져 있는 경우 위 에러 발생함.
<br> 따라서 아나콘다를 관리자 권한으로 실행하거나, 윈도우 os 개발자 모들를 켜야 함
