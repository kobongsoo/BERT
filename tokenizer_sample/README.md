### BertWordPieceTokenizer 와 SentencePieceTokenizer 예제들

#### 1 .BertWordPieceTokenizer
- word 첫글자에는 그대로, 다음 subword는 ## prefix 붙음
- 대표 모델 : BERT-base-mulitlingual-cased
```
나는 오늘 아침밥을 먹었다." =>
Tokens (str) : [''나', '##는', '오늘', '아침', '##밥', '##을', '먹', '##었다', '.']
Tokens (int) : [875, 3261, 5446, 6142, 3776, 3509, 1474, 17145, 18]
```
#### 2. SentencePieceTokenizer
- word 첫글자에는 _ prefix 붙고, 다음 subword는 그대로.
- 대표 모델 : KoBert(SKT)
```
'나는 오늘 아침밥을 먹었다.' => 
Tokens (str) : ['▁나는', '▁오늘', '▁아침', '밥', '을', '▁먹', '었다', '.']
Tokens (int) : [4284, 552, 4269, 30456, 29636, 2570, 371, 29631]
```
