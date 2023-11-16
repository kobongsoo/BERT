import random
import numpy as np
import torch
import time
import os
import numpy as np
import logging
from tqdm.notebook import tqdm
from transformers import set_seed
import yaml # pip install PyYAML

import time
import pytz
from datetime import datetime
#########################################################################################
# 로그메시지
#########################################################################################
def log_message(settings, message:str):
    
    folder = settings['LOG_PATH']
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
# .yaml 파일 호출
# -in : file_path = .yaml 파일이 있는 경로
#########################################################################################
def get_options(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        options = yaml.load(file, Loader=yaml.FullLoader)
    
    return options

#########################################################################################
# seed 설정
#########################################################################################
def seed_everything(seed):
    random.seed(seed)
    os.environ['PYTHONHASHSEED'] = str(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    set_seed(seed)

#########################################################################################
# GPU 정보
#########################################################################################
def GPU_info():
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
# mlogging 설정
#########################################################################################
def mlogging(
    loggername: str = 'mlogger',  #logger 구분자
    logfilename: str = None       #log 저장 파일명
):
    import time
    
    # logfilepath가 None이면 현재날짜로 로그파일 생성
    if logfilename is None:
        logfilepath = time.strftime('mlog_%Y-%m-%d.log', time.gmtime())
    else:   
        logfilepath = logfilename + time.strftime('_%Y-%m-%d.log', time.gmtime()) 
        
    # 폴더가 없으면 생성
    dir_path = os.path.dirname(logfilepath)  
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    
    # 로그 생성
    logger = logging.getLogger(loggername)

    # 로그의 출력 기준 설정(INFO, ERROR, WARNING 출력함)
    logger.setLevel(logging.INFO)

    # log 출력 형식
    #formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s \n%(message)s')
    formatter = logging.Formatter('%(asctime)s[%(levelname)s] \n%(message)s')

    # log 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)

    # log를 파일에 출력
    file_handler = logging.FileHandler(logfilepath)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
    
    return logger

# main    
if __name__ == '__main__':
    main()