## 말뭉치 예시 <img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white"/><img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>

### 한국어 kowiki 전처리 방법
<br> kowiki 전처리 예제는 [여기](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/make_corpus_kowiki.ipynb) 참조, 한줄/두줄 문장 말뭉치로 만드는 예제는 [여기](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/make_corpus_kowiki_line.ipynb) 참조
- [kowiki 최신](https://dumps.wikimedia.org/kowiki/) 버전을 다운로드 한다.
- wikiextractor 를 설치한다.
```
pip install wikiexractor
```
- wikiextractor 실행시, **윈도우 os에서는 아래와 같은 에러**가 발생할수 있다 (**fork context in multiprocessing is only supported in UNIX**)
<br>그러므로, 되도록이면 리눅스(유닉스)환경에서 설치 및 실행 하는게 좋음.
```
 File "c:\programdata\anaconda3\lib\multiprocessing\context.py", line 193, in get_context
    raise ValueError('cannot find context for %r' % method) from None
ValueError: cannot find context for 'fork'
```
- kowiki파일경로로 이동해서 wikiextractor 실행하여 text 추출
```
wikiextractor kowiki파일명 -o 출력폴더
```
![image](https://user-images.githubusercontent.com/93692701/175891162-cff245ea-c73c-4350-8b57-f49854940d42.png)

<br>참고 : [한국어 위키백과 (kowiki) 말뭉치 다운로드 / 전처리](https://blog.naver.com/PostView.naver?blogId=duqrlwjddns1&logNo=222484574485)

- 파일 합치기 
<br> 추출이 완료되면 출력폴더 하위 AA, AB, AC, ...폴더에  wiki_00, wiki_01, .. 쪼개진 파일을 하나의 파일로 합친다.
```
in_folder_path = kowiki_extra_folder       # 합칠 파일들이 있는 root 폴더
out_corpos_file = 'kowiki-20220620-corpus.txt' # 합치고나서 생성될 파일명


import os
from tqdm.notebook import tqdm

def load_file(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_text(path):
    texts = []
    for idx, (current, dirs, files) in enumerate(os.walk(path)):
        if idx == 0:
            continue
        print(current, dirs, files)
        for file in tqdm(files, desc="[Parsing]"):
            text = load_file(os.path.join(current, file))
            texts.append(text)

    return texts


def save_file(path, src):
    with open(path, "w", encoding="utf-8") as f:
        f.write(src)
        
# wikiextractor로 xml 파싱되어 저장된 파일들을 하나로 합침
texts = parse_text(in_folder_path)
save_file(out_corpos_file, "\n".join(texts))
```
참고 : https://blog.naver.com/PostView.naver?blogId=duqrlwjddns1&logNo=222484574485

- doc 테그 제거
<br> 합쳐진 kowiki 파일에는 아래와 같은 doc 테그가 있으므로, 내용만 빼고 제거한다.
```
<doc id="문서 번호" url="실제 위키피디아 문서 주소" title="문서 제목">
내용
</doc>
```

```
import re
from tqdm.notebook import tqdm

in_new_corpus_file = out_corpos_file # 입력파일
out_new_corpus_file = 'kowiki-20220620-corpus-1.txt'  # 출력 파일

# 문장길이가 짧은 문장은 삭제 
remove_short_sentence=False
remove_short_sentence_len = 20

with open(in_new_corpus_file, 'r', encoding='utf8') as f:
    data = f.read()

# 태그 삭제
splits = data.split('\n')
start = re.compile('<doc')
end = re.compile('<\/doc>')
docs = []

for split in tqdm(splits):
    # <doc> 시작과 끝 테그가 아니면 
    if not (start.match(split) or end.match(split)):
         # 짦은 문장 삭제 적용된 경우면(remove_short_sentence=Ture)
        # => 해당 길이보다 큰 경우에만 남김
        if remove_short_sentence and split:
            if len(split) > remove_short_sentence_len:
                docs.append(split)
        else:
            docs.append(split)

result = '\n'.join(docs)

with open(out_new_corpus_file, 'w', encoding='UTF8') as f:
    f.write(result)
```
참고 : https://wdprogrammer.tistory.com/42

### [Kopora](https://ko-nlp.github.io/Korpora/)
- 한국어 말뭉치 다운로드 사이트
- git 소스는 [여기](https://github.com/ko-nlp/Korpora) 참조
- **모두의 말뭉치와 AI HUB 말뭉치는 이제 다운로드 받을수 없고**, 이들은 아래 각각 사이트에서 다운로드 받아야 함

##### Kopora 설치
```
!pip install Korpora
```
##### Kopora 목록 확인
```
from Korpora import Korpora
Korpora.corpus_list()

{'kcbert': 'beomi@github 님이 만드신 KcBERT 학습데이터',
 'korean_chatbot_data': 'songys@github 님이 만드신 챗봇 문답 데이터',
 'korean_hate_speech': '{inmoonlight,warnikchow,beomi}@github 님이 만드신 혐오댓글데이터',
 'korean_parallel_koen_news': 'jungyeul@github 님이 만드신 병렬 말뭉치',
 'korean_petitions': 'lovit@github 님이 만드신 2017.08 ~ 2019.03 청와대 청원데이터',
 'kornli': 'KakaoBrain 에서 제공하는 Natural Language Inference (NLI) 데이터',
 'korsts': 'KakaoBrain 에서 제공하는 Semantic Textual Similarity (STS) 데이터',
 'kowikitext': 'lovit@github 님이 만드신 wikitext 형식의 한국어 위키피디아 데이터',
 'namuwikitext': 'lovit@github 님이 만드신 wikitext 형식의 나무위키 데이터',
 'naver_changwon_ner': '네이버 + 창원대 NER shared task data',
 'nsmc': 'e9t@github 님이 만드신 Naver sentiment movie corpus v1.0',
 'question_pair': 'songys@github 님이 만드신 질문쌍(Paired Question v.2)' }
```
##### Kopora 말뭉치 다운로드
```
Korpora.fetch("kcbert",root_dir='my_data/')
```
소스 : [kopora](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/Korpora.ipynb)

### [AI HUB](https://aihub.or.kr/)
- 개방형 한국어 말뭉치 제공 사이트
- **회원가입 필요**
- **신청 후 바로 다운로드 받을수 있음**
#### 예제

| 코드 |내용 | 
|:-----------|:--------------------------------------------|
|[ai_hub example-1](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/ai_hub_web_corpus_example.ipynb)|'대규모 웹데이터 기반 한국어 말뭉치 데이터'(json파일)에서 원천말뭉치(ts1,vs1)를 파싱해서 2줄 말뭉치를 만드는 예제|
|[ai_hub example-2](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/ai_hub_web_corpus_example2.ipynb)|'대규모 웹데이터 기반 한국어 말뭉치 데이터'(json파일)에서 라베링말뭉치(tl1,vl1)를 파싱해서 1줄/2줄/문단 말뭉치를 만드는 예제|

### [모두의 말뭉치](https://corpus.korean.go.kr/)
- 문화에육관광부 국립국어원에서 제공하는 말뭉치 사이트
- **회원 가입 필요**
- **신청후 반려될수도 있음**
### [KLUE](https://klue-benchmark.com/)
- 한국어 기반 인공지능 평가 지표. 총 8개 분야에 대한 훈련 및 평가 데이터 셋 제공함.
- Hugging Face에도 [klue dataset](https://huggingface.co/datasets/klue) 이 등록되어 있어, 아래처럼 사용 가능.
```
from datasets import load_dataset
dataset = load_dataset('klue', 'sts') # ynat, nli, ner, re, dp, mrc, wos
```
###  [영어-한국어 문장쌍 말뭉치](https://github.com/UKPLab/sentence-transformers/tree/master/examples/training/multilingual)
- SentenceBERT 훈련시 필요한 영어-한국어 문장쌍 말뭉치 다운로드 사이트
- 영어-한국어 문장쌍 뿐만 아니라 , 다양한 언어들간 문장쌍 말뭉치를 다운로드 할수 있음
- 말뭉치 다운로드 사이트는 [여기](https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/datasets/) 참조
#### 주요 말뭉치
- [TED2020](https://sbert.net/datasets/ted2020.tsv.gz) : 약 100개의 영어와 다른 언어들간 문장쌍으로 된 말뭉치([다운로드 예제](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/get_parallel_data_ted2020.ipynb))
- [tatoeba](https://downloads.tatoeba.org/exports/) : 언어들을 지정해서 문장쌍 말뭉치 다운로드 할 수 있음([다운로드 예제](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/get_parallel_data_tatoeba.ipynb))
- [tatoeba를 파일로 다운로드 받기](http://www.manythings.org/anki/)
- [kowiki 파일 ](https://dumps.wikimedia.org/kowiki/)

### Huggingface
- Huggingface에는 다양한 말뭉치를 load_dataset 이용하여 불러와 사용할수 있음.
```
# korquad_v1 말뭉치 다운로드 예시
dataset = load_dataset('squad_kor_v1', cache_dir='./data')
```
```
# kor_nli 중 xnli subset 다운로드 예시
from datasets import load_dataset
dataset = load_dataset('kor_nli','xnli', cache_dir='./data')

# dataset 출력
dataset
DatasetDict({
    validation: Dataset({
        features: ['premise', 'hypothesis', 'label'],
        num_rows: 2490
    })
    test: Dataset({
        features: ['premise', 'hypothesis', 'label'],
        num_rows: 5010
    })
})

# dataset 에서 validation dataset에서 premise만 출력
dataset['validation']['premise']
```
### 기타 말뭉치
| 말뭉치 |설명 | 다운로드|
|:-----------|:--------------------------------------------|:----------|
|KorQuAD 2.0|질문답변 20,000+ 쌍을 포함하여 총 100,000+ 쌍으로 구성된 한국어 데이터셋 | https://korquad.github.io/|
|AwesomeKorean_Data| 2020년까지 구축된 데이터중에서 오픈된 한국어 데이터 셋 모음|https://github.com/songys/AwesomeKorean_Data|

### 참고
- [말뭉치 합치기 예제](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/merge_files.ipynb) : 여러 말뭉치들을 하나로 합치는 예제(단 말뭉치들의 열계수는 같아야함)
- [.xlsx 파일을 .csv 파일로 변환 예제](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/xlsx-to-csv.ipynb)
- [.json 파일를 .csv 파일로 변환 예제](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/json-to-csv.ipynb)
- [korQuAD_v1.0 List to csv 변환 예제](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/korQuADv1.0_json-to-list-to-csv.ipynb)
- [kowiki 전처리 예제](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/make_corpus_kowiki.ipynb)
- [kowiki 한줄/두줄 말뭉치 예제](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/make_corpus_kowiki_line.ipynb)
