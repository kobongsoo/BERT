import random
import numpy as np
import torch
import time
import os
import numpy as np
from transformers import set_seed
import yaml # pip install PyYAML

import time
import pytz
from datetime import datetime
import re
import string

#로컬파일 삭제
def delete_local_file(filepath:str):
    if len(filepath) < 1:
        return
    
    try:
        os.remove(filepath)
        print(f"File deleted: {filepath}")
    except FileNotFoundError:
        print(f"File not found: {filepath}")
        
# 랜덤한 문자열 만드는 함수 
def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

# 문자열 치환
# 테스트 예제
#input_string = "This is a <br> test &gt; string &lt; with &quot;special&quot; characters &nbsp;&amp;"
#output_string = to_replace(input_string)
#print(output_string)
def to_replace(input_str):
    if input_str is None:
        return None

    return_str = input_str

    return_str = re.sub(r'<br>', '\n', return_str)
    return_str = re.sub(r'&gt;', '>', return_str)
    return_str = re.sub(r'&lt;', '<', return_str)
    return_str = re.sub(r'&quot;', '', return_str)
    return_str = re.sub(r'&nbsp;', ' ', return_str)
    return_str = re.sub(r'&amp;', '&', return_str)

    return return_str


#######################################################################################################
# myutils 클래스
#######################################################################################################
class MyUtils:
    
    def __init__(self, yam_file_path:str):
        self.yam_file_path = yam_file_path
        self.settings = self.get_options()
        self.seed = self.settings['SEED']
        return
      
    #########################################################################################
    # .yaml 파일 호출
    # -in : file_path = .yaml 파일이 있는 경로
    #########################################################################################
    def get_options(self):
        with open(self.yam_file_path, 'r', encoding='utf-8') as file:
            options = yaml.load(file, Loader=yaml.FullLoader)

        return options

    #########################################################################################
    # 로그메시지
    #########################################################################################
    def log_message(self, message:str, log_folder:str=""):
        if len(log_folder) <= 0:
            folder = self.settings['LOG_PATH']
        else:
            folder = log_folder
       
        # 한국 시간대 설정
        korea_tz = pytz.timezone('Asia/Seoul')

        try:
            log_file = datetime.now(korea_tz).strftime('log_%Y-%m-%d.log')
            log_fullpath = folder + log_file

            with open(log_fullpath, 'a') as log:
                # 현재 날짜와 시간 가져오기
                current_time = datetime.now(korea_tz).strftime('%Y-%m-%d %H:%M:%S')
                #print(f"[{current_time}]{message}\n")
                log.write(f"[{current_time}]{message}\n")
        except Exception as e:
            print(f"An error occurred while log_message: {e}")
        

    #########################################################################################
    # seed 설정
    #########################################################################################
    def seed_everything(self):
        random.seed(self.seed)
        os.environ['PYTHONHASHSEED'] = str(self.seed)
        np.random.seed(self.seed)
        torch.manual_seed(self.seed)
        torch.cuda.manual_seed(self.seed)
        torch.backends.cudnn.deterministic = True
        torch.backends.cudnn.benchmark = False
        set_seed(self.seed)

    #########################################################################################
    # GPU 정보
    #########################################################################################
    def GPU_info(self):
        biscuda = torch.cuda.is_available()
        print(biscuda)

        device = str(torch.device('cuda:0' if biscuda else 'cpu'))
        print('device:',device)

        if biscuda:
            print('cuda index:', torch.cuda.current_device())
            print('gpu 개수:', torch.cuda.device_count())
            print('graphic name:', torch.cuda.get_device_name())
            #cuda = torch.device('cuda')

        return device
  
    #########################################################################################
    # ElasticSearch소숫점 score-> 백분율
    #########################################################################################
    def get_es_format_score(self, score:float)->str:
        formatted_score = "100"
        if score < 2.0:
            formatted_score = "{:.0f}".format((score-1)*100)
        return formatted_score

    #########################################################################################
    # 폴더(서브폴더포함)에 있는 파일들의 풀경로를 얻어오는 함수
    # 출처 : https://thispointer.com/python-how-to-get-list-of-files-in-directory-and-sub-directories/
    #########################################################################################
    def getListOfFiles(self, dirName):
        # create a list of file and sub directories 
        # names in the given directory 
        listOfFile = os.listdir(dirName)
        allFiles = list()
        # Iterate over all the entries
        for entry in listOfFile:
            # Create full path
            fullPath = os.path.join(dirName, entry)
            # If entry is a directory then get the list of files in this directory 
            if os.path.isdir(fullPath):
                allFiles = allFiles + self.getListOfFiles(fullPath)
            else:
                allFiles.append(fullPath)

        return allFiles

    #########################################################################################
    # es mapping 정보
    #########################################################################################
    def get_mapping_esindex(self):
        mapping ={
          "settings": {
            "number_of_shards": 2,
            "number_of_replicas": 1,
            "analysis": {
                "analyzer": {
                    "mpower10u_korean_analyzer": {
                        "type": "custom",
                        "tokenizer": "mpower10u_korean_tokenizer",
                        "filter": [
                                "lowercase",
                                "stop",
                                "nori_readingform",
                                "mpower10u_korean_pos"
                        ]
                    }
                },
                "tokenizer": {
                    "mpower10u_korean_tokenizer": {
                        "type": "nori_tokenizer",
                        "decompound_mode": "discard"
                    }
                },
                "filter": {
                    "mpower10u_korean_pos": {
                        "type": "nori_part_of_speech",
                        "stoptags": [
                            "J", "E", "XSA", "XSN", "XSV"
                        ]
                    }
                }
            }
          },
           "mappings": {
            "dynamic": "true",
            "_source": {
              "enabled": "true"
            },
            "properties": {
              "query": {
                "type": "text"
              },
              "response": {
                "type": "text"
              },
              "classification" : {
                "type": "text"
              },
              "qr_vector": {
                "type": "dense_vector",
                "dims": self.settings['E_OUT_DIMENSION']
              }
            }
          }
        }

        return mapping
