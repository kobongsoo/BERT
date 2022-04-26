### BERT 모델의 출력 차원(dimension) 줄이가

#### 1. 필요성
- Sementic Search 혹은 분류 모델 구축시 문장들간 유사도 측정을 위해  문장들의 임베딩(BERT는 기본 임베딩 768임)들을 비교하는 코사인 유사도를 사용한다.
- 이때 임베딩 차원은 768이므로, 이때 **한 문장당 768byte이 저장공간(DB, 메모리 등)이 필요함**
- 따라서 **데이터가 많은 경우 메모리 낭비가 심하므로, 이를 128처럼 줄이는 방법이 필요함**

##### 2. 코드
- dimension을 줄이는 방법은 모델의 출력에 fullyconnect 레이어를 추가한다.
- Activation function은 Tanh 이용

```
class MyDistilBertModel(nn.Module):
    
    def __init__(self, 
                model_path: str,      # 기존 huggingface distilbert 모델 경로
                in_dim: int = 768,    # 입력 dimension(기본=768)
                out_dim: int = 768,   # 출력 dimension(기본=768)
                nlabel: int = 2,      # 혹시 classificaiton에 사용하는 경우 label 계수  
                drop_rate: int = 0.1):# dropout 비율(기본=0.1)
        
        
        super().__init__()  #nn.Module 호출시 반드시 호출해야함
        
        # bert 모델 정의 : huggingface에 distilbert pretrained 모델 불러옴
        self.model = AutoModel.from_pretrained(model_path)
        
        
        self.activefunc = nn.Tanh()            # activefunc 함수 정의 : activation function은 Tanh 이용
        self.drop = nn.Dropout(drop_rate)      # dropout 레이어 정의
        self.fc = nn.Linear(in_dim, out_dim)   # fullyconnect 레이어 정의 : 입력 dim, 출력 dim
        
        #self.classifier = nn.Linear(out_dim, nlabel)  # classification 레이어 정의
        
    def forward(self,
               input_ids,
               #token_type_ids = None,  #distilbert에는 token_type_ids가 없다.
               attention_mask 
               ):
        output = self.model(input_ids, attention_mask)
        h = output.last_hidden_state  #distilber는 맨마지막 hidden state만 리턴한다.
      
        out1 = self.drop(h)
        out2 = self.activefunc(self.fc(out1))
        
        #logits = self.classifier(self.drop(pooled_h))
        return out2
```
#### 3. 테스트
- cosin 유사도 측정시, 768이나 128일때 별반 차이 없은 것으로 여겨짐. 
