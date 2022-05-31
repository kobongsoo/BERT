## ETC <img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/>
 
### 1. Transformer
#### 1) 개요
- 2017년 구글이 발표한 논문 "**Attention is all you need**" 에서 제시한 모델
- 기존 NLP(자연어 처리) 분야에 사용되던 **인코더-디코더 구조**를 따르면서도, **RNN 레이어를 사용하지 않고**, 엄청 우수한 번역 성능을 보여준 모델임.
- 기존 RNN, LSTM 모델은 인코더에서 정보를 압축하여 디코더에 보낼때, 정보 손실이 있는데, 이를 Transfomer는 Attention 이라는 메커니즘으로 정보 손실을 줄였음.

#### 2) 장점
- 병렬 프로세싱 처리에 최적화 되도록 설계되어, GPU 환경에서 대량의 데이터셋을 가지고 훈련 가능 함.
- 대량이 데이터 셋은 기존처럼 라벨링된 데이터 셋이 아니라서, 라벨링 하는데 전문인력과 시간이 필요 없음.
- Pre-Training 된 모델을 가지고 task에 맞게 Fine-Tuning 해서 성능 높은 NLP 모델을 손쉽게 만들수 있음.

#### 3) 단점
- 요즘 파생된 모델들은, 점점더 모델 SIZE가 커지고 있어서, 웬만한 H/W 로는 훈련 및 추론 불가.

#### 4) 구조

|구분|내용|
|:--------|:---------------|
|임베딩벡터|512|
|인코더/디코더 레이더|6개|
|멀티 헤더 어텐션 수|8개|
|피드포워드 네트워크 입출력 크기|2048|
![image](https://user-images.githubusercontent.com/93692701/171071032-90593545-8842-463e-bedd-8ee3100df88d.png)
![image](https://user-images.githubusercontent.com/93692701/171070996-b2b1d648-42b0-4ebd-8cd0-0fc7b7120694.png)
![image](https://user-images.githubusercontent.com/93692701/171071078-06adff18-85ea-4002-8b92-03c382a7c074.png)

출처 : https://wikidocs.net/31379

***
### Tips
#### 1. 말뭉치에 개행문자(/r/n) 제거
```
with open(corpus_path, 'r') as f: # 읽기로 파일 열기
    lines = f.readlines()
    
    with open(corpus_path1, 'w') as f1:  # 쓰기로 파일 열기
        for line in lines:               # 한줄씩 읽어와서, 개행문자 제거
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            f1.write(line)               # 제거된 한줄씩 저장
 ```
#### 2. 파일 로딩/저장
```
import numpy as np
import pandas as pd

file_path = "../../korpora/korQuAD/KorQuAD_v1.0_train.csv"

#df = pd.read_excel(file_path)    #excel 파일 로딩
#df = pd.read_csv(file_path, encoding="euc-kr")   #csv 파일 로딩
#df = pd.read_csv(file_path, sep='\t')  # tsv 파일 로딩
df=pd.read_json(file_path)   #json 파일 로딩
```
```
# df -> csv 로 저장(header=None : head는 제외)
outfile_fpath = "../../korpora/mycorpus/newspaper.csv"
df.to_csv(outfile_fpath, index=False, header= None)
```
#### 3. df 를 list로 변환
```
# csv 파일 로딩해봄
outfile_fpath = "../../korpora/korQuAD/KorQuAD_v1.0_train.csv"
df1 = pd.read_csv(outfile_fpath)

# df을 list로 변환
context_list = np.array(df['context'].tolist())
question_list = np.array(df['question'].tolist())
answer_list = np.array(df['answer'].tolist())
```
```
# list들을 zip 으로 묶고, df 생성함
df = pd.DataFrame((zip(context_list, question_list, answer_list)), columns = ['context','question','answer'])
```

### 4. torch.save 모델 저장
```
# 모델 저장
# => torch.save 로 저장하는 방법 
from transformers import WEIGHTS_NAME, CONFIG_NAME

output_dir = "./quantized/"
os.makedirs(output_dir, exist_ok=True)

output_model_file = os.path.join(output_dir, WEIGHTS_NAME)
output_config_file = os.path.join(output_dir, CONFIG_NAME)
print(output_model_file)
print(output_config_file)

# 모델 저장
torch.save(quantized_model.state_dict(), output_model_file)  # 모델 파일 pytorch_model.bin
quantized_model.config.to_json_file(output_config_file)      # 모델 config.json 저장=>huggingface 모델 로딩시 필요 

# tokenizer 저장 =>toeknizer_config.json, added_toekns.json, special_tokens_map.json, vocab.txt 
tokenizer.save_pretrained(output_dir)   
```
