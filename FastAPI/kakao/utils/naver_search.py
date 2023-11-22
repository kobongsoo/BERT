import time
import os
import sys
import json
import re
import kss
import torch
import numpy as np
import urllib.request
import requests
from utils import embedding
from sentence_transformers import util
from bs4 import BeautifulSoup

class NaverSearchAPI:
    def __init__(self, client_id:str, client_secret:str):
        assert client_id, f'client_id is empty'
        assert client_id, f'client_secret is empty'
        
        self.client_id = client_id
        self.client_secret = client_secret

    def find_descript(self, descript, contexts):
        for context in contexts:
            if descript in context['descript']:
                return True
        return False
    
    def get_text_navernews(self, url:str):
        assert url, f'url is empty'
        text: str = ""
        
        if url.startswith("https://n.news.naver.com/"):
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            findtext = soup.find_all(name='div', class_='_article_body')
            
            if findtext:
                text = findtext[0].get_text()
                text = text.replace('/n/n', '')  # /n/n 치환
                
                if len(text) > 512:
                    text = text[0:512]
                return text.strip()
            else:
                return text
        else:
            return text

    def normalize2(self, text:str, removelen:int=8):
        out:str = ""
        for sentence in kss.split_sentences(text): 
            remove_text = ['...','!!']
            for word in remove_text:  
                sentence = sentence.replace(word, '')
                
            if sentence != '' and len(sentence) > removelen: 
                    out += sentence +'\n'
                
        return out

    def normalize(self, text:str):
        if text:
            text = text.replace('<b>', '')  # <b> 치환
            text = text.replace('</b>', '') # </b> 치환

            # 한글,영문,숫자,.,,.(),[],{} 아니면 제거
            #text_filter = re.compile('[^ㄱ-ㅎㅏ-ㅣ가-힣a-zA-Z0-9,\.\?\!\"\'-()\[\]\{\}]')
            #text = text_filter.sub(' ', text)
            return text
        else: 
            return ""

    #=================================================
    # 네이버 검색 API
    # - 출처: https://developers.naver.com/docs/serviceapi/search/blog/blog.md#%EB%B8%94%EB%A1%9C%EA%B7%B8
    # classification 
    # - blog:블로그, news:뉴스, webkr: 웹문서, kin : 지식인,  encyc : 백과사전, doc:전문자료
    # - display=10 : 10개 검색
    #=================================================
    def search_naver(self, query:str, classification:list=['news', 'webkr', 'blog'], display:int=10):
        assert query, f'query is empty'

        links:list = []
        contexts:list = []
 
        encText = urllib.parse.quote(query)
        
        for classi in classification:
            if classi == "webkr":
                url = f"https://openapi.naver.com/v1/search/{classi}?query={encText}&display={display}"
            else:
                url = f"https://openapi.naver.com/v1/search/{classi}?query={encText}&display={display}&sort=date"  # sort=date : 날짜순 정렬, sort=sim 정확도순
      
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", self.client_id)
            request.add_header("X-Naver-Client-Secret", self.client_secret)
    
            response = urllib.request.urlopen(request)
            rescode = response.getcode()
    
            if rescode == 200:
                response_body = response.read().decode('utf-8')
                response_dict = json.loads(response_body)
    
                #print(response_dict)
                #print()
                for res in response_dict['items']:
                    context:dict={}
                    title = res['title']
                    descript = res['description']
                    context['link'] = res['link']
                    context['score'] = "0"                  

                    title = self.normalize(title)
                    descript = self.normalize(descript)

                    # 중복된 descript 있으면 추가하지 않음
                    if self.find_descript(descript, contexts) == True:
                        continue
                        
                    context['title'] = title

                    # naver뉴스 웹크롤링해서 내용이 있으면 descript에 저장
                    text = self.get_text_navernews(res['link'])
                    if text:
                        context['descript'] = text
                    else:
                        context['descript'] = descript
                    
                    contexts.append(context)
            else:
                print("Error Code:" + rescode)
                return "", rescode

        return contexts, 0
     
    #=================================================
    # 네이버 검색 API 확장
    # - 출처: https://developers.naver.com/docs/serviceapi/search/blog/blog.md#%EB%B8%94%EB%A1%9C%EA%B7%B8
    # classification 
    # - blog:블로그, news:뉴스, webkr: 웹문서, kin : 지식인,  encyc : 백과사전, doc:전문자료
    # display=10 : 10개 검색
    #=================================================
    def search_naver_ex(self, query:str, bi_encoder, float_type:str="float16", 
                        classification:list=['news', 'webkr', 'blog'], display:int=10, top_k:int=10):
        
        assert query, f'query is empty'
        assert float_type, f'float_type is empty'
        
        contexts:list = []   
        links1:list = []
        links:list = []
        titles:list = []
        descripts:list = []
        
        encText = urllib.parse.quote(query)
        
        # 쿼리에 대한 임베딩 벡터 구함.
        queryembed = embedding(query, bi_encoder, float_type)
        tensor_queryembed = torch.Tensor(queryembed) # cos 비교를 위해 tensor로 변환
            
        for classi in classification:
            if classi == "webkr":
                url = f"https://openapi.naver.com/v1/search/{classi}?query={encText}&display={display}"
            else:
                url = f"https://openapi.naver.com/v1/search/{classi}?query={encText}&display={display}&sort=date"  # sort=date : 날짜순 정렬, sort=sim 정확도순
                
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", self.client_id)
            request.add_header("X-Naver-Client-Secret", self.client_secret)

            response = urllib.request.urlopen(request)
            rescode = response.getcode()

            if rescode == 200:
                response_body = response.read().decode('utf-8')
                response_dict = json.loads(response_body)

                for res in response_dict['items']:
                    link:dict = {}
            
                    title = res['title']
                    descript = res['description']
                    link['link'] = res['link']
                    link['score'] = 0
                    
                    
                    title = self.normalize(title)
                    descript = self.normalize(descript)
                    title = self.normalize2(title)
                    descript = self.normalize2(descript)

                    # 중복된 descript 있으면 추가하지 않음
                    if descript in descripts:
                        continue
                        
                    titles.append(title)
                    links1.append(link)

                    # naver뉴스 웹크롤링해서 내용이 있으면 descript에 저장
                    text = self.get_text_navernews(res['link'])
                    if text:
                        descripts.append(text)
                    else:
                        descripts.append(descript)
            else:
                print("Error Code:" + rescode)
                return "", rescode
        
        # 각 검색 text들에 대한 임베딩 구함.
        
        if len(titles) > 0:
            if top_k > len(titles):
                top_k = len(titles)
                
            embeddings = embedding(titles, bi_encoder, float_type)
            tensor_embed = torch.Tensor(embeddings)
            cos_scores = util.pytorch_cos_sim(tensor_queryembed, tensor_embed)[0]
            
            # 스코어 오름차순으로 tok_k 만큼만 contexts에 추가함.
            # We use np.argpartition, to only partially sort the top_k results
            top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
            
            for idx in top_results[0:top_k]:
                context:dict={}
                score = cos_scores[idx] 
                
                if score > 0.40:
                    context['link'] = links1[idx]['link'].strip()
                    context['score'] = "{:.2f}".format(score)
                    context['title'] = titles[idx].strip()
                    context['descript'] = descripts[idx].strip()
                    contexts.append(context)
                 
        return contexts, 0

