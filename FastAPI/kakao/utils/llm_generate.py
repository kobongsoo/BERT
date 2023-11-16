import time
import os
import json
import requests

import openai     # pip install "openai<1.0.0"
import sseclient  # pip install sseclient-py

from requests.exceptions import Timeout
from functools import lru_cache  # 캐싱

# 캐싱을 위한 256 데코레이터 설정
#@lru_cache(maxsize=256)  
#-----------------------------------------
# GPT를 이용한 text 생성2 
# => 아래 1번 함수와 차이점은 timeout(초)를 설정할수 있음.
#-----------------------------------------
def generate_text_davinci(gpt_model:str, prompt:str,  
                          timeout:int=30, stream:bool=False):
    
    error = 0
    answer:str = ""
    start_time = time.time()
    
    data = {
        'model': gpt_model,
        'prompt': prompt,
        'max_tokens': 350,
        'temperature':0.5,# temperature 0~2 범위 : 작을수록 정형화된 답변, 클수록 유연한 답변(2는 엉뚱한 답변을 하므로, 1.5정도가 좋은것 같음=기본값은=1)
        'stream': stream,
        #'top_p': 0.1,      # 기본값은 1 (0.1이라고 하면 10% 토큰들에서 출력 토큰들을 선택한다는 의미)
        #'frequency_penalty':1, # 일반적으로 나오지 않는 단어를 억제하는 정도
        #'presence_penalty': 0.5 # 동일한 단어나 구문이 반복되는 것을 억제하는 정도
    }
    
    print(f'data:{data}')

    try:
        response = requests.post(
            'https://api.openai.com/v1/completions',
            headers={'Accept': 'text/event-stream', 'Authorization': f'Bearer {openai.api_key}'},
            json=data,
            stream=stream,
            timeout=timeout  # Set your desired timeout in seconds
        )
        
        # 스트림 아닐때
        if stream == False:
            response.raise_for_status()  # Raise an HTTPError for bad responses
            output = json.loads(response.text)
            answer = output["choices"][0]["text"]
        else:  # 스트림 적용일때 => 한글자(토큰)씩 출력됨.
            client = sseclient.SSEClient(response)
            for event in client.events():
                if event.data != '[DONE]':
                    chunk = json.loads(event.data)['choices'][0]['text']
                    answer += chunk
                    #print(chunk)
                    
        # 소요된 시간을 계산합니다.
        end_time = time.time()
        elapsed_time = "{:.2f}".format(end_time - start_time)
        print(f'time:{elapsed_time}, answer:{answer}')
        
        return answer, error
    except Timeout:
        answer = f'The request timed out.=>max:{timeout}'
        error = 1001
        return answer, error
    except Exception as e:
        answer = f"Error in API request: {e}"
        error = 1002
        return answer, error
    

# 캐싱을 위한 256 데코레이터 설정
#@lru_cache(maxsize=256)  
#-----------------------------------------
# GPT를 이용한 text 생성2 
# => 아래 1번 함수와 차이점은 timeout(초)를 설정할수 있음.
#-----------------------------------------
def generate_text_GPT2(gpt_model:str, prompt:str, system_prompt:str="", 
                       timeout:int=30, stream:bool=False):
    
    error = 0
    answer:str = ""
    start_time = time.time()
    
    messeges=[]
    if system_prompt:
        messeges = [
                {"role": "system", "content": system_prompt},
                {'role': 'user','content': prompt}
            ]
    else:
        messeges = [
                {'role': 'user','content': prompt}
            ]
    
    data = {
        'model': gpt_model,
        'messages': messeges,
        'max_tokens': 350,
        'temperature':0.5,# temperature 0~2 범위 : 작을수록 정형화된 답변, 클수록 유연한 답변(2는 엉뚱한 답변을 하므로, 1.5정도가 좋은것 같음=기본값은=1)
        'stream': stream,
        #'top_p': 0.1,      # 기본값은 1 (0.1이라고 하면 10% 토큰들에서 출력 토큰들을 선택한다는 의미)
        #'frequency_penalty':1, # 일반적으로 나오지 않는 단어를 억제하는 정도
        #'presence_penalty': 0.5 # 동일한 단어나 구문이 반복되는 것을 억제하는 정도
    }
    
    print(f'data:{data}')

    try:
        response = requests.post(
            'https://api.openai.com/v1/chat/completions',
            headers={'Content-Type': 'application/json', 'Authorization': f'Bearer {openai.api_key}'},
            json=data,
            stream=stream,
            timeout=timeout  # Set your desired timeout in seconds
        )
        
        # 스트림 아닐때
        if stream == False:
            response.raise_for_status()  # Raise an HTTPError for bad responses
            output = json.loads(response.text)
            answer = output["choices"][0]["message"]["content"]
        else:  # 스트림 적용일때 => 한글자(토큰)씩 출력됨.
            client = sseclient.SSEClient(response)
            for event in client.events():
                if event.data != '[DONE]':
                    chunk = json.loads(event.data)['choices'][0].get('delta', {}).get('content', '')
                    answer += chunk
                    print(chunk)
                    
        # 소요된 시간을 계산합니다.
        end_time = time.time()
        elapsed_time = "{:.2f}".format(end_time - start_time)
        print(f'time:{elapsed_time}')
        
        return answer, error
    except Timeout:
        answer = f'The request timed out.=>max:{timeout}'
        error = 1001
        return answer, error
    except Exception as e:
        answer = f"Error in API request: {e}"
        error = 1002
        return answer, error
    
#-----------------------------------------
# GPT를 이용한 text 생성
#-----------------------------------------
# 캐싱을 위한 데코레이터 설정
#@lru_cache(maxsize=256)
def generate_text_GPT(gpt_model:str, prompt:str, system_prompt:str="",
                     stream:bool=False):
    
    error = 0
    answer:str = ""
    assert gpt_model, f'gpt_model is empty'
    assert prompt, f'prompt is empty'
    
    start_time = time.time()
    #print(f'len(messages):{len(messages)}') 
    #print()
    
    # 메시지 설정
    messages=[]
    if system_prompt:
        messages = [
                {"role": "system", "content": system_prompt},
                {'role': 'user','content': prompt}
            ]
    else:
        messages = [
                {'role': 'user','content': prompt}
            ]
         
    try:
        # ChatGPT-API 호출하기
        response = openai.ChatCompletion.create(
            model=gpt_model,
            messages=messages,  
            max_tokens=350, # 토큰 수 
            temperature=0.5,  # temperature 0~2 범위 : 작을수록 정형화된 답변, 클수록 유연한 답변(2는 엉뚱한 답변을 하므로, 1.5정도가 좋은것 같음=기본값은=1)
            stream=stream,
            #top_p=0.1, # 기본값은 1 (0.1이라고 하면 10% 토큰들에서 출력 토큰들을 선택한다는 의미)
            #frequency_penalty=1, # 일반적으로 나오지 않는 단어를 억제하는 정도
            #presence_penalty=0.5 # 동일한 단어나 구문이 반복되는 것을 억제하는 정도
            #stop=["다.","다!"] # . 나오면 중단
        )

        if stream==False:
            answer = response['choices'][0]['message']['content']  # + '다.' # 뒤에 '다' 붙여줌.
        else:
            for line in response:
                chunk = line['choices'][0].get('delta', {}).get('content', '')
                if chunk:
                    answer += chunk
                    print(chunk)
                    #print(chunk, end='')
            
        # 소요된 시간을 계산합니다.
        end_time = time.time()
        elapsed_time = "{:.2f}".format(end_time - start_time)
        print(f'time:{elapsed_time}')
        
        return answer, error
    except Exception as e:
        answer = f"Error in API request: {e}"
        error = 1002
        return answer, error
#------------------------------------------------------------------

# main    
if __name__ == '__main__':
    main()