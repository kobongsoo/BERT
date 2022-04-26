### BertWordPieceTokenizer 와 SentencePieceTokenizer

#### 1 .BertWordPieceTokenizer
- subword는 ## prefix 붙고, word는 prefix 없음
- 대표 모델 : BERT-base-mulitlingual-cased
```
나는 오늘 아침밥을 먹었다." => word: 나, 오늘, 아침, 먹, . / subword: ##는, ##밥, ##을, ##었다

Tokens (str) : [''나', '##는', '오늘', '아침', '##밥', '##을', '먹', '##었다', '.']
Tokens (int) : [875, 3261, 5446, 6142, 3776, 3509, 1474, 17145, 18]
```
#### 2. SentencePieceTokenizer
- word는 _ prefix 붙고, subword는 prefix 없음
- 대표 모델 : KoBert(SKT)
```
'나는 오늘 아침밥을 먹었다.' => word: _나는, _오늘, _아침, _먹 / subword: 밥, 을, 었다, .

Tokens (str) : ['▁나는', '▁오늘', '▁아침', '밥', '을', '▁먹', '었다', '.']
Tokens (int) : [4284, 552, 4269, 30456, 29636, 2570, 371, 29631]
```
