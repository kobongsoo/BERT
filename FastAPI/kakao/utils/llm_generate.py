import torch
import time
import os
import numpy as np
from tqdm.notebook import tqdm

import asyncio
import openai

#-----------------------------------------
# GPT를 이용한 text 생성
#-----------------------------------------
def generate_text_GPT(gpt_model:str, prompt:str, system_prompt:str, messages:list):
    
    assert gpt_model, f'gpt_model is empty'
    assert prompt, f'prompt is empty'
    
    #print(f'len(messages):{len(messages)}') 
    #print()
    
    #-----------------------------------------
    # *** gpt에 메시지는 계속 대화 내용이 유지가 되므로, 비용이 발생함.
    # 따라서 최근 2개 대화만 유지함.
    #if len(messages) >= 2:
    #    messages = messages[len(messages)-2:]  # 최근 2개의 대화만 가져오기
  
    messages = []  # 무조건 최근대화 초기화
    #messages.append( {"role": "user", "content": prompt})
    #-----------------------------------------
         
    # 메시지 설정
    messages = [
            {"role": "system", "content": system_prompt}, # 시스템 프롬프트.
            {"role": "user", "content": prompt}
        ]
            
    print(f'messages:{messages}')

    # ChatGPT-API 호출하기
    response = openai.ChatCompletion.create(
        model=gpt_model,
        messages=messages,
        max_tokens=512, # 토큰 수 
        temperature=1,  # temperature 0~2 범위 : 작을수록 정형화된 답변, 클수록 유연한 답변(2는 엉뚱한 답변을 하므로, 1.5정도가 좋은것 같음=기본값은=1)
        top_p=0.1, # 기본값은 1 (0.1이라고 하면 10% 토큰들에서 출력 토큰들을 선택한다는 의미)
        frequency_penalty=0.5, # 일반적으로 나오지 않는 단어를 억제하는 정도
        presence_penalty=0.5 # 동일한 단어나 구문이 반복되는 것을 억제하는 정도
        #stop=["다.","다!"] # . 나오면 중단
    )

    #print(response)
    #print()
    #answer = response['choices'][0]['message']['content'] + '다.' # 뒤에 '다' 붙여줌.
    answer = response['choices'][0]['message']['content']
    return answer
#------------------------------------------------------------------

# main    
if __name__ == '__main__':
    main()