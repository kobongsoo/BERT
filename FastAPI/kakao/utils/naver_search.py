import time
import os
import sys
import json
import re
import urllib.request

class NaverSearchAPI:
    def __init__(self, client_id:str, client_secret:str):
        assert client_id, f'client_id is empty'
        assert client_id, f'client_secret is empty'
        
        self.client_id = client_id
        self.client_secret = client_secret

    def normalize(self, text:str):
        if text:
            text = text.replace('<b>', '')  # <b> 치환
            text = text.replace('</b>', '') # </b> 치환

            # 한글,영문,숫자,.,,.(),[],{} 아니면 제거
            text_filter = re.compile('[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9,\.\?\!\"\'-()\[\]\{\}]')
            text = text_filter.sub(' ', text)
            return text
        else: 
            return ""

    #=================================================
    # 네이버 검색 API
    # - 출처: https://developers.naver.com/docs/serviceapi/search/blog/blog.md#%EB%B8%94%EB%A1%9C%EA%B7%B8
    # classification 
    # - blog:블로그, news:뉴스, webkr: 웹문서, kin : 지식인,  encyc : 백과사전, doc:전문자료
    # display=10 : 10개 검색
    #=================================================
    def search_naver(self, query:str, classification:str='webkr', display:int=10):
        assert query, f'query is empty'
        
        links = []
        encText = urllib.parse.quote(query)
        url = f"https://openapi.naver.com/v1/search/{classification}?query={encText}&display={display}"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", self.client_id)
        request.add_header("X-Naver-Client-Secret", self.client_secret)

        response = urllib.request.urlopen(request)
        rescode = response.getcode()

        if rescode == 200:
            response_body = response.read().decode('utf-8')
            response_dict = json.loads(response_body)

            context = ""
            for res in response_dict['items']:
                title = res['title']
                descript = res['description']
                link = res['link']
                links.append(link)
                
                title = self.normalize(title)
                descript = self.normalize(descript)
                context += title + '\n' + descript + '\n\n'

            return context, links, 0
        else:
            print("Error Code:" + rescode)
            return "", links, rescode

