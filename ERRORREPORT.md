# 에러 리포트

## distilbert 관련 에러
### 1. TypeError: forward() got an unexpected keyword argument 'token_type_ids'
- distilbert에는 token_type_ids 가 없다. 따라서 말뭉치를 tokenizer 할때, token_type_ids가 생성되어 모델 훈련및 예측이 안되는 것이므로, tokenizer가 잘못 설정된 것이다.
<br> tokenizer_config.json 에 "tokenizer_class": "DistilBertTokenizer" 으로 잘 설정되어 있는지 확인해라.


## huggingface 관련 에러
### 1. windows requires developer mode to be activated
- huggingface 모델 혹은 tokenizer를 불러오기 할때, 관리자 권한이 아니거나, 윈도우 10/11에서 개발자 모드가 꺼져 있는 경우 위 에러 발생함.
<br> 따라서 아나콘다를 관리자 권한으로 실행하거나, 윈도우 os 개발자 모들를 켜야 함

### 2. please explicitly set TOKENIZERS_PARALLELISM=(true | false)
- 병렬화 tokenizer 처리 를 disable 시키면 됨.
```
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
```

## jupyter lab 관련 에러
### 1. 파일저장 및 출력시 에러 
```
IOPub data rate exceeded.
The Jupyter server will temporarily stop sending output
to the client in order to avoid crashing it.
To change this limit, set the config variable
`--ServerApp.iopub_data_rate_limit`.

Current values:
ServerApp.iopub_data_rate_limit=1000000.0 (bytes/sec)
ServerApp.rate_limit_window=3.0 (secs)
```
- 위 에러는 출력 데이터 초과시 발생하는 오류이다. 
터미널 창을 열고 cmd 창에 아래처럼 jupyter lab --ServerApp.iopub_data_rate_limit=1.0e10 입력하여 새로운 jupyter lab을 실행시킨다.

```
(bong)E:\> jupyter lab --ServerApp.iopub_data_rate_limit=1.0e10
```
