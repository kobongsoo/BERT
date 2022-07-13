# P-Tuning
## 개요
- prompt learning 한 방식으로, Fine-tuning 처럼 모델이 모든 파라메터를 업데이트 하지 않고, 모델이 일부 파라메터만 업데이트 하는 방식중 하나임.
- 원래 처음 GPT 계열의 단점이 NLU 테스크에서 성능이 떨어지고, 좋은 NLU 성능을 내기 위해서는 in context learning(few-shout learning) 하기 위해서 최적의
prompt 조합을 찾는게 쉽지 않다는 문제가 있다.
- 따라서 여기서 말하는 p-tuning은 이 최적의 prompt 조합을 찾는데, 기존 discreate space(분리된 공간) 에서 벗어나, 
continuous space(연속된 공간)에 prompt가 존재하도록 하는 방법이다.
- 아래는 prompt가 조금만 바뀌어도 큰 성능 차이를 보이는 예시임.
![image](https://user-images.githubusercontent.com/93692701/178618230-f1d95ec1-1a4e-474e-9660-3016b85c3b8e.png)
- p-tuning은 2021년 [GPT Understands, Too 논문](https://arxiv.org/pdf/2103.10385.pdf) 에서 처음 제시 되었고, 
이후 [p-tuning-v2](https://github.com/THUDM/P-tuning-v2) 방식도 제안 되었다.


### prefix-tuning
- GPT-2, T5등 LM에서 접두사 prompt를 추가하여 훈련시키는 방식.

### P-tuning
- P-tuning은 prefix-tuning과 같은데, 좀더 개선된 방식으로, 접두사(시작할때)에만 토큰을 삽입하는게 아니라, 중간에도 토큰을 삽입하는 방식.
![image](https://user-images.githubusercontent.com/93692701/178617025-0c87e02c-5f00-4e64-b57d-0a601f52d2f0.png)

### P-tuning-v2
- P-tunin-v2는 새로운 방식이 아니라, NLU(Natual Language Understanding) 향상을 위해 LM 모델(GTP, T5등)뿐만 아니라, MLM 모델(BERT)에도 prefix-tuning을 적용한 방식.
![image](https://user-images.githubusercontent.com/93692701/178617332-95bd50c6-35a1-4a22-9987-fb4a20a14d80.png)
출처 : https://github.com/THUDM/P-tuning / https://github.com/THUDM/P-tuning-v2

### P-tuning-v2 구현 방식
- P-tuning-v2의 구현 방식은 prefix N 시퀀스를 생성한 다음, 원래 bert 모델과 연결한다. 
- 이때 bert의 **past_key_values**(여기서는 원래 목적인 decoding 속도 개선 목적이 아님)를 이용함.
<br>따라서 **albert, distilbert 등에서는 past_key_values 인자가 없으므로 적용 못함.**
- get_prompt() 함수 : prefix를 past_key_value 형식(batch_size, num_heads, sequence_length - 1, embed_size_per_head)으로 조정(만듬)
- attention_mask : 기존 attention_mask +  prefix_attention_mask 더함.

```
class PrefixEncoder(torch.nn.Module):
    def __init__(self):
        super().__init__()
        self.embedding = torch.nn.Embedding(seq_len, dim_ebd)
        self.trans = torch.nn.Sequential(
            torch.nn.Linear(dim_ebd, dim_ebd),
            torch.nn.Tanh(),
            
            # num_hidden_layers(12)*2*dim_embedding 인데, 
            #- 여기서 *2는 key와 value를 기존 입력 key와 value로 연결시키는 구조이므로, *2를 해준것임.
            torch.nn.Linear(dim_ebd, num_layer * 2 * dim_ebd)
        ).to(device)
    def forward(self, prefix):
        prefix_tokens = self.embedding(prefix)
        past_key_values = self.trans(prefix_tokens)
        return past_key_values
```
```
config = BertConfig.from_pretrained("path")
class BertPrefixForQuestionAnswering(BertPreTrainedModel):
    def __init__(self):
        super().__init__(config)
        self.num_labels = 2
        self.bert = BertModel.from_pretrained("path", add_pooling_layer=False)
        self.path = "path"
        self.bert.load_state_dict(torch.load(self.path))
        self.qa_outputs = torch.nn.Linear(1024, self.num_labels)
        self.dropout = torch.nn.Dropout(0.3)
        self.prefix_encoder = PrefixEncoder()
        self.pre_seq_len = 15
        self.prefix_tokens = torch.arange(self.pre_seq_len).long()
       
        for param in self.bert.parameters():
            param.requires_grad=False

    # prefix를 past_key_value 형식(batch_size, num_heads, sequence_length - 1, embed_size_per_head)으로 조정(만듬)
    def get_prompt(self, batch_size):
        prefix_tokens = self.prefix_tokens.unsqueeze(0).expand(batch_size, -1).to(device)
        past_key_values = self.prefix_encoder(prefix_tokens)
        bsz, seqlen, _ = past_key_values.shape
        past_key_values = past_key_values.view(
            bsz,
            seqlen,
            num_layer * 2,
            num_head,
            dim_ebd//num_head
            )
        past_key_values = self.dropout(past_key_values)
        past_key_values = past_key_values.permute([2, 0, 3, 1, 4]).split(2)
        return past_key_values

    def forward(self, input_ids, token_type_ids, attention_mask):

        batch_size = input_ids.shape[0]
        
        # prefix에 대한 past_key_values 값을 구함
        past_key_values = self.get_prompt(batch_size=batch_size)
        
        # attention_mask : 기존 attention_mask +  prefix_attention_mask 더함.
        prefix_attention_mask = torch.ones(batch_size, self.pre_seq_len).to(self.bert.device)
        attention_mask = torch.cat((prefix_attention_mask, attention_mask), dim=1)
        outputs = self.bert(input_ids = input_ids,
                token_type_ids=token_type_ids,
                attention_mask=attention_mask,
                past_key_values=past_key_values) # past_key_values로 넘김

        logits = self.qa_outputs(outputs[0])
        start_logits, end_logits = logits.split(1, dim=-1)
        start_logits = start_logits.squeeze(-1).contiguous()
        end_logits = end_logits.squeeze(-1).contiguous()

        return start_logits, end_logits
```
- bert의 past_key_values로 prefix에대한 key 와 value 를 넘겨줘서, 기존 입력 key, value와 연결시키도록 함.
<br> 내부적으로 BertSelfAttention 에서, past_key_values가 있으면 연결시킴.
```
class BertSelfAttention(nn.Module):
    def forward(
        self,
        hidden_states,
        attention_mask=None,
        head_mask=None,
        encoder_hidden_states=None,
        encoder_attention_mask=None,
        past_key_value=None,
        output_attentions=False,
    ):
        mixed_query_layer = self.query(hidden_states)

        # If this is instantiated as a cross-attention module, the keys
        # and values come from an encoder; the attention mask needs to be
        # such that the encoder's padding tokens are not attended to.
        is_cross_attention = encoder_hidden_states is not None

        if is_cross_attention and past_key_value is not None:
            # reuse k,v, cross_attentions
            key_layer = past_key_value[0]
            value_layer = past_key_value[1]
            attention_mask = encoder_attention_mask
        elif is_cross_attention:
            key_layer = self.transpose_for_scores(self.key(encoder_hidden_states))
            value_layer = self.transpose_for_scores(self.value(encoder_hidden_states))
            attention_mask = encoder_attention_mask
        elif past_key_value is not None:
            key_layer = self.transpose_for_scores(self.key(hidden_states))
            value_layer = self.transpose_for_scores(self.value(hidden_states))
            key_layer = torch.cat([past_key_value[0], key_layer], dim=2)
            value_layer = torch.cat([past_key_value[1], value_layer], dim=2)
        else:
            key_layer = self.transpose_for_scores(self.key(hidden_states))
            value_layer = self.transpose_for_scores(self.value(hidden_states))

        query_layer = self.transpose_for_scores(mixed_query_layer)
```
<br> 참고 : [past_key_values 사용](https://zhuanlan.zhihu.com/p/459305102) 


## 테스트
- P-tuning-v2의 prefix-tuning 방식으로 BERT-based-multilingual-cased 모델의 NLI(Natual Language Inference:자연어추론) task에 대해 성능 테스트를 해봄.
- prefix_projection=True로 해서, 2-layer MLP 사용함.(Multi-layer perceptron(다중퍼셉트론)). 
  <br> prefix_projection=False일때는 embedding layer만 사용하는데, 이때 성능은 엄청 떨어짐
  ```
  # prefix_projection=True 일때, 2-layer MLP 구조
  
  (prefix_encoder): PrefixEncoder(
    (embedding): Embedding(20, 768)
    (trans): Sequential(
      (0): Linear(in_features=768, out_features=512, bias=True)
      (1): Tanh()
      (2): Linear(in_features=512, out_features=18432, bias=True)
    )
  )
  ```
- prefix_hidden_size=512로 고정함. 테스트시 768로 늘려도 큰 차이(0.004) 정도 향상이 있었음.
- 테스트는 prefix 사이즈를 20, 100, 200 으로 조정하면서 테스트 해봄. 

|소스명                    |설명                          | 기타              |
|:-------------------------|:-----------------------------|:------------------|
|[bert-p-tuningv2-pefix-nli](https://github.com/kobongsoo/BERT/blob/master/p-tuning/bert-p-tuningv2-pefix-nli.ipynb)|P-TUNING NLI 훈련 예제||
|[bert-p-tuningv2-prefix-nli-test](https://github.com/kobongsoo/BERT/blob/master/p-tuning/bert-p-tuningv2-prefix-nli-test.ipynb)|P-TUNING NLI 테스트 예제||


참고 소스 : https://github.com/THUDM/P-tuning-v2

### Hyperparameter
- epoch : 50
- batch_size: 32
- lr: 3e-5
- max_seq_len : 128
- 말뭉치 : klue-nli-v1.1_train.json(훈련), klue-nli-v1.1_dev.json(평가)

|방식                 |prefix 크기|prefix_hidden_size|prefix_projection|ACC            |훈련속도/1epoch(초) | 훈련시 GPU 사용량(MIB)  |
|:--------------------|----------:|:-----------------|:----------------|--------------:|-------------------:|-----------------------:|
|훈련없음(org)        |x          |x                 |x                |0.338          |x                   |x                     |
|Fine-tuning          |x          |x                 |x                |**0.743**      |**110**             |**8,194**             |
|P-tuning-v2(prefix)  | 20        |512               |False            |0.531          |50                  |5,374                 |
|P-tuning-v2(prefix)  |**20**     |512               |**True**         |**0.692**      |**60**              |**5,507**             |
|P-tuning-v2(prefix)  | 100       |512               |False            |0.548          |73                   |6,411                |
|P-tuning-v2(prefix)  |**100**    |512               |**True**         |**0.695**      |**77**               |**6,546**            |
|P-tuning-v2(prefix)  | 200       |512               |True             |0.694          |93                   |7,691                |
|P-tuning-v2(prefix)  | 200       |**768**           |True             |0.698          |95                   |7,791                |

### 결론
- P-tuning-v2 **prefix 크기를 20으로 할때, Fine-tuning 보다는 성능 5%정도 떨어지지만, 훈련속도 및 GPU 사용량에서는 약 40% 정도 향상이 있음.**
- prefix 크기는 100일때 가장 성능이 좋고, prefix_hidden_size는 768로 하더라도 0.5%정도 미미한 성능 향상이 있음.

### 기타
- [SwissArmy 라이브러리](https://github.com/THUDM/SwissArmyTransformer/tree/cfcd7b738d4231a2d26c2f9a8391c7438c9aaab9) 
: P-Tuning을 라이브러리화 한 소스
