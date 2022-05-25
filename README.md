# BERT
<img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white"/><img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
[![Hits](https://hits.seeyoufarm.com/api/count/incr/badge.svg?url=https%3A%2F%2Fgithub.com%2Fkobongsoo%2FBERT&count_bg=%2379C83D&title_bg=%23555555&icon=&icon_color=%23E7E7E7&title=hits&edge_flat=false)](https://hits.seeyoufarm.com)
- BERT와 관련된 자료들입니다. 자세한 내용은 아래 각 항목에 링크를 누르시면 확인할 수 있습니다.
- 테스트는 추가 학습한 [sentencebert 모델](https://huggingface.co/bongsoo/sentencebert_v1.0)을 통해 테스트 해볼수 있음 
### 1. BERT 
- [BERT를 이용한 sementic 검색 모델 제작 과정](https://github.com/kobongsoo/BERT/tree/master)
- [BERT 예제](https://github.com/kobongsoo/BERT/tree/master/bert)
- [BERT 모델의 출력 차원(dimension) 줄이기](https://github.com/kobongsoo/BERT/tree/master/mymodel)
- [BERT 추출 요약](https://github.com/kobongsoo/BERT/tree/master/summarizer)

### 2. DistilBERT
- [DistilBERT 예제](https://github.com/kobongsoo/BERT/tree/master/distilbert)

### 3. SentenceBERT
- [SenetenceBERT 예제](https://github.com/kobongsoo/BERT/tree/master/sbert)

### 4. Tokenizer
- [BertWordPieceTokenizer/ SentencePieceTokenizer](https://github.com/kobongsoo/BERT/tree/master/tokenizer_sample)

### 5. 유사도 측정
- [유사도 측정 예제/FAISS](https://github.com/kobongsoo/BERT/tree/master/embedding_sample)
- [ElasticSearch로 임베딩 벡터(Embedding Vector)를 이용한 문장 유사도 검색 구현하기](https://github.com/kobongsoo/BERT/tree/master/elasticsearch)

### 6. 기타
- [말뭉치(Corpus)](https://github.com/kobongsoo/BERT/tree/master/corpus_sample)
- [FLASK](https://github.com/kobongsoo/BERT/tree/master/Flask)
- [WandB](https://github.com/kobongsoo/WandB/tree/master)
- [GPU 메모리보다 큰 모델 파인 튜닝하기](https://github.com/kobongsoo/GPUTech/tree/master)
- [양자화(Quantization) 기법](https://github.com/kobongsoo/BERT/tree/master/Quantization)

***

### Tips
##### 1. 말뭉치에 개행문자(/r/n) 제거
```
with open(corpus_path, 'r') as f: # 읽기로 파일 열기
    lines = f.readlines()
    
    with open(corpus_path1, 'w') as f1:  # 쓰기로 파일 열기
        for line in lines:               # 한줄씩 읽어와서, 개행문자 제거
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            f1.write(line)               # 제거된 한줄씩 저장
 ```
##### 2. 파일 로딩/저장
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
##### 3. df 를 list로 변환
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

#### 4. torch.save 모델 저장
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
