import os
import yaml

file_path1 = './data/settings.yaml'

def get_options(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        options = yaml.load(file, Loader=yaml.FullLoader)
    return options

options = get_options(file_path=file_path1)
print(len(options))
print(type(options))
print(options)

OUT_DIMENSION = options['model']['OUT_DIMENSION']
print(OUT_DIMENSION)

EMBEDDING_METHOD = options['embedding']['EMBEDDING_METHOD']
print(EMBEDDING_METHOD)

FLOAT_TYPE = options['embedding']['FLOAT_TYPE']
print(FLOAT_TYPE)

ES_INDEX_FILE = options['es']['ES_INDEX_FILE']
print(ES_INDEX_FILE)

ES_INDEX_NAME = options['es']['ES_INDEX_NAME']
print(ES_INDEX_NAME)

BATCH_SIZE = options['es']['BATCH_SIZE']
print(BATCH_SIZE)

CLUSTRING_MODE = options['custring']['CLUSTRING_MODE']
print(CLUSTRING_MODE)

NUM_CLUSTERS = options['custring']['NUM_CLUSTERS']
print(NUM_CLUSTERS)

OUTMODE = options['custring']['OUTMODE']
print(OUTMODE)

REMOVE_SENTENCE_LEN = options['preprocessing']['REMOVE_SENTENCE_LEN']
print(REMOVE_SENTENCE_LEN)

REMOVE_DUPLICATION = options['preprocessing']['REMOVE_DUPLICATION']
print(REMOVE_DUPLICATION)

SEARCH_SIZE = options['search']['SEARCH_SIZE']
print(SEARCH_SIZE)

VECTOR_MAG = options['search']['VECTOR_MAG']
print(VECTOR_MAG)

'''
data_list = []
with open(file_path, 'r', encoding='utf-8') as f:
    data = f.read()
    data_list.append(data)

print(data_list)
'''