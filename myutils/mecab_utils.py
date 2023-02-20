from konlpy.tag import Mecab
import numpy as np
from .model import embed_text

mecab = Mecab()
    
#------------------------------------------------------------------------------------------------------------------------------
# 입력 문장에 대해 명사단어들만 추출하고 벡터를 구한후, 평균값을 리턴함.
# - in : model=bi_encoder 모델 인스턴스
# - in : paragraphs=1차원 리스트 예: ['오늘 날씨가 너무 좋다']
# - in : dimension=임베딩차원(기본:768), return_tensor=True 이면 tensor값으로 임베딩벡터생성됨.
# - out : 오늘+날씨 명사만 추출한후 평균 임베딩 벡터 => 1차원 배렬 예: (768)
#------------------------------------------------------------------------------------------------------------------------------
def embed_vocab_bytag(model, paragraph:list, dimension:int=768, return_tensor=False, show=False):
    
    avg_paragraph_vocabs_vector = np.zeros((1,dimension))
    
    # 문장에서 단어들만 추출
    paragraph_vocabs = get_vocab_bytag(paragraph)
    
    if(show == True):
        print(paragraph_vocabs)
    
    # 단어들의 임베딩 벡터 구함
    paragraph_vocabs_vectors = embed_text(model=model, paragraphs=paragraph_vocabs, return_tensor=False)
    
    # 단어들의 평균을 구함
    #arr = np.array(paragraph_vocabs_vectors)
    avg_paragraph_vocabs_vector = paragraph_vocabs_vectors.mean(axis=0)
    
    return avg_paragraph_vocabs_vector.ravel(order='C') # 1차원 배열로 변경
            
    
#-------------------------------------------------------------------------------------------------------------------------------------
# 1차원 문장리스트를 입력 받아서, 검색 tag에 대한 단어들만 추출해서 출력함.
# - in : sentences : 1차원 문장 리스트 예: ['오늘 날씨가 너무 좋다','오늘 비나 눈이 온다고 한다','오늘은 춤고 바람이 분다.']
# - in : search_tag : 해당 tag에 단어들만 추출 (기본 = ['NNG', 'NNP'] 명사들만 추출함)
# - out : vocab 리스트 : 1차원 추출한 vocab 리스트 예:['오늘','날씨',비','눈','바람']
#-------------------------------------------------------------------------------------------------------------------------------------
def get_vocab_bytag(sentences:list, search_tag:list=['NNG', 'NNP']):

    #search_tag:list=['NNG', 'NNP'] # 명사들만 추출함
    vocab_temp = []
    for sentence in sentences:       
        node = mecab.pos(sentence) # 문장 node 분석
        #print(node)
        for i, (word, tag) in enumerate(node):
            if tag in search_tag:
                if word not in vocab_temp:
                    vocab_temp.append(word)
         
        # 추출된 단어가 없으면 문장을 추가
        if not vocab_temp:
            vocab_temp.append(sentence)

    return vocab_temp
        
    
#-------------------------------------------------------------------------------------------------------------------------------------
# 1차원 문장리스트를 입력 받아서, 단어들만 추출해서 출력함.
# - in : sentences : 1차원 문장 리스트 예: ['오늘 날씨가 너무 좋다','오늘 비나 눈이 온다고 한다','오늘은 춤고 바람이 분다.']
# - out : vocab 리스트 : 1차원 추출한 vocab 리스트 예:['오늘','날씨',비','눈','바람']
#-------------------------------------------------------------------------------------------------------------------------------------
def get_vocab(sentences:list):

    vocab_temp = []
    for sentence in sentences:

        temp = mecab.nouns(sentence) #각 문장별 단어 추출

        for vocab in temp:
            # 중복단어는 추가안함.
            if vocab not in vocab_temp:
                vocab_temp.append(vocab)
                
        # 추출된 단어가 없으면 문장을 추가
        if not vocab_temp:
            vocab_temp.append(sentence)
            
    return vocab_temp
        
        
#-------------------------------------------------------------------------------------------------------------------------------------
# 문장들을 split_tag 기준으로 분리해서 분리한 문장들을 출력하는 옛시
# => in : sentences : 분리할 문장들 리스트 1차원=> 예: ['오늘 날씨가 너무 좋다','오늘 비나 눈이 온다고 한다','오늘은 춤고 바람이 분다.']
# => in : pos_show : true이면 문장들 word와 tag를 쌍으로 보여줌.
#        예: ('2', 'SN'), ('월', 'NNBC'), ('15', 'SN'), ('일', 'NNBC'), ('여의도', 'NNP'), ('농민', 'NNG'), ('폭력', 'NNG'), ('시위', 'NNG'), ('를', 'JKO')..
# => in : split_tag : 분리 기준 리스트 (예: ['NNG', 'NNP'] 이면 일반명사,고유명사 기준으로 문장 분리)
#
# => out : 분리된 문장 리스트 1차원 => 예: ['오늘',날씨가',좋다','오늘','비나','눈이','온다고한다'...]
#-------------------------------------------------------------------------------------------------------------------------------------
# http://kkma.snu.ac.kr/documents/?doc=postag
def split_sentence_list(sentences: list, 
                        pos_show=False,
                        split_tag:list=['NNG', 'NNP'] 
                        ):
    
    # 분리 tag 설정 이 tag 기준으로 문장을 분리함
    #EC(연결어미)=해/고/어/여, JKO=를/을, JX(보조사)=는/은, JKB=에서/으로/에/과/로
    # NLG=일반명사(해결, 대학교..), NNP=고유명사(여의도)
    #split_tag = ['NNG', 'NNP']  
    
    # 공백 붙이지 않는 tag => 아래 tag들은 앞에 공백(띄어쓰기:' ') 하지 않는다.
    # ('되', 'XSV'), ('었', 'EP'), ('다', 'EF'), ('.', 'SF')
    # ('임종석', 'NNP'), ('이', 'JKS')
    # ('1989', 'SN'), ('년', 'NNBC'), ('2', 'SN'), ('월', 'NNBC'), ('15', 'SN'), ('일', 'NNBC')
    non_space_tag = ['EP', 'EF', 'SF', 'JKS', 'JKG', 'NNBC']
    
    split_sentence = []

    for sentence in sentences:
        
        #  node 는 '값','형태소' 식으로 출려됨.
        # 예: ('2', 'SN'), ('월', 'NNBC'), ('15', 'SN'), ('일', 'NNBC'), ('여의도', 'NNP'), ('농민', 'NNG'), ('폭력', 'NNG'), ('시위', 'NNG'), ('를', 'JKO')..
        node = mecab.pos(sentence) # 문장 node 분석
        if pos_show == True:
            print(sentence)
            print(node)
            print(f'--------------------------------------------------')
        stext: str ='' 
        for i, (word, tag) in enumerate(node):
            
            if tag in split_tag:
                split_sentence.append(stext+' '+word)
                stext=''
            elif len(stext) == 0:
                stext += word
            elif tag in non_space_tag:
                stext += word
            else:
                stext += ' '+word
                
        if len(stext) > 0:
            split_sentence.append(stext)
            
    return split_sentence
           
# main    
if __name__ == '__main__':
    main()