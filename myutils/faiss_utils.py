import faiss

#===================================================================================== 
# faiss 인덱스 생성
# =>in: embedding: 임베딩 벡터 목록 (100,768) => 2차원 numpy.array 배열
# =>in : method: faiss 인덱스 생성 방식(0= Cosine Similarity 적용(IndexFlatIP 사용), 1= Euclidean Distance 적용(IndexFlatL2 사용))
# =>out : index : faiss에서 생성된 인덱스
#===================================================================================== 
def fassi_index(embeddings, method): 
    
    if method == 0:  # Cosine Similarity 적용
        index = faiss.IndexFlatIP(embeddings.shape[1]) # cosine simirity 인덱스 생성(768)
        faiss.normalize_L2(embeddings) # *cosine유사도 구할때는 반드시 normalize 처리함.
        index.add(embeddings)
    elif method == 1: # Euclidean Distance 적용
        index = faiss.IndexFlatL2(embeddings.shape[1])
        index.add(embeddings)
    
    return index