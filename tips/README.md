## Tips <img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/>
### 모델 일부 parameter update 방법
- 모델 일부를 freeze(고정) 시키고, 일부에 대해서만 parameter 업데이트 하는 방법

#### 모델 B parameter만 업데이트 하기
- B->A로 가는 gradient 막으면 됨.
![image](https://user-images.githubusercontent.com/93692701/177694379-b20de390-cc7e-4a9a-bdb2-a50017367ae0.png)
```
#detach() 이용
z=A(x)
y=B(z.detach())
```
```
#no_grade 이용
with torch.no_grad():
    z=A(x)
y=B(z)
```
```
# requires_grad 사용 => 모델마다 gradient를 끌수 있음.
for p in A.parameter():
    p.requires_grad = False
z=A(x)
y=B(z)
```

#### 모델 A parameter만 업데이트 하기
- B->A로 가는 gradient 막으면 안됨. 따라서 detach() 사용 못함
- no_grade 는 gradient를 계산하지 않겠다는 의미므로, B가 계산안되면, A도 계산안되므로 사용 불가.
- requires_grad 만 사용 가능

![image](https://user-images.githubusercontent.com/93692701/177694834-4fcdc007-88c2-422b-9f4d-27fa01d3bce3.png)

```
# requires_grad 사용 => 모델마다 gradient를 끌수 있음.
for p in B.parameter():
  p.requires_grad = False
z = A(x)
y = B(z)
```
출처 : https://nuguziii.github.io/dev/dev-003/

### HuggingFace BertTokenizer 방식들
- Huggingface BertTokenizer 를 사용하는 방식들에 대해 설명한다.
```
from transformers import BertTokenizer
tokenizer = BertTokenizer.from_pretrained('bert-multilingual-cased')
```
예제 : [BertTokenizer 방식](https://github.com/kobongsoo/BERT/blob/master/tips/huggingface_tokenizer_methods.ipynb)

```
text = "hello world!"
```

#### 1. encode
- list/tensor type: input_ids만 출력
```
token_ids = tokenizer.encode(text, max_length=128, padding="max_length", return_tensors="pt")
```
```
print(token_ids)

tensor([[  101, 61694, 10133, 11356,   106,   102,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0]])
```

#### 2. encode_plus
-  dict type: input_ids, token_type_id, attention_mask 출력 
```
token_ids = tokenizer.encode_plus(text, max_length=128, padding="max_length", return_tensors="pt")
```
```
print(token_ids)

{'input_ids': tensor([[  101, 61694, 10133, 11356,   106,   102,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0,     0,     0,
             0,     0,     0,     0,     0,     0,     0,     0]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
         0, 0, 0, 0, 0, 0, 0, 0]])}
```
#### 3. toknizer
- encode_plus 와 동일
```
token_ids = tokenizer(text, max_length=128, padding="max_length", return_tensors="pt")
```
#### 4. convert_tokens_to_ids 
-  [CLS]=101, [SEP]=102 빼고 tokeni_id만 출력
```
tokens = tokenizer.tokenize(text)
token_ids = tokenizer.convert_tokens_to_ids(tokens)

```
```
print(tokens)
print(token_ids)

['hell', '##o', 'world', '!']
[61694, 10133, 11356, 106]
```

#### 5. batch_encode_plus 사용 
- input_ids, token_type_id, attention_mask 배치로 묶어 출력
```
text_list = ["hello world!", "hellow mars!", "hellow sum!"]
token_ids = tokenizer.batch_encode_plus(text_list, max_length=8, padding="max_length", return_tensors="pt")
```
```
print(token_ids)

{'input_ids': tensor([[  101, 61694, 10133, 11356,   106,   102,     0,     0],
        [  101, 61694, 16602, 11438,   106,   102,     0,     0],
        [  101, 61694, 16602, 28439,   106,   102,     0,     0]]), 'token_type_ids': tensor([[0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0]]), 'attention_mask': tensor([[1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 0],
        [1, 1, 1, 1, 1, 1, 0, 0]])}
```
- 아래도 방식도 동일함
```
token_ids = tokenizer(text_list, max_length=8, padding="max_length", return_tensors="pt")
```
***
### Python 관련
#### Generator
- generator 는 간단하게 설명하면 iterator 를 생성해 주는 function 이다. 
- iterator 는 next() 메소드를 이용해 데이터에 순차적으로 접근이 가능한 object 이다
- Generator 생성하는 방법에는 yield 사용, generator expression 2가지 방법이 있다.
- 장점은 **메모리를 효율적 사용 가능**
<br> **Lazy evaluation** 즉 계산 결과 값이 필요할 때까지 계산을 늦추는 효과를 볼 수 있다.
```
#  list 의 경우 사이즈가 커질 수록 그만큼 메모리 사용량이 늘어나게 된다. 
하지만, generator 의 경우는 사이즈가 커진다 해도 차지하는 메모리 사이즈는 동일하다. 이는 list 와 generator의 동작 방식의 차이에 기인한다.

import sys
sys.getsizeof( [i for i in xrange(100) if i % 2] )    # list
536

sys.getsizeof( [i for i in xrange(1000) if i % 2] )
4280

sys.getsizeof( (i for i in xrange(100) if i % 2) )    # generator
80

sys.getsizeof( (i for i in xrange(1000) if i % 2) )    # generator
80
```

```
def sleep_func(x):
     print "sleep..."time.sleep(1)
     return x

# list 생성list = [sleep_func(x) for x in xrange(4)]

for i in list:
    print i
    
<결과>
sleep...
sleep...
sleep...
sleep...
0
1
2
3

# generator 생성
gen = (sleep_func(x) for x in xrange(5))

for i in gen:
    print i
    
<결과>
sleep...
0
sleep...
1
sleep...
2
sleep...
3
```
<br> 출처: https://bluese05.tistory.com/56

##### yield
- yield 만하면, 됨.
- generator 함수가 처음부터 시작되는게 아니라 yield 이후 구문부터 시작되게 됨.

```
def generator(n):    
    i = 0    
    while i < n:        
    yield i        
    i += 1

for x in generator(4):
print x

0
1
2
3
```
##### generator expression
- list comprehension 처럼 () 로 묶어 주면됨.
```
>>> [ i for i in xrange(10) if i % 2 ]
[1, 3, 5, 7, 9]

>>> ( i for i in xrange(10) if i % 2 )
<generator object <genexpr> at 0x7f6105d90960>
```

### 기타
#### 말뭉치에 개행문자(/r/n) 제거
```
with open(corpus_path, 'r') as f: # 읽기로 파일 열기
    lines = f.readlines()
    
    with open(corpus_path1, 'w') as f1:  # 쓰기로 파일 열기
        for line in lines:               # 한줄씩 읽어와서, 개행문자 제거
            line = line.replace("\r", "")
            line = line.replace("\n", "")
            f1.write(line)               # 제거된 한줄씩 저장
 ```
#### 파일 로딩/저장
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
#### 파일들 병합 하기 
```
filenames = [
    '../nlp_corpus/noxlsx2_dump/0000.txt',
    '../nlp_corpus/noxlsx2_dump/0001.txt',
    '../nlp_corpus/noxlsx2_dump/0002.txt'
          ]

out_file = '../data11/korpora/nlp_corpus_merge.txt'

with open(out_file, 'w') as outfile:
    for filename in filenames:
        with open(filename) as file:
            for line in file:
                outfile.write(line)
```                
#### df 를 list로 변환
```
# 예제 1)
# csv 파일 로딩해봄
outfile_fpath = "../../korpora/korQuAD/KorQuAD_v1.0_train.csv"
df1 = pd.read_csv(outfile_fpath)

# df을 list로 변환
context_list = np.array(df['context'].tolist())
question_list = np.array(df['question'].tolist())
answer_list = np.array(df['answer'].tolist())

# list들을 zip 으로 묶고, df 생성함
df = pd.DataFrame((zip(context_list, question_list, answer_list)), columns = ['context','question','answer'])
```
```
# 예제 2)
# 영어-한국어 쌍 말뭉치를 df->list로 변환후 한국어-영어 쌍 tsv 파일로 만
# df -> list로 만들기(df.values.tolist())

import numpy as np
import pandas as pd
from tqdm.notebook import tqdm
import csv

# 영어-한국어 쌍 tsv 파일 불러옴 
train_file = '../../data11/korpora/pair/en-ko/news_talk_en_ko_train.tsv' #영어-한국어

df = pd.read_csv(train_file, sep = '\t')
dataset = df.values.tolist()  # df->list로 변환
print(dataset[0:5])

# 한국어-영어 쌍 tsv 로 만듬
f = open('../../data11/korpora/pair/en-ko/news_talk_ko_en_train.tsv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f, delimiter='\t')
for data in tqdm(dataset):
    wr.writerow([data[1], data[0]])
f.close()

```

### torch.save 모델 저장
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

### load_dataset 로딩 후 tsv 파일로 저장
- load_dataset 데이터셋 로딩후, 특정 열만 tsv 파일로 저장하는 예시
```
# 
from datasets import load_dataset
dataset = load_dataset('csv', data_files='./data11/1113_social_train_set_1210529.csv')

#  huggingface load_dataset 예시: glue, subset: stsb, split: train
#dataset = load_dataset('glue', 'stsb', split='train')

```
```
# dataset 구조 확인
dataset

DatasetDict({
    train: Dataset({
        features: ['sn', 'file_name', 'data_set', 'domain', 'subdomain', 'source', 'ko', 'mt', 'en', 'source_language', 'target_language', 'license', 'style'],
        num_rows: 1210529
    })
})
```
```
# 'en', 'ko' 열만 뽑아내서 .tsv 파일에 쓰기  
import csv
from tqdm.notebook import tqdm
    
f = open('en_ko_train.tsv', 'w', encoding='utf-8', newline='')
wr = csv.writer(f, delimiter='\t')
for data in tqdm(dataset['train']):
    wr.writerow([data['en'], data['ko']])
f.close()
```
### load_dataset 불러오기 예시
```
[로컬 데이터 파일 로딩]
dataset = load_dataset("text", data_files='로컬.txt')       # text 로컬 파일 로딩
dataset = load_dataset("csv", data_files='로컬.csv')        # csv 로컬 파일 로딩
dataset = load_dataset("csv", data_files='로컬.tsv', delimiter="\t")  # tsv 로컬 파일 로딩
dataset = load_dataset("json", data_files='로컬.json')      # json 로컬 파일 로딩
dataset = load_dataset("pandas", data_files='로컬.pkl')     # pickled dataframe 로컬 파일 로딩
```
```
[원격 데이터 파일 로딩]
url = "https://github.com/crux82/squad-it/raw/master/"
data_files = {
 "train": url + "SQuAD_it-train.json.gz",
"test": url + "SQuAD_it-test.json.gz",
 }
 
squad_it_dataset = load_dataset("json", data_files=data_files, field="data")
```
### sklenarn 으로 cosine 확인 예제
```
from sklearn.metrics.pairwise import cosine_similarity
cosine_sim = cosine_similarity([embed_querys[0]], [embed_querys_1[0]]) # (1,768) 식에 2차원 배열입력되어야 함.
```
