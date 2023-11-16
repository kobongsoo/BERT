import time
import os
import json
import numpy as np
from tqdm.notebook import tqdm
import urllib.request
from googletrans import Translator

#=================================================================
# 구글 번역 서비스 (무료)
# 설치 : !pip install googletrans==4.0.0-rc1
#=================================================================
def translate_google(text:str, source_lang:str, target_lang:str):
        
    text1 = text
    source_lang1 = source_lang
    target_lang1 = target_lang
    
    assert text1, f'Error:text is empty'
    assert source_lang1, f'Error:source_lang is empty'
    assert target_lang1, f'Error:source_lang is empty'

    start_time = time.time()
    translator = Translator()    
    res = translator.translate(text1, src=source_lang1, dest=target_lang1)

    # 소요된 시간을 계산합니다.
    end_time = time.time()
    elapsed_time = "{:.2f}".format(end_time - start_time)
    response_text = res.text.strip('"')
    print(f'\t# translate_google=>response:{response_text}, time:{elapsed_time}, text:{text1}, source:{source_lang1}, target:{target_lang1}, res:{res}')

    return response_text

#=================================================================
# 네이버 파파고 번역 서비스
# => https://developers.naver.com/docs/papago/papago-nmt-overview.md
#client_id = "" # 개발자센터에서 발급받은 Client ID 값
#client_secret = ""       # 개발자센터에서 발급받은 Client Secret 값
# api 1일 호출량 : 10,000 글자로 제한.
#
# query 대해 한국어 -> 영어로 번역 => source_lang='ko', target_lang='en'
# query 대해 영어 -> 한국어 번역 => source_lang='en', target_lang='ko'
#=================================================================
def translate_naver(text:str, source_lang:str, target_lang:str, 
              client_id:str, client_secret:str):
    
    out_query:str = ""
    
    assert text, f'Error:text is empty'
    assert source_lang, f'Error:source_lang is empty'
    assert target_lang, f'Error:source_lang is empty'
    assert client_id, f'Error:client_id is empty'
    assert client_secret, f'Error:client_id is empty'
        
    start_time = time.time()

    encText = urllib.parse.quote(text)

    #data = "source=ko&target=en&text=" + encText
    data = f"source={source_lang}&target={target_lang}&text={encText}"
    #print(f'data:{data}')
    url = "https://openapi.naver.com/v1/papago/n2mt"

    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)

    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()

    if(rescode==200):
        response_body = response.read()
        response_body.decode('utf-8')

        # JSON 문자열을 딕셔너리로 변환
        my_response = json.loads(response_body)
        out_query = my_response["message"]["result"]["translatedText"].strip("'")
        print(out_query)

    else:
        print("Error Code:" + rescode)

     # 소요된 시간을 계산합니다.
    end_time = time.time()
    formatted_elapsed_time = "{:.2f}".format(end_time - start_time)
    print(f'time:{formatted_elapsed_time}')
    
    return out_query
        

# main    
if __name__ == '__main__':
    main()