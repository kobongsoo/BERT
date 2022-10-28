# 에러 리포트

## distilbert 관련 에러
#### 1. TypeError: forward() got an unexpected keyword argument 'token_type_ids'
- distilbert에는 token_type_ids 가 없다. 따라서 말뭉치를 tokenizer 할때, token_type_ids가 생성되어 모델 훈련및 예측이 안되는 것이므로, tokenizer가 잘못 설정된 것이다.
<br> tokenizer_config.json 에 "tokenizer_class": "DistilBertTokenizer" 으로 잘 설정되어 있는지 확인해라.


## huggingface 관련 에러
#### 1. windows requires developer mode to be activated
- huggingface 모델 혹은 tokenizer를 불러오기 할때, 관리자 권한이 아니거나, 윈도우 10/11에서 개발자 모드가 꺼져 있는 경우 위 에러 발생함.
<br> 따라서 아나콘다를 관리자 권한으로 실행하거나, 윈도우 os 개발자 모들를 켜야 함

#### 2. please explicitly set TOKENIZERS_PARALLELISM=(true | false)
- 병렬화 tokenizer 처리 를 disable 시키면 됨.
```
import os
os.environ["TOKENIZERS_PARALLELISM"] = "false"
```

#### 3. CUDA error: CUBLAS_STATUS_NOT_INITIALIZED 
```
CUDA error: CUBLAS_STATUS_NOT_INITIALIZED when calling `cublasCreate(handle)
indexSelectLargeIndex: block: [306,0,0], thread: [0,0,0] Assertion `srcIndex < srcSelectDimSize` failed.
```
- 해당 오류는 기존 Embedding(8002, 768, padding_idx=1) 처럼 입력 vocab 사이즈가 8002인데, 0~8001 사이를 초과하는 word idx 값이 들어가면 에러 발생함.
- 즉 **모델과 tokenizer간에 embedding이 맞지 않아서 발생하는 문제**로 보통 모델이 embeddgin 사이즈를 아래처럼 설정하면 됨

```
model.resize_token_embeddings(len(tokenizer))
```
- 혹은 다른 경우에는 tokenizer 처리된 이전 **cache 말뭉치를 그대로 사용하는 경우**이므로, 이때는 말뭉치 cache 파일을 삭제하면됨 

#### 4. KoBert tokenizer 
- **skt/kobert-base-v1 허깅페이스 모델**을 사용할때 AutoTokenizer 사용하면 안됨.(훈련시 CUBLAS_STATUS_NOT_INITIALIZED 에러 발생함)
- 이유는 **XLNetTokenizer** 사용하는데, AutoTokenizer 로는 지원하지 않음. 그렇다고 XLNetTokenizer tokenizer를 이용해도 안됨(이유는 모름)
- 따라서 아래처럼 **kobert_tokenizer 패키지를 설치하고 KoBERTTokenizer 함수**를 이용해야 함.
```
#kobert_tokenizer 패키지를 설치
!pip install 'git+https://github.com/SKTBrain/KOBERT.git#egg=kobert_tokenizer&subdirectory=kobert_hf'
```
```
from kobert_tokenizer import KoBERTTokenizer
tokenizer = KoBERTTokenizer.from_pretrained('skt/kobert-base-v1')

from transformers import BertModel
model = BertModel.from_pretrained('skt/kobert-base-v1')

```
- 출처 : https://velog.io/@m0oon0/KoBERT-%EC%82%AC%EC%9A%A9%EB%B2%95

#### 5. truncation 에러
```
Be aware, overflowing tokens are not returned for the setting you have chosen, 
i.e. sequence pairs with the 'longest_first' truncation strategy. So the returned list will always be empty even if some tokens have been removed.
```
- tokenizer 에서 max_seq_len이 작은 경우 긴 문장은 잘리는데, 해당 tokenizer에서 지원 안되서 발생하는 문제(kobert nli 훈련시 긴문장 발생함)
- max_seq_len 를 늘리면 됨

## jupyter lab 관련 에러
#### 1. 파일저장 및 출력시 에러 
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
