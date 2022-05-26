## 양자화(Quantization) 기법 
- 모델의 파라메터를 줄여, 추론 시간과 사용 메모리를 줄이는 모델 경량화 기법
- 양자화 기법 자체는 CPU 환경에서 추론시간을 줄이는데 목적이 있다. (어차피 훈련은 GPU 환경을 CPU가 대체할수는 없음)
  <br>따라서 **양자화 기법은 GPU 환경에서는 불가**.
- 일반적으로, pytorch, tensorflow에서 모델 파라메터의  **float32 를 int8 로 변환** 함으로써, 경량화 시킨다.
- 동적 양자화, 정적 양자화, 양자화 Training 등이 있음.

### 참고자료 : 
- [딥러닝 양자화 정리](https://velog.io/@jooh95/%EB%94%A5%EB%9F%AC%EB%8B%9D-Quantization%EC%96%91%EC%9E%90%ED%99%94-%EC%A0%95%EB%A6%AC)
- [파이토치-BERT 모델 동적 양자화하기](https://tutorials.pytorch.kr/intermediate/dynamic_quantization_bert_tutorial.html)
- [허깅페이지-ONNX런타임을 위한 최적의 추론](https://huggingface.co/docs/optimum/onnxruntime/modeling_ort)

***
### 1. 동적 양자화(Dynamic Quantization)
-  Pytorch 및 ONNX 런타임등을 이용해 동적 양자화 시킨 결과 기존 모델과 비교하여 **용량, 추론시간 등은 30% 정도 향상**이 있으며, 
   <br>**정확도는 1~3% 정도 감소**함.
  
### 1-1. Pytorch 사용
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

# quantized_model 추론
with torch.no_grad():
        # 모델 실행
        outputs = quantized_model(input_ids=input_ids, 
                       attention_mask=attention_mask,
                       token_type_ids=None,
                       labels=labels)
```
- torch 를 이용한 동적 양자화 기법은 추론시 cpu만 지원함.(따라서 **GPU 서버에서는 사용불가**, 다른 CPU 서버에서는 적용해볼만함)
- 양자화 된 모델을 저장후 huggingface 모델에서 불러와서 추론해보면 정확도가 엄청 떨어짐(사용불가).
- 단 원본 모델을 양자화 모델로 변환후 저장하지 않고 추론시에는 정확도가 약간 떨어짐.
- 아래표는 bert-multilingle-cased(bert 다국어버전)를 양자화 시킨후 저장하지 않고 추론한 테스트임

|구분|용량|추론시간|NLI Acc|
|:---|:---|:------|:-------|
|bert|819M|158초|71%|
|양자화처리|574M|123초|68.5%|

예제 : [Dynamic-Quantization](https://github.com/kobongsoo/BERT/blob/master/Quantization/Dynamic-Quantization.ipynb)

***
### 1-2. ONNX 런타임 사용
- **ONNX(Open Neural Network Exchange)는,Tensorflow, PyTorch 와 같은, 서로 다른 DNN 프레임워크 환경에서 만들어진 모델들이 호환 될 수 있도록 하는 플렛폼**
- ONNX 모델로 만들면, 어떤 DNN 프레임워크 환경 환경에서든지 사용 가능 함.
- 동적 양자화시 ONNX Runtime을 이용하여 기존모델->ONNX 모델로 변환->ONNX 모델 동적 양자화 할수 있음.
- ONNX 와 ONNX 런타임 설치 해야함.
```
!pip install datasets
!pip install optimum
!pip install optimum[onnxruntime]
!pip install optimum[onnxruntime-gpu]  #gpu 사용인 경우
```
- 기존 distilbert 모델을 ONNX 모델로 동적 양자화 하는 코드.  
```
from optimum.onnxruntime import ORTConfig, ORTQuantizer
from optimum.onnxruntime.configuration import AutoQuantizationConfig

# 기존 bert 모델 경로 
model_checkpoint = "./distilbert-0331-TS-nli-0.1-10"

# 동적 양자화인 경우 is_static = False로 해야 함.
qconfig = AutoQuantizationConfig.arm64(is_static=False, per_channel=False)

# 분류 모델인 경우에는 feature="sequence-classification"
quantizer = ORTQuantizer.from_pretrained(model_checkpoint, feature="sequence-classification")

# ONNX 모델로 만들고 양자화 함
quantizer.export(
    onnx_model_path="model.onnx",   # ONNX 모델 출력 경로
    # onnx 양자화 모델이 생성되는 경로(이름은 model.onnx로 해야함=>그래야 huggingface 함수 이용시 경로만 지정해도 자동으로 불어옴)
    onnx_quantized_model_output_path="./distilbert-TS/model.onnx",  
    quantization_config=qconfig,
)
```
- 아래표와 예시는 HuggingFace 와 ONNX 런타임을 가지고, Distilbert-NLI 추론 모델을 동적 양자화 시킨 후 성능 비교한 내용임.

|구분|용량|추론시간|NLI Acc|
|:---|:---|:------|:-------|
|distilbert-NLI|672M|1,321초|73.1%|
|양자화처리    |548M|959초  |72.4%|

예제 : [ONNX-Dynamic-Quantization](https://github.com/kobongsoo/BERT/blob/master/Quantization/ONNX_Dynamic_Quantization.ipynb)
