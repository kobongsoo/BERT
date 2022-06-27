## 말뭉치 예시 <img src="https://img.shields.io/badge/Pytorch-EE4C2C?style=flat-square&logo=Pytorch&logoColor=white"/><img src="https://img.shields.io/badge/Python-3766AB?style=flat-square&logo=Python&logoColor=white"/></a>

### 한국어 kowiki 전처리 방법
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
- kowiki파일경로로 이동해서 wikiextractor 실행
```
wikiextractor kowiki파일명 -o 출력폴더
```
![image](https://user-images.githubusercontent.com/93692701/175891162-cff245ea-c73c-4350-8b57-f49854940d42.png)


참고 : [한국어 위키백과 (kowiki) 말뭉치 다운로드 / 전처리](https://blog.naver.com/PostView.naver?blogId=duqrlwjddns1&logNo=222484574485)

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

### [모두의 말뭉치](https://corpus.korean.go.kr/)
- 문화에육관광부 국립국어원에서 제공하는 말뭉치 사이트
- **회원 가입 필요**
- **신청후 반려될수도 있음**

###  [영어-한국어 문장쌍 말뭉치](https://github.com/UKPLab/sentence-transformers/tree/master/examples/training/multilingual)
- SentenceBERT 훈련시 필요한 영어-한국어 문장쌍 말뭉치 다운로드 사이트
- 영어-한국어 문장쌍 뿐만 아니라 , 다양한 언어들간 문장쌍 말뭉치를 다운로드 할수 있음
- 말뭉치 다운로드 사이트는 [여기](https://public.ukp.informatik.tu-darmstadt.de/reimers/sentence-transformers/datasets/) 참조
#### 주요 말뭉치
- [TED2020](https://sbert.net/datasets/ted2020.tsv.gz) : 약 100개의 영어와 다른 언어들간 문장쌍으로 된 말뭉치([다운로드 예제](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/get_parallel_data_ted2020.ipynb))
- [tatoeba](https://downloads.tatoeba.org/exports/) : 언어들을 지정해서 문장쌍 말뭉치 다운로드 할 수 있음([다운로드 예제](https://github.com/kobongsoo/BERT/blob/master/corpus_sample/get_parallel_data_tatoeba.ipynb))
- [tatoeba를 파일로 다운로드 받기](http://www.manythings.org/anki/)
- [kowiki 파일 ](https://dumps.wikimedia.org/kowiki/)
- 
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
