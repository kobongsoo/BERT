## AI 에서 양자화(Quantization) 
- 모델의 파라메터를 줄여, 추론 시간과 사용 메모리를 줄이는 모델 경량화 기법
- 일반적으로, pytorch, tensorflow에서 data type float32 를 int8 로 변환 함으로써, 경량화 시킨다.
- 동적 양자화, 정적 양자화, 양자화 Training 등이 있음.

### 1. 동적 양자화(Dynamic Quantization)
- 기존 모델을 가지고, 특정 레이어에 data type을 줄인다.
- torch.quantization.quantize_dynamic를 가지고 동적 양자화 하는 예시

```
# 원본 모델 불러옴
tokenizer = BertTokenizer.from_pretrained(vocab_path, do_lower_case=False)
model = BertForSequenceClassification.from_pretrained(model_path, num_labels=3)

# 양자화 처리 
# => Linear 레이어에 대해 int8 로 양자화 처리
# => 원본 모델은 gpu 설정하면 안됨
quantized_model = torch.quantization.quantize_dynamic(
    model, {torch.nn.Linear}, dtype=torch.qint8
)
```
- torch 를 이용한 동적 양자화 기법은 추론시 cpu만 지원함.(따라서 **GPU 서버에서는 사용불가**, 다른 CPU 서버에서는 적용해볼만함)
- 양자화 된 모델을 저장후 huggingface 모델에서 불러와서 추론해보면 정확도가 기본으로 떨어짐.
- 단 원본 모델을 양자화 모델로 변환후 저장하지 않고 추론시에는 정확도가 약간 떨어짐.
- 확실히 용량은 819MB->574MB 정도로 약 70% 정도 줌. 

예제 : [Dynamic-Quantization](https://github.com/kobongsoo/BERT/blob/master/Quantization/Dynamic-Quantization.ipynb)
