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
    def log_message(self, message:str):

        folder = self.settings['LOG_PATH']
       
        # 한국 시간대 설정
        korea_tz = pytz.timezone('Asia/Seoul')

        try:
            log_file = datetime.now(korea_tz).strftime('log_%Y-%m-%d.log')
            log_fullpath = folder + log_file

            with open(log_fullpath, 'a') as log:
                # 현재 날짜와 시간 가져오기
                current_time = datetime.now(korea_tz).strftime('%Y-%m-%d %H:%M:%S')
                print(f"[{current_time}]{message}\n")
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

        device = torch.device('cuda:0' if biscuda else 'cpu')
        print('device:',device)

        if biscuda:
            print('cuda index:', torch.cuda.current_device())
            print('gpu 개수:', torch.cuda.device_count())
            print('graphic name:', torch.cuda.get_device_name())
            #cuda = torch.device('cuda')

        return device
    
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
              "answer": {
                "type": "text"
              },
              "response": {
                "type": "text"
              },
              "classification" : {
                "type": "text"
              },
              "answer_vector": {
                "type": "dense_vector",
                "dims": self.settings['E_OUT_DIMENSION']
              }
            }
          }
        }

        return mapping
