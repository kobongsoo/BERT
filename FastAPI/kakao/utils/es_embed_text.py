import torch
import time
import os
import numpy as np
import asyncio
import numpy as np

from sentence_transformers import models
from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk

from typing import Dict, List, Optional
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids

from .es_model import bi_encoder
from .es_embed import embed_text, embedding

class ES_Embed_Text:
    
    def __init__(self, es_url:str, index_name:str, mapping, bi_encoder, float_type:str="float16", uid_min_score:float=10.0):
        assert es_url, f'es_url is empty'
        assert index_name, f'index_name is empty'
        assert mapping, f'mapping is empty'
        
        self.es_url = es_url
        self.index_name = index_name
        self.mapping = mapping
        self.bi_encoder = bi_encoder
        self.float_type = float_type
        self.uid_min_score = uid_min_score
        
        try:
            # 1.elasticsearch 접속
            self.es = Elasticsearch(self.es_url) 
        except Exception as e:
            msg = f'Elasticsearch:{self.es_url}=>{e}'
            print(msg)
            
        self.create_index() # 인덱스만듬
        
        return
        
    ###########################################################
    # 인덱스 생성/삭제
    ###########################################################
    ## 인덱스 생성 => 매핑
    def create_index(self):
        if not self.es.indices.exists(index=self.index_name):
            return self.es.indices.create(index=self.index_name ,body=self.mapping)

    ## 인덱스 자체 삭제
    def delete_index(self):
        if self.es.indices.exists(index=self.index_name):
            return self.es.indices.delete(index=self.index_name)
        
    ###########################################################
    # 인데스에 데이터 추가 
    ###########################################################
    def insert(self, doc:dict, doc_type:str="_doc"):
        return self.es.index(index=self.index_name, doc_type=doc_type, body=doc)

    ############################################################
    ## 인덱스 내의 데이터 업데이트=>_id 에 데이터 업데이트
    ############################################################
    def update(self, esid, doc, doc_type):

        body = {
            'doc': doc
        }

        res=self.es.update(index=self.index_name, id=esid, body=body, doc_type=doc_type)
        return res

    ############################################################
    ## 인덱스 내의 데이터 삭제 => query 이용(예: data = {'title': '제주도'})
    ############################################################
    def delete(self, doc:dict):
        if doc is None:  # data가 없으면 모두 삭제
            data = {"match_all":{}}
        else:
            data = {"match": doc}

        body = {"query": data}
        return self.es.delete_by_query(index=self.index_name, body=body)

    ############################################################
    ## 인덱스 내의 데이터 삭제 => id 이용
    ############################################################
    def delete_by_id(self, esid):
        return self.es.delete(index=self.index_name, id=esid)
       
    # ############################################################
    #쿼리에 대해 일반검색해서 임베딩 검색할 후보군 10개 목록 uids를 얻기
     ############################################################
    def search_uids(self, size:int=10, data=None):
        
        if data is None: #모든 데이터 조회
            data = {"match_all":{}}
        else:
            data = {"match": data}

        body = {
            "size": size,
            "query": data,
            "_source":{"includes": ["answer","response"]}
        }

        #print(f'body:{body}')
        
        response = None
        response = self.es.search(index=self.index_name, body=body)

        #print(f'uid_min_score:{self.uid_min_score}')
        #print(f'res:{response}')

        answerlist = []
        count = 0
        docs = []

        for hit in response["hits"]["hits"]: 
            tmp = hit["_source"]["answer"]

            # 중복 제거
            if tmp and tmp not in answerlist:
                answerlist.append(tmp)
                doc = {}  #dict 선언

                score = hit["_score"]
                if score > self.uid_min_score: 
                    doc['_id'] = hit["_id"]
                    doc['answer'] = hit["_source"]["answer"]      # contextid 담음
                    doc['response'] = hit["_source"]["response"]      # text 담음.
                    doc['score'] = score
                    docs.append(doc)
                    count += 1

        uids = []
        for doc in docs:
            uids.append(doc['_id'])

        return uids, docs

    ############################################################
    ## 쿼리 스크립트 만들기
    ############################################################
    def make_query_script(self, query_vector, class_list:list=None, uid_list:list=None)->str:
        # 문단별 10개의 벡터와 쿼리벡터를 서로 비교하여 최대값 갖는 문단들중 가장 유사한  문단 출력
        # => script """ 안에 코드는 java 임.
        # => "queryVectorMag": 0.1905 일때 100% 일치하는 값은 9.98임(즉 10점 만점임)

        # uid_list가 있는 경우에는 해당하는 목록만 검색함
        if uid_list:
            query = { "bool" :{ "must": [ { "terms": { "_id": uid_list } } ] } }
        elif class_list:
            query = { "bool" :{ "must": [ { "terms": { "classification": class_list } } ] } }
        else: # uid_list가 있는 경우에는 해당하는 목록만 검색함
            query = { "match_all" : {} }

        script_query = {
            "script_score":{
                "query":query,
                "script":{
                    "source": "cosineSimilarity(params.queryVector, doc['answer_vector']) + 1.0",  # 뒤에 1.0 은 코사인유사도 측정된 값 + 1.0을 더해준 출력이 나옴
                    "params": {"queryVector": query_vector}
                }
            }
        }

        return script_query

    ############################################################
    ## 쿼리 검색
    ############################################################
    def embed_search(self, query:str, classification:str):
        
        assert query, f'query is empty'
        assert classification, f'classification is empty'
        
        query = query.strip()
        classification = classification.strip()
        
        # 1.내용검색으로 쿼리와 맞는 이전질문들을 10개 뽑아냄
        #data = {'answer': query, 'classification': classification}
        #uids, docs = self.search_uids(size=10, data=data)
        
        #if len(uids) < 1:
        #    return docs
            
        # 2. 쿼리 임베딩 구함.
        embed_query = embed_text(model=self.bi_encoder, paragraphs=query, return_tensor=False).astype(self.float_type)
        
        # 3. 기본 벡터 쿼리 만듬
        script_query = self.make_query_script(query_vector=embed_query, class_list=[classification]) 
        #print(f'script_query:{script_query}')
        
        # 4. 실제 ES로 검색 쿼리 날림
        response = self.es.search(
            index=self.index_name,
            body={
                "size": 1,
                "query": script_query,
                "_source":{"includes": ["answer","response"]}
            }
        )
        
        # 5. 결과 리턴
        # - 쿼리 응답 결과값에서 _id, _score, _source 등을 뽑아내고 내림차순 정렬후 결과값 리턴
        #print(f'\t==>embed_search:\n{response}')

        answerlist = []
        count = 0
        docs = []
        for hit in response["hits"]["hits"]: 
            tmp = hit["_source"]["answer"]

            # 중복 제거
            if tmp and tmp not in answerlist:
                answerlist.append(tmp)
                doc = {}  #dict 선언
                doc['_id'] = hit["_id"]
                doc['answer'] = hit["_source"]["answer"]      # contextid 담음
                doc['response'] = hit["_source"]["response"]      # text 담음.
                doc['score'] = hit["_score"]
                docs.append(doc)

                count += 1
                if count >= 3:
                    break
                    
        return docs # 쿼리,  rfilename, rfiletext, 스코어 리턴 
    
    ############################################################
    ## 인덱스에 데이터 추가
    ## doc1 = {'answer':'2023년 미국 대통령은?', 'response':'조 바이든이다.'}
    ############################################################
    def delete_insert_doc(self, doc:dict, classification:str):
        
        error:int = 0
        doc1 = doc
        #print(f'doc:{doc1}')
        #print(f'type: {type(doc1)}')
        
        assert classification, f'classification is empty'
        
        if len(doc1) < 1:
            return 'doc is empty', 1001
        
        try:
            # 인덱스 생성
            self.create_index()
            
            answer = doc1['answer'].strip()
            if len(answer) < 1:
                return 'answer is empty', 1001
            
            '''
            # 해당 질문과 완전 동일한 질문이 있는지 검색(term 으로 검색)
            answer_id:str = ""
            answer_type:str = ""
            body = {
                "query": {
                    "term": {
                        "answer": answer
                    }
                }
            }
            response = self.es.search(index=self.index_name, body=body)
            '''
            # 쿼리에 대해 임베딩 구하고, 가자 유사한 쿼리를 얻음.
            # 제목에 대해 임베딩 구함
            embeddings = embed_text(model=self.bi_encoder, paragraphs=answer, return_tensor=False).astype(self.float_type)    

            # 3. 기본 벡터 쿼리 만듬
            script_query = self.make_query_script(query_vector=embeddings, class_list=[classification]) 
            #print(f'script_query:{script_query}')

            # 4. 실제 ES로 검색 쿼리 날림
            response = self.es.search(
                index=self.index_name,
                body={
                    "size": 1,
                    "query": script_query,
                    "_source":{"includes": ["answer","response"]}
                }
            )
            
            #print(f'response:response')
            
            for hit in response["hits"]["hits"]: 
                preanswer_id = hit["_id"]
                preanswer_type=hit['_type']
                preanswer_score = hit['_score']
                preanswer = hit["_source"]["answer"]
                preresponse = hit["_source"]["response"]
                print(f'\t==>[delete_insert_doc]=>preanswer_id:{preanswer_id}, preanswer:{preanswer}, preanswer_score:{preanswer_score}')
                
                # 기존 질문과 스코어가 1.80 이상이면 해당 질문과 답변, 질문벡터등을 업데이트 함.=>삭제하고 insert 함.(dense_vector은 업데이트 안됨)
                if preanswer_score >= 1.80:
                    res = self.delete_by_id(esid=preanswer_id)              
                    print(f'\t==>[delete_insert_doc]=>self.delete_by_id=>res:{res}')
                break
                               
            # 인덱스 추가
            doc1['answer_vector'] = embeddings
            doc1['classification'] = classification
            res = self.insert(doc=doc1, doc_type="_doc")
            print(f'\t==>[delete_insert_doc]=>self.insert=>res:{res}')
            return res, 0
        
        except Exception as e:
            error = 1002
            msg = f'delete_insert_doc:=>{e}'
            return msg, error