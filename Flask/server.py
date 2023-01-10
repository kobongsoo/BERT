#================================================================
# Flask BERT 서버 
# - Flask 서버로 임베딩(/embed), 요약 임베딩(/summarize)을 수행하는 코드
# - 실행 : python server.py
# - 접속 및 임베딩 테스트 : curl_test.ipynb 실행 혹은 cmd에서 curl 이용(사용방법은 아래 참조)
# 참고 : https://github.com/dmmiller612/bert-extractive-summarizer/blob/master/server.py
#
# pip install flask
# pip install flask-cors  # flask Cross-Origin Resource Sharing( CORS는 시스템 수준에서 타 도메인 간 자원 호출을 승인하거나 차단하는 것을 결정하는 것)
# pip install argparse
#
# curl 사용법 : 
# 참고 : https://twpower.github.io/223-attach-data-to-curl-command
#curl -X<VERB> '<PROTOCOL>://<HOST>:<PORT>/<PATH>?<QUERY_STRING>' -d '<BODY>'
# d 옵션을 사용하고 POST 방식으로 text 형태의 자료를 보내는 예제(BODY에 한글을 입력하면 안되고, 반드시 인코딩된 한글문장을 입력해야 함)
# curl -XPOST -H "Content-Type: text/plain" -d "raw text data" http://127.0.0.1:9999/test?param1=value
#
# -d 옵션을 사용하고 POST 방식으로 x-www-form-urlencoded 형태의 자료를 보내는 예제
# curl -XPOST -H "Content-Type: application/x-www-form-urlencoded" -d "param1=value1&param2=value2" http://127.0.0.1:5000/test
#
# -d 옵션을 사용하고 POST 방식으로 JSON 형태의 자료를 보내는 예제
#curl -XPOST -H "Content-Type: application/json" http://127.0.0.1:9999/test?num_sentence=2 -d '
#{
#   "text": "my name is tiger. tiger is big animal",
#}
#'
# 참고: https://losskatsu.github.io/programming/py-flask-korean/#2-%EC%84%9C%EB%B2%84-flask-%ED%95%9C%EA%B8%80-post-%EC%9A%94%EC%B2%AD-%EB%B0%9B%EA%B8%B0
#==================================================================================================================================

from flask import Flask, request, jsonify, abort, make_response
from flask_cors import CORS
import argparse
from typing import List
from urllib import parse
import numpy

import torch
from summarizer.sbert import SBertSummarizer                # 추출 요약 모델
from sentence_transformers import SentenceTransformer, util # sbert 임베딩 모델

from elasticsearch import Elasticsearch
from elasticsearch.helpers import bulk
import time

import sys
sys.path.append('..')
from myutils import seed_everything, GPU_info
device = GPU_info()             #device = torch.device('cpu')
seed_everything(111)

#==================================================================================================================================
app = Flask(__name__, template_folder='')
app.config['JSON_AS_ASCII'] = False     # flask 서버에서 json으로 응답시, 한글깨짐 방지
CORS(app)
#==================================================================================================================================
@app.route('/', methods=['GET'])
def hello_world():
    return 'Hello World!'

#==================================================================================================================================
# 입력 문장 임베딩 벡터 구하고 response
# => IN : 문장, OUT : 임베딩 벡터
#==================================================================================================================================
@app.route('/embed', methods=['POST'])
def embedding():
    # json으로 text 를 받음.
    args = request.json
    text = args['text']
    data = parse.unquote(text, 'utf-8')
    if not data:
         abort(make_response(jsonify(message="Request must have raw text"), 400))
            
    print(f'data:{data}/type:{type(data)}')
    
    # embedding 후 벡터값 구하고, 이을 string으로 json 형식으로 전송함.
    embed = embed_text(data)
    
    return jsonify({
            'embed': embed
            })
#==================================================================================================================================
# 요약문 처리 후 embedding 구하고 response
# => IN : 요약할 긴 문장, OUT : 요약문, 임베딩 벡터
#==================================================================================================================================
@app.route('/summarize', methods=['POST'])
def summarize_text():
    args = request.json
    print(args)
    
    min_length =  int(request.args.get('min_length', 25))
    max_length = int(request.args.get('max_length', 500))
    num_sentence = int(request.args.get('num_sentence', 3))   
    print(f'min_length: {min_length}, max_length: {max_length}, num_sentence: {num_sentence}')
    
    text = args['text']
    data = parse.unquote(text, 'utf-8')
    if not data:
         abort(make_response(jsonify(message="Request must have raw text"), 400))
    
    print(f'data:{data}/type:{type(data)}')
   
    # 요약문 구함
    summarize = summarizer(data, 
                        min_length=min_length, 
                        max_length=max_length,
                        num_sentences=num_sentence)
    
    # 만약 요약문 추출 못하면 원본 담음.
    if not summarize:
        summarize = data
        print(f'summarize is empty!!=>copy data to summarize')
    print(f'summarize: {summarize}')
          
    # 요약문에 평균 임베딩을 구함함
    embed = paragraph_index(summarize)
    #print(f'embed: {embed}')
    
    return jsonify({
            'summarize': summarize,
            'embed': embed
            })
#==================================================================================================================================
# 검색문장 vector 구하고, ElasticSearch(엘라스틱서치: ES)에서 유사도 측정 검색 결과 response
# => IN : 검색 문장, -esurl={ESurl}, OUT: 검색결과
#==================================================================================================================================
@app.route('/search', methods=['POST'])
def search_text():
    # json 파일 파싱
    args = request.json
    print(args)
    
    # 인자로 넘어온 arg에서 esurl 추출함
    esurl = request.args.get('eshost', "http://localhost:9200/")
    esindex = request.args.get('index', "indexname")
    essearchsize = int(request.args.get('size', 3))
    print(f'esurl: {esurl}, esindex: {esindex}, essearchsize: {essearchsize}\r\n')
    
    # json으로 넘어온 데이터에서 texe 추출함
    text = args['text']
    data = parse.unquote(text, 'utf-8')
    if not data:
         abort(make_response(jsonify(message="Request must have raw text"), 400))
    print(f'data:{data}/type:{type(data)}\r\n')
    
    # 1. elasticsearch 접속
    es = Elasticsearch(esurl)
    print(f'esinfo:\n{es.info()}\r\n')
    
    # 2. 검색 문장 embedding 후 벡터값 
    start_embedding_time = time.time()
    query_vector = embed_text([data])[0]
    end_embedding_time = time.time() - start_embedding_time
    print("*embedding time: {:.2f} ms\r\n".format(end_embedding_time * 1000)) 
    
    print(f'*vector:\n{query_vector}\r\n')
    
     #3.쿼리 구성
    script_query = {
        "script_score":{
            "query":{
                "match_all": {}},
            "script":{
                "source": "cosineSimilarity(params.query_vector, doc['summarize_vector']) + 1.0",  # 뒤에 1.0 은 코사인유사도 측정된 값 + 1.0을 더해준 출력이 나옴
                "params": {"query_vector": query_vector}
            }
        }
    }
    
    #print('query\n')
    #print(script_query)
    
    # 4. 실제 ES로 검색 쿼리 날림
    start_search_time = time.time()
    response = es.search(
        index=esindex,
        body={
            "size": essearchsize,
            "query": script_query,
            "_source":{"includes": ["title", "summarize"]}
        }
    )
    end_search_time = time.time() - start_search_time
    print("*search time: {:.2f} ms\r\n".format(end_search_time * 1000)) 
    
    print(f'response:\n{response}\r\n')
    
    # 5. es 종료
    es.transport.close()
    
    return response

#==================================================================================================================================
# main(메인 함수) : 임베딩 모델, 추출요약 모델 설정, vector 함수 정의, 평균 vector 함수 정의
# => IN: -host=IP, -port=9999, -sbert={SBERT 모델 경로}
#==================================================================================================================================
if __name__ == '__main__':
    
    # args 처리
    parser = argparse.ArgumentParser(description='')
    parser.add_argument('-host', dest='host', help='', default='0.0.0.0')  # host 파싱
    parser.add_argument('-port', dest='port', help='', default=9999)       # port 파싱
    parser.add_argument('-sbert', dest='sbert', help='sbert model full path', default='../../../model/sbert/klue-sbert-v1.0')
    
    args = parser.parse_args()
    print(f'sbert path:{args.sbert}')

    # 문장 임베딩 모델 정의
    embedder = SentenceTransformer(args.sbert, device=device)
    print(f'embedder:{embedder}')
     
    # 추출 요약 모델 정의
    summarizer = SBertSummarizer(args.sbert)
    print(f'summairzer:{summarizer}')
    
    # embedding 모델에서 vector를 구하는 함수    
    def embed_text(input):
        vectors =  embedder.encode(input, convert_to_tensor=True)
        return [vector.numpy().tolist() for vector in vectors]

    # 여러문장일때 평균 vector를 구하는 함수
    def paragraph_index(paragraph):
        avg_paragraph_vec = numpy.zeros((1,768))
        sent_count = 0
    
        # ** kss로 분할할때 히브리어: מר, 기타 이상한 특수문자 있으면 에러남. 
        # 따라서 여기서는 그냥 . 기준으로 문장을 나누고 평균을 구함
        # 하나의 문장을 읽어와서 .기준으로 나눈다.
        sentences = [sentence for sentence in paragraph.split('. ') if sentence != '']
        for sent in sentences:
            # 문장으로 나누고, 해당 vector들의 평균을 구함.
            avg_paragraph_vec += embed_text([sent])
            sent_count += 1

        avg_paragraph_vec /= sent_count
        return avg_paragraph_vec.tolist()

    # app 실행
    app.run(host=args.host, port=int(args.port))
