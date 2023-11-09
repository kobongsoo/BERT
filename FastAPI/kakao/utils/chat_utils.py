import torch
import time
import os
import numpy as np
from tqdm.notebook import tqdm

import asyncio

#---------------------------------------------------------------------------
# 이전 답변/응답 문장들중 오래된것 제거하며, 문장을 구분자 <hr> 로 구분해서 답변/응답 문단을 만든는 함수
#---------------------------------------------------------------------------
def remove_prequery(prequery:str, remove_count:int=4):
    
    if prequery:
        # prequery는 5개 이상이면 무조건 오래된 문장/답변은 제거함
        hr_count = prequery.count("<hr>")
        #print(f'4) hr_count:{hr_count}')

        remove_count -= 1
        if hr_count > remove_count: # 4 개 이상이면 <hr>로 구분해서 오래된 문장/답변은 제거함.
            hr_list = prequery.split("<hr>") # <hr>로 구분
            hr_list.pop(0)                   # 제일 오래된 <hr> 구분해서 첫번째 문장/답변은 제거.
            prequery = "<hr>".join(hr_list)  # 다시 hr 구분된 문장/답변 조합.
            #print(f'5) prequery:{prequery}')
    
    return prequery

#---------------------------------------------------------------------------
# context 문자열을 입력받아서,\n\n 문단으로 구분후, 문단 맨 첫번째 문장 title들을
# 조합해서 title_str 만들고 ,return 하는 함수
# -> title에 해당하는 문서가 있으면 url링크 생성함
#---------------------------------------------------------------------------
def get_title_with_urllink(context:str, data_folder:str=''):
    
    titles_str:str = ''  # titles를 str형으로 만들어서 전송함. 
    
    # context에서 title만 뽑아냄
    titles = []
    context_list = context.split("\n\n")  #\n\n으로 구분.
    for context1 in context_list:
        context1 = context1.strip()
        context2 = context1.split("\n")
        if len(context2) > 0:
            titles.append(context2[0].strip())
    
    # 중복 제거하면서 순서유지.
    titles2 = []
   
    for idx, title in enumerate(titles):
        if title and title not in titles2:
            titles2.append(title)
            
            # 실제 title에 해당하는 파일이 경로에 존재하는 경우에만 url 링크 생성함.
            if data_folder and title:
                if os.path.isfile(data_folder + title + ".txt"):

                    # html뿌릴때 중간에 쌍따옴표가 있으면 에러 나므로, "(쌍따옴표) 대신에 ;s&s; 로 치환해서 전송함. 
                    # => 이후 chat01.html에서 ;s&s; 문자열을 다시 "(쌍따옴표)로 치환해줌.
                    # => 참고로 " 대신에 홑따옴표(') 해도 되는데, openPopup 함수는 반드시 "(쌍따옴표)로 묶어져야 동작하므로 이렇게 처리함.
                    title = f"<a href='javascript:void(0);' onclick=;s&s;;openPopup('{ENV_URL}/doc?name={title}');;s&s;>{title}</a>"
                    #title = f"<a href='/doc?name={title}'>{title}</a>"
                
            if idx == 0:
                titles_str = title
            else:
                titles_str += ', ' + title
                
    return titles_str
#---------------------------------------------------------------------------

# main    
if __name__ == '__main__':
    main()