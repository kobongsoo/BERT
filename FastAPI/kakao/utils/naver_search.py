import time
import os
import sys
import json
import re
import kss
import torch
import numpy as np
import urllib.request
from utils import embedding
from sentence_transformers import util

class NaverSearchAPI:
    def __init__(self, client_id:str, client_secret:str):
        assert client_id, f'client_id is empty'
        assert client_id, f'client_secret is empty'
        
        self.client_id = client_id
        self.client_secret = client_secret

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

            context:str = ""
            for res in response_dict['items']:
                link:dict={}
                title = res['title']
                descript = res['description']
                link['link'] = res['link']
                link['score'] = 0
                links.append(link)
                
                title = self.normalize(title)
                descript = self.normalize(descript)
                context += title + '\n' + descript + '\n\n'

            return context, links, 0
        else:
            print("Error Code:" + rescode)
            return "", links, rescode
     
    #=================================================
    # 네이버 검색 API 확장
    # - 출처: https://developers.naver.com/docs/serviceapi/search/blog/blog.md#%EB%B8%94%EB%A1%9C%EA%B7%B8
    # classification 
    # - blog:블로그, news:뉴스, webkr: 웹문서, kin : 지식인,  encyc : 백과사전, doc:전문자료
    # display=10 : 10개 검색
    #=================================================
    def search_naver_ex(self, query:str, bi_encoder, float_type:str="float16", 
                        classification:list=['webkr', 'news', 'blog'], display:int=10, top_k:int=10):
        
        assert query, f'query is empty'
        assert float_type, f'float_type is empty'
        
        contexts:list = []
        texts1:list=[]
        links1:list=[]
        
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
                    text1 = f"{title}\n{descript}"
                    
                    text2 = self.normalize2(text1)
                    if text2 == "":
                        continue
                       
                    links1.append(link)
                    texts1.append(text2)
            else:
                print("Error Code:" + rescode)
                return "", links1, rescode
        
        # 각 검색 text들에 대한 임베딩 구함.
        links:list = []
        context:str = ""
        
        if len(texts1) > 0:
            if top_k > len(texts1):
                top_k = len(texts1)
                
            embeddings = embedding(texts1, bi_encoder, float_type)
            tensor_embed = torch.Tensor(embeddings)
            cos_scores = util.pytorch_cos_sim(tensor_queryembed, tensor_embed)[0]
            
            # 스코어 오름차순으로 tok_k 만큼만 contexts에 추가함.
            # We use np.argpartition, to only partially sort the top_k results
            top_results = np.argpartition(-cos_scores, range(top_k))[0:top_k]
            
            for idx in top_results[0:top_k]:
                link:dict={}
                score = cos_scores[idx] 
                
                if score > 0.4:
                    link['link'] = links1[idx]['link'].strip()
                    link['score'] = "{:.2f}".format(score)
                    links.append(link)
                    context += texts1[idx].strip() + '\n\n'   
                 
        return context, links, 0

