## BertWordPieceTokenizer(이하: BPT) / SentencePieceTokenizer(이하: SPT) <img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white"/><img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>
소스: [BPT/SPT Tokenizer 예제](https://github.com/kobongsoo/BERT/blob/master/tokenizer_sample/SPvsWP.ipynb)

### 1 .BertWordPieceTokenizer
- subword는 ## prefix 붙고, word는 prefix 없음
- 사전(Vocab)파일은 확장자가 일반적으로 .txt 임
- 대표 모델 : BERT-base-mulitlingual-cased
```
나는 오늘 아침밥을 먹었다." => word: 나, 오늘, 아침, 먹, . / subword: ##는, ##밥, ##을, ##었다

Tokens (str) : [''나', '##는', '오늘', '아침', '##밥', '##을', '먹', '##었다', '.']
Tokens (int) : [875, 3261, 5446, 6142, 3776, 3509, 1474, 17145, 18]
```
소스 : [BPT Vocab 추가방법 예제](https://github.com/kobongsoo/BERT/blob/master/tokenizer_sample/bert_add_vocab.ipynb)

### 2. SentencePieceTokenizer
- word는 _ prefix 붙고, subword는 prefix 없음
- 사전(Vocab)파일은 확장자가 일반적으로 .spiece 임
- 대표 모델 : KoBert(SKT)
```
'나는 오늘 아침밥을 먹었다.' => word: _나는, _오늘, _아침, _먹 / subword: 밥, 을, 었다, .

Tokens (str) : ['▁나는', '▁오늘', '▁아침', '밥', '을', '▁먹', '었다', '.']
Tokens (int) : [4284, 552, 4269, 30456, 29636, 2570, 371, 29631]
```
소스 : [SPT Vocab 추가방법 예제](https://github.com/kobongsoo/BERT/blob/master/tokenizer_sample/sp_new_insert.ipynb)

### 3. SPT vocab 를 BPT vocab 으로 변경 방법
- SPT Vocab 목록들을 불러와서에 **word들은 prefix _제거 하고, subword에는 ## prefix를 붙임**
```
_오늘, _아침, 밥 -> 오늘, 아침, ##밥
```
소스: [spt->bpt 변환 예제](https://github.com/kobongsoo/BERT/blob/master/tokenizer_sample/kobertvocab.ipynb)

```
import gluonnlp as nlp   # GluonNLP는 버트를 간단하게 로딩하는 인터페이스를 제공하는 API 임

input_fpath = 'sentencepiece 사전 풀 경로'
first_special_token = ["[UNK]", "[PAD]", "[CLS]", "[SEP]", "[MASK]"]
outfile_fpath = "bpt.txt" # bpt 출력(변환) 파일

vocab = nlp.vocab.BERTVocab.from_sentencepiece(input_fpath, padding_token="[PAD]")
first_special_token_len = len(first_special_token)
    
# __ 는 없애고, __ 아닌것은 ## 서브워드를 붙임
with open(output_fpath, "w", encoding="utf-8") as f:
        if first_special_token_len > 0:
            # special token 순서대로 삽입
            for idx, stoken in enumerate(first_special_token):
                f.writelines(stoken + "\n")
                print('sp:{}, idx:{}'.format(idx,stoken))
                
        for k, v in vocab.token_to_idx.items():
            print('k:{}, idx:{}'.format(k,v))
            if k[0] == '▁':
                k = k.replace('▁', '')
                f.writelines(k + "\n")
            elif k in ["[UNK]", "[PAD]", "[CLS]", "[SEP]", "[MASK]"]:
                if first_special_token_len == 0:
                    f.f.writelines(stoken + "\n")  
                pass
            else:
                k = '##' + k
                f.writelines(k + "\n")
```

### 4. BPT 사전 만들기
- BPT 를 이용하여, 사전(Vocab)을 만드는 방식은 크게 2가지 방식이 있음
- **1.처음부터 사전 만들기, 2.기존 사전에 도메인 단어들을 추가하기**
- 사전을 만들기 위해서는 단어들의 있는 말뭉치가 필요함.
- **좋은 사전을 만들기 위해서는 전처리 단계로 [한국어 형태소 분석기](https://konlpy.org/ko/latest/index.html)(Mecab,Okt, Komoran등)들을 이용하여 말뭉치에 대해 형태소 분리가 필요함**

#### 4-1.처음부터 사전 만들기
- 1. Mecab을 이용하여 말뭉치 형태소 분리
- 2. Vocab size, 최소 빈도수(min_frequency), special_tokens 등을 지정 
- 3. BertWordPieceTokenizer 를 이용하여, 훈련

소스 : [처음부터 사전 만들기 예제](https://github.com/kobongsoo/BERT/blob/master/tokenizer_sample/bert_tokenizer.ipynb)

#### 4-2.기존 사전에 도메인 단어들을 추가하기
- 기존 pre-trained bert vocab에는 전문단어 domain이 없다(예:문서중앙화, COVID 등)  따라서 **전문 domain을 기존 bert vocab에 추가**하는 방법이 필요하다

- 1. 도메인 말뭉치(예:kowiki.txt)에서 **mecab을 이용하여 형태소 분석하여 단어들을 추출함**.
   - **mecab으로 형태소 혹은 명사만 분할하면서, subword 앞에는 '##' prefix 추가함**
- 2. NLTK 빈도수 계산하는 FreqDist()를 이용하여, **단어들이 빈도수 계산**
- 3. 상위 빈도수(예:30000)를 가지는 단어들만 add_vocab.txt 로 만듬
- 4. 기존 bert vocab.txt 파일에 직접, add_vocab.txt 토큰들 추가(**이때 중복 제거함**)
- 5. 추가한 vocab을 가지고, tokenizer 생성하고, special 토큰 추가 후, 저장

소스 : [기존 사전에 도메인 단어들을 추가하기 예제](https://github.com/kobongsoo/BERT/blob/master/tokenizer_sample/make_mecab_vocab.ipynb)

### 5. 참고

#### 5-1. 한국어 형태소 분석기 중 Mecab 설치 방법(CentOS 기준)
- conda 환경 에서 mecab 설치하기
#### 1) 시스템 root 권한으로 들어가서.
```
>> bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh) 
```
#### 2) conda 가상 환경으로 들어가서.
```
>> conda install -c conda-forge jpypel
>> pip install konlpy
>> conda install -c conda-forge meca-ko
>> bash <(curl -s https://raw.githubusercontent.com/konlpy/konlpy/master/scripts/mecab.sh)
>> pip3 install /tmp/mecab-python-0.996
```
#### 3) 테스트 
```
import konlpy
from konlpy.tag import Mecab
mecab1=Mecab()
sentence = "안녕하세요 저는 상휴입니다"
output = mecab1.morphs(sentence)
print(output)
```
