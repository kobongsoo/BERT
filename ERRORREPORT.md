# 에러 리포트

## distilbert 관련 에러
### 1. TypeError: forward() got an unexpected keyword argument 'token_type_ids'
- distilbert에는 token_type_ids 가 없다. 따라서 말뭉치를 tokenizer 할때, token_type_ids가 생성되어 모델 훈련및 예측이 안되는 것이므로, tokenizer가 잘못 설정된 것이다.
<br> tokenizer_config.json 에 "tokenizer_class": "DistilBertTokenizer" 으로 잘 설정되어 있는지 확인해라.

