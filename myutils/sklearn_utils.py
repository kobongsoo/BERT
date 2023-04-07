import os
import random
import numpy as np
import torch
import torch.nn as nn
import logging
import warnings
from tqdm import tqdm
from torch import Tensor
from typing import Dict, List, Optional
from sklearn.cluster import KMeans
from sklearn_extra.cluster import KMedoids
#------------------------------------------------------------------------------------------------------------------------------
# KMedoids = k-대표값 군집 분석
# embeddings 을 클러스터링 처리해서 평균 임베딩을 구함
# - in : embeddings : 클러스터링 처리할 임베딩 벡터 2차원 배열 (예:(11,768))
# - in : num_clusters: 클러스터링 몇개로 묶을지 (*무조건 embeddings 계수 11보다 작아야 함)
# - in : outmode: mean=평균임베딩값, medoid=대표임베딩값.
# - out : 각 클러스터링 후 생성된 평균 임베딩 벡터 2차원 배열 (예: (num_clusters, 768), *무조건 0번지는 num_clusters 임)
#------------------------------------------------------------------------------------------------------------------------------
def kmedoids_clustering_embedding(embeddings, num_clusters:int, seed:int=111, outmode:str="medoid", debug:bool=False)->np.array:
    
    assert num_clusters > 1, f'error!! num_clusers{num_clusers}값은 1보다 크게 입력해야 합니다.'
    assert outmode == "mean" or outmode == "medoid", f'error!! outmode 입력으로 mean(평균), medoid(대표) 만 입력해야 합니다.=>입력 outmode={outmode}'
        
     # embedding 계수가 > num_clusers 보다 큰 경우에만 처리 
    if len(embeddings) > num_clusters:
        clustering_model = KMedoids(n_clusters=num_clusters, random_state=seed)
        clustering_model.fit(embeddings)
        cluster_assignment = clustering_model.labels_

        if debug == True:
            print(f'*embeddings.shape: {embeddings.shape}')
        
        # 클러스터링 목록을 저장해 둠.
        cluster_id_list = [[] for i in range(num_clusters)]
        for sentence_id, cluster_id in enumerate(cluster_assignment):
            cluster_id_list[cluster_id].append(sentence_id)
            
        #if not cluster_id_list[0]:
        #    print('cluster_id_list=>none')
            
        if debug == True:
            print('cluster_id_list')
            print(cluster_id_list)
            print()
    
        embeddings_list = []
        
        # 각 클러스터의 대표 샘플(index), 즉 대표 임베딩값 구함.
        if outmode == "medoid":      # 클러스터 안에서 가장 중심에 위치한 데이터 포인트
            medoids = clustering_model.medoid_indices_
            for i, medoid in enumerate(medoids):
                if debug == True:
                    print(f'[{i}] medoid: {medoid}')
                embeddings_list.append(embeddings[medoid])
        # 클러스터링 목록을 불러와서 평균 임베딩 구함.    
        else:            
            for cluster_sub in cluster_id_list:
                cluster_vector = np.zeros((embeddings.shape[1]))
                if not cluster_sub: # cluster_sub 리스트가 비어 있으면 그냥 저장.
                    embeddings_list.append(cluster_vector)
                else:    
                    count = 0
                    for sentence_id in cluster_sub:
                        cluster_vector += embeddings[sentence_id] 
                        count += 1
                    if count > 0:
                        cluster_vector /= count
                    embeddings_list.append(cluster_vector)

        embedding_arr = np.array(embeddings_list).astype('float32')
        
        if debug == True:
            print(f'*len(embedding_arr):{len(embedding_arr)}')
            print(f'*embedding_arr.shape:{embedding_arr.shape}\n')
            #print(f'*embedding_arr[0]:{embedding_arr[0]}\n')
            
        return embedding_arr
    
    else:
        return embeddings
    

#------------------------------------------------------------------------------------------------------------------------------
# KMeans = k-평균 군집 분석
# embeddings 을 클러스터링 처리해서 평균 임베딩을 구함
# - in : embeddings : 클러스터링 처리할 임베딩 벡터 2차원 배열 (예:(11,768))
# - in : num_clusters: 클러스터링 몇개로 묶을지 (*무조건 embeddings 계수 11보다 작아야 함)
# - in : outmode: mean=평균임베딩값, max=최대임베딩값.
# - out : 각 클러스터링 후 생성된 평균 임베딩 벡터 2차원 배열 (예: (num_clusters, 768), *무조건 0번지는 num_clusters 임)
#------------------------------------------------------------------------------------------------------------------------------
def clustering_embedding(embeddings, num_clusters:int, seed:int=111, outmode:str="mean", debug:bool = False)->np.array:
    
    assert num_clusters > 1, f'error!! num_clusers{num_clusers}값은 1보다 크게 입력해야 합니다.'
    assert outmode == "mean" or outmode == "max", f'error!! outmode 입력으로 mean, max 만 입력해야 합니다.=>입력 outmode={outmode}'
    
    # embedding 계수가 > num_clusers 보다 큰 경우에만 처리 
    if len(embeddings) > num_clusters:
        clustering_model = KMeans(n_clusters=num_clusters, init='k-means++', random_state=seed)
        clustering_model.fit(embeddings)
        cluster_assignment = clustering_model.labels_

        if debug == True:
            print(f'*embeddings.shape: {embeddings.shape}')
        
        # 클러스터링 목록을 저장해 둠.
        cluster_id_list = [[] for i in range(num_clusters)]
        for sentence_id, cluster_id in enumerate(cluster_assignment):
            cluster_id_list[cluster_id].append(sentence_id)
            
        if debug == True:
            print('cluster_id_list')
            print(cluster_id_list)
            print()
    
    
        embeddings_list = []
        
        if outmode == "mean":      # 클러스터링 목록을 불러와서 평균 임베딩 구함.
            for cluster_sub in cluster_id_list:
                cluster_vector = np.zeros((embeddings.shape[1]))
                count = 0
                for sentence_id in cluster_sub:
                    cluster_vector += embeddings[sentence_id] 
                    count += 1
                if count > 0:
                    cluster_vector /= count
                embeddings_list.append(cluster_vector)

            embedding_arr = np.array(embeddings_list).astype('float32')
        
        elif outmode == "max": # 클러스터링 목록을 불어와서 최대값 임베딩 구함.
            for cluster_sub in cluster_id_list:
                arr_list = []
                for sentence_id in cluster_sub:
                    arr_list.append(embeddings[sentence_id])

                arr = np.array(arr_list).astype('float32')
                
                #print(arr)
                #print()
                
                # 임베딩 벡터가 2개 이상인 경우에만 max 최대값 구함.
                if len(arr_list) > 1:
                    max_index = np.argmax(np.linalg.norm(arr, axis=1))# 최대값을 갖는 벡터의 인덱스를 찾습니다.
                    cluster_max_vector = embeddings[max_index] # 최대값을 갖는 벡터를 출력합니다.
                else: # 임베딩 벡터가 1개인 경우에는 그대로 출력
                    cluster_max_vector = arr[0]
                    
                #print(f'max_index:{max_index}')
                #print(f'max_vector:{cluster_max_vector}')
                #print()
                    
                embeddings_list.append(cluster_max_vector)
            
            embedding_arr = np.array(embeddings_list).astype('float32')
        
        if debug == True:
            print(f'*len(embedding_arr):{len(embedding_arr)}')
            print(f'*embedding_arr.shape:{embedding_arr.shape}\n')
            #print(f'*embedding_arr[0]:{embedding_arr[0]}\n')
            
        return embedding_arr
    
    else:
        return embeddings
    
            
# main    
if __name__ == '__main__':
    main()
    