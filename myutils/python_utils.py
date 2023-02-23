import os
import random
import numpy as np
from typing import Dict, List, Optional

import numpy as np

#---------------------------------------------------------------
# 2차원 배열을 (210,768) 입력 받아서, 5, 10, 15, 5, 10, 15,... 단위로 차레대로 배열을 분리해서
# 각 분리된 배열의 평균을 구하는 함수
# - in: embed_arr : 입력받은 2차원 배열 예:(210,768)
# - in: divide_arrs : 해당 배열을 몇개씩 나눌지 값 배열 (예: [2,3] = 1번째는 2개 평균, 2번째는 3개 평균, 3번째는 다시 2개 평균, ....구함)
# - out: 평균구한 2차원 배열 예 (9, 768) 
#---------------------------------------------------------------
def divide_arr_avg_exten(embed_arr, divide_arrs = [5,10,15], debug=False):
    boundaries = []
    boundaries.append(0)  
    embed_arr_len = len(embed_arr)
    arr_count = 0          
    stop = False
    
 
    
    # 바운드리 구함. 
    # 예: [1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24]

    if embed_arr_len <= divide_arrs[0]:
        boundaries.append(embed_arr_len)
    else:
        for i in range(256):
            for divide_len in divide_arrs:
                arr_count += divide_len
                if arr_count <= embed_arr_len:
                    if arr_count not in boundaries:
                        boundaries.append(arr_count)
                else:
                    if embed_arr_len not in boundaries:
                        boundaries.append(embed_arr_len)  
                    stop = True
                    break
            if stop==True:
                break

    # 인덱스 범위 구함
    # 예: [(1, 2), (2, 4), (4, 6), (6, 8), (8, 10), (10, 12), (12, 14), (14, 16), (16, 18), (18, 20), (20, 22), (22, 24)]
    index_list = [(boundaries[i], boundaries[i+1]) for i in range(len(boundaries) - 1)]
    
    # 각 단계에서의 평균값을 저장할 리스트 생성
    result = []

    # 각 인덱스 범위에 해당하는 값의 평균 계산
    for start, end in index_list:
        # 해당 범위의 평균값 계산
        mean = np.mean(embed_arr[start:end], axis=0)
        # 결과 리스트에 추가
        result.append(mean)

    if debug == True:
        divide_arrs
        print(f'[divide_arr_avg_exten]divide_arrs:{divide_arrs}')
        print(f'[divide_arr_avg_exten]len:{len(embed_arr)}')
        print(f'[divide_arr_avg_exten]boundaries:{boundaries}')
        print(f'[divide_arr_avg_exten]index_list:{index_list}')
        print(f'[divide_arr_avg_exten]result_len:{len(result)}')
        
    return np.array(result).astype('float32')

#---------------------------------------------------------------
# 2차원 배열을 (210,768) 입력 받아서, 10만큼씩 잘라, 각 잘라진 배열의 평균을 구하는 함수
# - in: embed_arr : 입력받은 2차원 배열 예:(210,768)
# - in: divide_len : 해당 배열을 몇개씩 나눌지 10이면 213을 10씩 분리해서 21개+1개에 대해 평균을 구함.
# - out: 평균구한 2차원 배열 예 (9, 768) 
#---------------------------------------------------------------
def divide_arr_avg(embed_arr, divide_len: int=10):
    
    DIVIDE_LEN = divide_len
    EMBED_ARR_COUNT = int(len(embed_arr)/DIVIDE_LEN) # 임베딩 할 계수
    EMBED_ARR_LEN = DIVIDE_LEN * EMBED_ARR_COUNT
    #print(f'*len:{len(embed_arr)}/divide_count:{embed_arr_count}')

    result = []
    for i in range(EMBED_ARR_COUNT):
        tmp = embed_arr[i*DIVIDE_LEN:(i+1)*DIVIDE_LEN]
        result.append(tmp.mean(axis=0))

    # 나머지 남은 토큰 평균 구함.    
    if len(embed_arr) > EMBED_ARR_LEN:
        tmp = embed_arr[EMBED_ARR_LEN: len(embed_arr)]
        result.append(tmp.mean(axis=0))
        
    return np.array(result).astype('float32')

#---------------------------------------------------------------
# a와 b 리스트를 합치는 함수
# - in: a와b 리스트는 1차원이어야하며, 계수도 같아야 함.
#---------------------------------------------------------------
def merge_list(a:list, b:list):
    merge_list = [row_a + row_b for row_a, row_b in zip(a, b)]
    return merge_list

#------------------------------------------------------------------------------------------------------------------------------
# dataframe 랜덤하게 샘플링하는 함수
# =>IN: df=dataframe, num=샘플링계수, seed=seed 값
#------------------------------------------------------------------------------------------------------------------------------
def df_sampling(df, num:int=3, seed: int=111):
    df_sample = df.sample(num, random_state=seed)
    df_sample = df_sample.reset_index(drop=True)  # index는 0부터 
    
    return df_sample
    
#------------------------------------------------------------------------------------------------------------------------------
# 2차원배열 입력받아서 각 배렬의 최대값 혹은 최소값 합을 리턴하는 함수
# 예: [[2,3,4],[5,3,1]] 입력 => 4+5=9 리턴
# => IN : array=2차원 배열, bmax=True이면 최대값 합 리턴, False=이면 최소값 합 리턴
#------------------------------------------------------------------------------------------------------------------------------
def sum_of_array_2d(array, bmin: bool=False):
    if bmin == False:
        values = np.amax(array, axis=1) # 2차원 배열 => np.array([[2,3,4],[4,3,2]])에서 최대값을 구함.
    else:
        values = np.amin(array, axis=1) # 2차원 배열 => np.array([[2,3,4],[4,3,2]])에서 최소값을 구함.
    
    sum_of_values = np.sum(values)
    
    return sum_of_values

#------------------------------------------------------------------------------------------------------------------------------
# 1차원리스트를 입력받아서 각 배열에서 max 혹은 min 값을 갖는 indext번지를 k개 출력하는 함수
# 예: listdata=[2,3,5,4,2,3,4,1], k= 3입력 => [2,3,6] 리턴
# => IN : listdata=1차원 리스트, k=출력계수, bmax=True이면 최대값 목록 리턴, False=이면 최소값 목록 리턴
#------------------------------------------------------------------------------------------------------------------------------
def index_of_list(listdata, k: int=1, bmin: bool=False):

    arr = np.array(listdata) # list를 배열로 변환

    if bmin == False:
        indexs = np.argsort(-arr)[:k]# 배열에서 max 값을 갖는 index를  k개 출력함
    else:
        indexs = np.argsort(arr)[:k] # 배열에서 min 값을 갖는 index를  k개 출력함

    return indexs

#------------------------------------------------------------------------------------------------------------------------------
# 리스트 중복 제거 (순서유지 안함)
#------------------------------------------------------------------------------------------------------------------------------
def remove_duplicate_lists_not_order(lst):
    return list(set(lst))

#------------------------------------------------------------------------------------------------------------------------------
# 리스트 중복 제거 (순서유지함)
#------------------------------------------------------------------------------------------------------------------------------
def remove_duplicate_lists_order(lst):
    return list(dict.fromkeys(lst))