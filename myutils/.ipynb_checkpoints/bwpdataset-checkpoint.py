import os
import csv
import time
import torch
import logging
import pickle
import copy
import json
import gluonnlp as nlp 

from filelock import FileLock
from dataclasses import dataclass
from typing import List, Optional
from torch.utils.data.dataset import Dataset
from transformers import PreTrainedTokenizer
from .utils import mlogging
from tqdm.notebook import tqdm
from typing import Dict, List, Optional

# [bong] mylogging 호출함
logger = mlogging(loggername='bwpdataset',logfilename='bwdataset')

@dataclass
class ClassificationExample:
    text_a: str
    text_b: Optional[str] = None
    label: Optional[str] = None


@dataclass
class ClassificationFeatures:
    input_ids: List[int]
    attention_mask: Optional[List[int]] = None
    token_type_ids: Optional[List[int]] = None
    label: Optional[int] = None
 
############################################################
# KlueNLI.Json 파일 불러오는 class
############################################################
class KlueNLICorpus:
    def __init__(self):
        pass

    def _create_examples(self, data_path):
        examples = []
        data = json.load(open(data_path, "r"))
        for el in data:
            example = ClassificationExample(
                text_a=el["premise"],
                text_b=el["hypothesis"],
                label=el["gold_label"],
            )
            examples.append(example)
        return examples

    def get_examples(self, data_fpath):
        logger.info(f"loading data... LOOKING AT {data_fpath}")
        examples = self._create_examples(data_fpath)
        return examples

    def get_labels(self):
        return ["entailment", "contradiction", "neutral"]

    @property
    def num_labels(self):
        return len(self.get_labels())

############################################################
# KorNLICorpus 파일 불러오는 class
############################################################
class KorNLICorpus:

    def __init__(self):
        pass

    def _create_examples(self, data_path):
        examples = []
        corpus = open(data_path, "r", encoding="utf-8").readlines()
        lines = [line.strip().split("\t") for line in corpus]
        for (i, line) in enumerate(lines):
            if i == 0:
                continue
            text_a, text_b, label = line
            examples.append(ClassificationExample(text_a=text_a, text_b=text_b, label=label))
        return examples

    def get_examples(self, data_fpath):
        logger.info(f"loading data... LOOKING AT {data_fpath}")
        examples = self._create_examples(data_fpath)
        return examples

    def get_labels(self):
        return ["entailment", "contradiction", "neutral"]

    @property
    def num_labels(self):
        return len(self.get_labels())

    
# .csv corpus 파일 불러오는 class    
class ClassificationCSVCorpus():
    
    def __init__(self,
                label_list: List[str],   #label_list = ["0", "1", "2", "3", "4", "5"] 
                column_num: int = 2,
                iscsvfile: int = 1       # 1이면 csv 파일, 0이면 tsv 파일
                ):
        self.iscsvfile = iscsvfile
        self.column_num = column_num
        
        if label_list is not None:
            self.label_list = label_list
        else:
            raise KeyError("label_list is empty")
            
    def get_examples(self, data_fpath):
        logger.info(f"loading data... LOOKING AT {data_fpath}")
        
        # csv 파일이면  
        if self.iscsvfile == 1:
            logger.info(f"csv file open")
            lines = list(csv.reader(open(data_fpath, "r", encoding="utf-8"), quotechar='"'))
        else: # tsv 파일이면
            logger.info(f"tsv file open")
            lines = list(csv.reader(open(data_fpath, "r", encoding="utf-8"), delimiter="\t", quotechar='"'))
            
        examples = []
        for (i, line) in enumerate(lines):
            if i == 0:
                column_num = len(lines)
                continue
    
            if self.column_num >= 3:
                _, text_a, label = line
            else:
                text_a, label = line
            examples.append(ClassificationExample(text_a=text_a, text_b=None, label=label))
        return examples

    def get_labels(self):
        return self.label_list

    @property
    def num_labels(self):
        return len(self.get_labels())
    
    
# corpus 파일을 classification 형태로 변경하는 함수    
def _convert_examples_to_classification_features(
        examples: List[ClassificationExample],
        tokenizer: PreTrainedTokenizer,
        max_seq_length,
        label_list: List[str],
):
    label_map = {label: i for i, label in enumerate(label_list)}
    labels = [label_map[example.label] for example in examples]

    logger.info("tokenize sentences, it could take a lot of time...")
    start = time.time()
        
    # tokenizer 실행    
    batch_encoding = tokenizer(
        [(example.text_a, example.text_b) for example in examples],
        max_length=max_seq_length,
        padding="max_length",
        truncation=True,
    )
    
    logger.info("tokenize sentences [took %.3f s]", time.time() - start)

    features = []
    for i in tqdm(range(len(examples))):
        inputs = {k: batch_encoding[k][i] for k in batch_encoding}
        feature = ClassificationFeatures(**inputs, label=labels[i])
        features.append(feature)

    for i, example in enumerate(examples[:2]):
        logger.info("*** Example ***")
        if example.text_b is None:
            logger.info("sentence: %s" % (example.text_a))
        else:
            sentence = example.text_a + " + " + example.text_b
            logger.info("sentence A, B: %s" % (sentence))
        logger.info("tokens: %s" % (" ".join(tokenizer.convert_ids_to_tokens(features[i].input_ids))))
        logger.info("label: %s" % (example.label))
        logger.info("features: %s" % features[i])

    return features    

#######################################################################################
##  classificationDataset 생성 class
## 인자
## - file_fpath : corpus 파일 풀경로
## - max_seq_length : token 길이, 126 이면, 126 이상 토큰화된 문장에 토큰들은 truncate 되고, 126 이하인 문장에는 padding 처리됨.
## - tokenizer : tokeinzier
## - copus : ClassficationCorpus() 함수 포인터
## - overwrite_cache(option 기본=False) : 캐쉬 파일 이용 유무(True 이면 'cached_train_class_name_126_filename' 식으로 생성된 cache 파일 이용함
#####################################################################################
class ClassificationDataset(Dataset):

    def __init__(
            self,
            file_fpath,           
            max_seq_length,        
            tokenizer: PreTrainedTokenizer,
            corpus,                
            overwrite_cache = False, 
            convert_examples_to_features_fn=_convert_examples_to_classification_features, 
    ):
        if corpus is not None:
            self.corpus = corpus
        else:
            raise KeyError("corpus is not valid")
            
        assert os.path.isfile(file_fpath), f"Input file path {file_fpath} not found"
        
        # Load data features from cache or dataset file
        directory, filename = os.path.split(file_fpath)
            
        cached_features_file = os.path.join(
            directory,
            "cached_{}_{}_{}".format(
                tokenizer.__class__.__name__,
                str(max_seq_length),
                filename,
            ),
        )

        # Make sure only the first process in distributed training processes the dataset,
        # and the others will use the cache.
        lock_path = cached_features_file + ".lock"
        with FileLock(lock_path):
            
            # 캐쉬파일이 있고, overwirte_cache==false인 경우엔 캐쉬 파일을 이용함    
            if os.path.exists(cached_features_file) and not overwrite_cache:
                start = time.time()
                self.features = torch.load(cached_features_file)
                logger.info(f"Loading features from cached file {cached_features_file} [took %.3f s]", time.time() - start)
            else:
                corpus_path = os.path.join(
                    directory,
                    filename,
                )
                logger.info(f"Creating features from dataset file at {corpus_path}")
                examples = self.corpus.get_examples(corpus_path)
                self.features = convert_examples_to_features_fn(
                    examples,
                    tokenizer,
                    max_seq_length,
                    label_list=self.corpus.get_labels(),
                )
                
                # overwrite_cache가 true일때만 생성
                #if overwrite_cache:
                start = time.time()
                logger.info(
                    "Saving features into cached file, it could take a lot of time..."
                )
                torch.save(self.features, cached_features_file)
                logger.info(
                     "Saving features into cached file %s [took %.3f s]", cached_features_file, time.time() - start
                )

    def __len__(self):
        return len(self.features)

    def __getitem__(self, i):
        return self.features[i]

    def get_labels(self):
        return self.corpus.get_labels()
    
#################################################################
## 위 ClassificationDataset를 dataloader로 변환할때 사용하는 함수
## 원본 소스 : https://github.com/ratsgo/ratsnlp/blob/master/ratsnlp/nlpbook/data_utils.py
#################################################################
def data_collator(features):
    """
    Very simple data collator that:
    - simply collates batches of dict-like objects
    - Performs special handling for potential keys named:
        - `label`: handles a single value (int or float) per object
        - `label_ids`: handles a list of values per object
    - does not do any additional preprocessing
    i.e., Property names of the input object will be used as corresponding inputs to the model.
    See glue and ner for example of how it's useful.
    """

    # In this function we'll make the assumption that all `features` in the batch
    # have the same attributes.
    # So we will look at the first element as a proxy for what attributes exist
    # on the whole batch.
    if not isinstance(features[0], dict):
        features = [vars(f) for f in features]

    first = features[0]
    batch = {}

    # Special handling for labels.
    # Ensure that tensor is created with the correct type
    # (it should be automatically the case, but let's make sure of it.)
    if "label" in first and first["label"] is not None:
        label = first["label"].item() if isinstance(first["label"], torch.Tensor) else first["label"]
        dtype = torch.long if isinstance(label, int) else torch.float
        batch["labels"] = torch.tensor([f["label"] for f in features], dtype=dtype)
    elif "label_ids" in first and first["label_ids"] is not None:
        if isinstance(first["label_ids"], torch.Tensor):
            batch["labels"] = torch.stack([f["label_ids"] for f in features])
        else:
            dtype = torch.long if type(first["label_ids"][0]) is int else torch.float
            batch["labels"] = torch.tensor([f["label_ids"] for f in features], dtype=dtype)

    # Handling of all other possible keys.
    # Again, we will use the first element to figure out which key/values are not None for this model.
    for k, v in first.items():
        if k not in ("label", "label_ids") and v is not None and not isinstance(v, str):
            if isinstance(v, torch.Tensor):
                batch[k] = torch.stack([f[k] for f in features])
            else:
                batch[k] = torch.tensor([f[k] for f in features], dtype=torch.long)

    return batch    
    
    
#################################################################
# textdataset 출력해보는 함수
# - dataset : list 형태  list[list 혹은 tensor]
# - tokenizer : tokenizer 변수
# - num : 앞에서 몇개까지 출력할지 
#################################################################
def print_dataset(dataset: list, tokenizer: PreTrainedTokenizer, num: int):
    if num > 0 :
        count = 0
        for example in dataset:
            count +=1
            if count > num:
                break
            #print(type(example))
            # tensor 타입이면 list로 변환
            if torch.is_tensor(example):
                example = example.tolist()
                
            token_str = [[tokenizer.convert_ids_to_tokens(s) for s in example]]
            print('count:{}=>{}'.format(count-1,example))
            print(token_str)
            print('\n')
            
#################################################################
# dict 형태 textdataset 출력해보는 함수
# - dataset : list[dict{"input_ids":tensor}] 형태 이면서, 
#            dict는 키로 input_ids를 가지고 있어야함
# - tokenizer : tokenizer 변수
# - num : 앞에서 몇개까지 출력할지 
#################################################################            
def print_dictdataset(dataset: list, tokenizer: PreTrainedTokenizer, num: int):
    if num > 0 :
        count = 0 
        for example in dataset:
            count +=1
            if count > num:
                break    
            #print(type(example))
            #print(example)
            token_str = []
            example1 = example['input_ids'].tolist()
            token_str = [[tokenizer.convert_ids_to_tokens(s) for s in example1]]
            print('count:{}=>{}'.format(count-1,example))
            print(token_str)
            print('\n')
           
    
#######################################################################################
##  Textdataset 생성 class
# => 입력 말뭉치를 max_seq_length 만큼 잘라서(라인구분 없이), dataset 만듬 
#
# 참고소스
# https://github.com/huggingface/transformers/blob/master/src/transformers/data/datasets/language_modeling.py
#
## 인자
## - file_fpath : corpus 파일 풀경로
## - max_seq_length : token 길이, 126 이면, 126 이상 토큰화된 문장에 토큰들은 truncate ,됨
## - tokenizer : tokeinzier
## - overwrite_cache(option 기본=False) : 캐쉬 파일 이용 유무(True 이면 'cached_train_class_name_126_filename' 식으로 생성된 cache 파일 이용함)
## - cache_dir : 캐쉬파일 저장 경로
## - show_num : dataset을 몇개까지 print 해서 보여줄지 
#######################################################################################
class MyTextDataset(Dataset):
    def __init__(
        self,
        tokenizer: PreTrainedTokenizer,
        file_path: str,
        block_size: int,
        overwrite_cache=False,
        cache_dir: Optional[str] = None,
        show_num=0  #추가
    ):
        if os.path.isfile(file_path) is False:
            raise ValueError(f"Input file path {file_path} not found")

        block_size = block_size - tokenizer.num_special_tokens_to_add(pair=False)

        directory, filename = os.path.split(file_path)
        cached_features_file = os.path.join(
            cache_dir if cache_dir is not None else directory,
            f"cached_lm_{tokenizer.__class__.__name__}_{block_size}_{filename}",
        )

        # Make sure only the first process in distributed training processes the dataset,
        # and the others will use the cache.
        lock_path = cached_features_file + ".lock"
        with FileLock(lock_path):
            ####################################################################
            # 캐쉬파일이 있고  overwrite_cache = False인 경우에는 캐쉬 파일을 읽어옴
            ####################################################################
            if os.path.exists(cached_features_file) and not overwrite_cache:
                
                logger.info(f"==>[Start] cached file read: {cached_features_file}")
   
                start = time.time()
                with open(cached_features_file, "rb") as handle:
                    self.examples = pickle.load(handle)
                
                logger.info(
                    f"<==[End] Loading features from cached file {cached_features_file} [took %.3f s]", time.time() - start
                )
            ####################################################################    
            # overwrite_cache = True인 경우
            # overwrite_cache = False 인데, 캐쉬파일이 없는 경우
            ####################################################################
            else:
                logger.info(f"Creating features from dataset file at {directory}")

                self.examples = []
                
                logger.info(f"==>[Start] file read: {file_path}")
                
                with open(file_path, encoding="utf-8") as f:
                    text = f.read()

                logger.info(f"<==[End] file read: {file_path}")
                
                logger.info(f"==>[Start] tokenizer convert_tokens_to_ids..wait max 30minute...")
                        
                tokenized_text = tokenizer.convert_tokens_to_ids(tokenizer.tokenize(text))

                logger.info(f"<==[End] tokenizer convert_tokens_to_ids")
                    
                logger.info(f"==>[Start] tokenizer")
                    
                for i in tqdm(range(0, len(tokenized_text) - block_size + 1, block_size)):  # Truncate in block of block_size
                    self.examples.append(
                        tokenizer.build_inputs_with_special_tokens(tokenized_text[i : i + block_size])
                    )
                    
                logger.info(f"==>[End] tokenizer")    
                
                # tokenizer 된 내용을 print 해봄
                num = min(len(self.examples), show_num)
                print_dataset(self.examples, tokenizer, num)
                
                # Note that we are losing the last truncated example here for the sake of simplicity (no padding)
                # If your dataset is small, first you should look for a bigger one :-) and second you
                # can change this behavior by adding (model specific) padding.
                
                # overwrite_cache=True 인경우에만 캐쉬파일 생성함
                if overwrite_cache:
                    logger.info(f"==>[Start] cached file create: {cached_features_file}")
                    start = time.time()
                    with open(cached_features_file, "wb") as handle:
                        pickle.dump(self.examples, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    logger.info(
                        f"<==[End] Saving features into cached file {cached_features_file} [took {time.time() - start:.3f} s]"
                    )

    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i) -> torch.Tensor:
        return torch.tensor(self.examples[i], dtype=torch.long)
    
    
#######################################################################################
##  Textdataset 생성 class
# => 입력 말뭉치를 라인으로 구분하여 dataset 생성함
#
# 참고소스
# https://github.com/huggingface/transformers/blob/master/src/transformers/data/datasets/language_modeling.py
#
## 인자
## - file_fpath : corpus 파일 풀경로
## - max_seq_length : token 길이, 126 이면, 126 이상 토큰화된 문장에 토큰들은 truncate ,됨
## - tokenizer : tokeinzier
## - out_format_dict : True명 출력형태는 list[dict{'iput_ids':tensor}] 형태로, False면 List[tensor] 형태로 출력함
## - show_num : dataset을 몇개까지 print 해서 보여줄지 
#######################################################################################    
class MyLineByLineTextDataset(Dataset):
  
    def __init__(
        self, 
        tokenizer: PreTrainedTokenizer, 
        file_path: str, 
        block_size: int, 
        out_format_dict=True,  # 추가한 변수 
        show_num = 0
    ):
        
        if os.path.isfile(file_path) is False:
            raise ValueError(f"Input file path {file_path} not found")
            
        # Here, we do not cache the features, operating under the assumption
        # that we will soon use fast multithreaded tokenizers from the
        # `tokenizers` repo everywhere =)
        logger.info(f"Creating features from dataset file at {file_path}")

        logger.info(f"==>[Start] file read lines: {file_path}")
        
        with open(file_path, encoding="utf-8") as f:
            lines = [line for line in tqdm(f.read().splitlines()) if (len(line) > 0 and not line.isspace())]

        logger.info(f"<==[End] file read lines: {file_path}")
                
        logger.info(f"==>[Start] tokenizer")
        
        batch_encoding = tokenizer(lines, add_special_tokens=True, truncation=True, max_length=block_size)
        self.examples = batch_encoding["input_ids"]
        
        num = min(len(self.examples), show_num)
            
        # dict tensor 형태로 출력하는 경우
        if out_format_dict:
            self.examples = [{"input_ids": torch.tensor(e, dtype=torch.long)} for e in self.examples]
            
            print_dictdataset(self.examples, tokenizer, num)
        # 그냥 tensor로만 출력하는 경우    
        else:
            self.examples = [torch.tensor(e, dtype=torch.long) for e in self.examples]
            print_dataset(self.examples, tokenizer, num)
            
        logger.info(f"<==[End] tokenizer")
        
        # tokenizer 된 내용을 print 해봄
       
      
                
    def __len__(self):
        return len(self.examples)

    def __getitem__(self, i) -> Dict[str, torch.tensor]:
        return self.examples[i]    

    
#######################################################################################
##  MLMDataset 생성 class
# => 입력 말뭉치를 line별루 MLM(MARK Language Model) 형태로 data 만드는 clsss
#
# 참고소스
# https://towardsdatascience.com/masked-language-modelling-with-bert-7d49793e5d2c
#
## 인자
## - corpus_path : corpus 파일 풀경로
## - tokenizer : tokeinzier
## - CLStokeinid: int,   # [CLS] 토큰 id  (예: 101)
## - SEPtokenid: int,    # [SEP] 토큰 id  (예: 102)
## - UNKtokenid: int,    # [UNK] 토큰 id  (예: 100)
## - PADtokenid: int,    # [PAD] 토큰 id  (예: 0)
## - Masktokenid: int,   # [MASK] 토큰 id (예: 103)
## - max_seq_length : token 길이, 128 이면, 128 이상 토큰화된 문장에 토큰들은 truncate ,됨
## - mlm_probability : 해당 문장에 있는 토큰들 중 몇 %로 [MASK] 토큰으로 변환할 것인가 (15% : 15% 확률로 [MASK]로 토큰 변환 시킴)
## - cache_dir : 캐쉬파일 저장경로
## - overwrite_cache : True면 cache 파일 씀, False이면 캐쉬파일 있으면 캐쉬파일 이용함
#######################################################################################    
class MLMDataset(Dataset):
    
    def __init__(self, 
                 corpus_path: str,   # corpus 파일 경로 
                 tokenizer: PreTrainedTokenizer, # tokenizer 
                 CLStokeinid: int,   # [CLS] 토큰 id
                 SEPtokenid: int,    # [SEP] 토큰 id
                 UNKtokenid: int,    # [UNK] 토큰 id
                 PADtokenid: int,    # [PAD] 토큰 id
                 Masktokenid: int,   # [MASK] 토큰 id
                 max_sequence_len: int=128,  # max_sequence_len
                 mlm_probability: float=0.15,  # [MASK] 변환할 토큰 % 수
                 cache_dir: Optional[str] = None,  # 캐쉬파일 저장 경로
                 overwrite_cache=False  # True면 cache 파일 씀, False이면 캐쉬파일 있으면 캐쉬파일 이용함
                ):
        
        self.mydict = {}  
        #==========================================
        # 각 인자값 유효성 검사
        #==========================================
        
        if corpus_path is None:
            raise KeyError("corpus_path is not valid")
        else:
            self.corpus_path = corpus_path
            
        if tokenizer is None:
            raise KeyError("tokenizer is not valid")
        else:
            self.tokenizer = tokenizer
            
        if CLStokeinid is None or SEPtokenid is None or UNKtokenid is None or PADtokenid is None or Masktokenid is None:
            raise KeyError("tokenids is not valid")
        else:
            self.CLStokeinid = CLStokeinid
            self.SEPtokenid = SEPtokenid
            self.UNKtokenid = UNKtokenid
            self.PADtokenid = PADtokenid
            self.Masktokenid = Masktokenid
            
        self.max_sequence_len = max_sequence_len
        self.mlm_probability = mlm_probability   
        
        print(f'*corpus:{corpus_path}')
        print(f'*max_sequence_len:{max_sequence_len}')
        print(f'*mlm_probability:{mlm_probability}')
        print('*CLStokenid:{}, SEPtokenid:{}, UNKtokenid:{}, PADtokeinid:{}, Masktokeid:{}' \
              .format(CLStokeinid, SEPtokenid, UNKtokenid, PADtokenid, Masktokenid))
        
        # 캐쉬파일 경로 얻어옴
        directory, filename = os.path.split(corpus_path)
        cached_features_file = os.path.join(
            cache_dir if cache_dir is not None else directory,
            f"cached_lm_{tokenizer.__class__.__name__}_{max_sequence_len}_{filename}",
        )
        
        # Make sure only the first process in distributed training processes the dataset,
        # and the others will use the cache.
        lock_path = cached_features_file + ".lock"
        with FileLock(lock_path):
            
            ####################################################################
            # 캐쉬파일이 있고  overwrite_cache = False인 경우에는 캐쉬 파일을 읽어옴
            ####################################################################
            if os.path.exists(cached_features_file) and not overwrite_cache:
                
                logger.info(f"==>[Start] cached file read: {cached_features_file}")
   
                start = time.time()
                with open(cached_features_file, "rb") as handle:
                    self.mydict = pickle.load(handle)
                
                logger.info(
                    f"<==[End] Loading features from cached file {cached_features_file} [took %.3f s]", time.time() - start
                )
            ####################################################################    
            # overwrite_cache = True인 경우
            # overwrite_cache = False 인데, 캐쉬파일이 없는 경우
            ####################################################################
            else:
                #==========================================
                # corpus 파일을 로딩함    
                #==========================================
                datalist = []
                # [bong] total_line 수를 구함
                with open(self.corpus_path, encoding="utf-8") as f:
                    total_line = len(f.readlines())
                    # [bong] 총 라인수 출력
                    print('*total_line: {}'.format(total_line))

                with open(self.corpus_path, encoding="utf-8") as f:
                    for idx in tqdm(range(total_line)): 
                        line = f.readline()
                        if not line:
                            # [bong] 총 라인수 읽기 끝
                            print('*readline=>count: {} End!'.format(scount))
                            break
                        line = line.strip() # 필수!!!!
                        datalist.append([line]) #2차원으로 묶어야 함

                #==========================================
                # tokenize 시작 
                #==========================================
                count = 0
                token_ids_list = []
                token_type_ids_list = []
                attention_mask_list = []
                labels_list = []

                for tmpdata in tqdm(datalist):

                    #===========================================
                    #  # data is null 이면 continue
                    #===========================================
                    data = tmpdata[0].strip()  # tmpdata는 list 형태임
                    if not data:
                        continue

                    count += 1
                    #===========================================
                    # tokenize 처리함
                    #===========================================

                    inputs = tokenizer(data, max_length=max_sequence_len, truncation=True, padding='max_length', return_tensors='pt')

                    #print(inputs)
                    # tokeni_ids, token_type_id, attentison_mask, label 등을 얻어옴
                    token_ids = inputs['input_ids']
                    token_type_ids = inputs['token_type_ids']
                    attention_mask = inputs['attention_mask']
                    labels = copy.deepcopy(token_ids) # *[bong] label를 token_ids 값을 deepcopy하여, 생성   

                    #===========================================
                    # token_ids 에 대해 MLM 생성      
                    #===========================================
                    #token_ids에 15% 확률로 [MASK] 붙임  
                    rand = torch.rand(token_ids.shape)
                    # [CLS],[SEP],[UNK],[PAD] 은 각각 특수 토큰이므로, 특수 토큰에는 [MASK]를 하지 않음
                    mask_arr = (rand < self.mlm_probability)*(token_ids != self.CLStokeinid)*(token_ids != self.SEPtokenid)* \
                                (token_ids != self.UNKtokenid)*(token_ids != self.PADtokenid)
                    #print(mask_arr)

                    # MASK 붙일 위치를 배열로 변환
                    selection = torch.flatten((mask_arr[0]).nonzero()).tolist()
                    #print('MASK Position: {}'.format(selection))

                    # [MASK] 토큰(4) 으로 변경
                    #print(f'befor:{token_ids}')
                    token_ids[0,selection] = Masktokenid
                    #print(f'after:{token_ids}')

                    token_ids_list.append(token_ids[0].tolist())
                    token_type_ids_list.append(token_type_ids[0].tolist())
                    attention_mask_list.append(attention_mask[0].tolist())
                    labels_list.append(labels[0].tolist())

                # dict 로 만듬.(*텐서롤 만들지는 않음=>dataloader에 들어가면 텐서로 만드므로.)     
                self.mydict = {'input_ids':token_ids_list, 'token_type_ids':token_type_ids_list, 'attention_mask':attention_mask_list, 'labels':labels_list} 

                 # overwrite_cache=True 인경우에만 캐쉬파일 생성함
                if overwrite_cache:
                    logger.info(f"==>[Start] cached file create: {cached_features_file}")
                    start = time.time()
                    with open(cached_features_file, "wb") as handle:
                        pickle.dump(self.mydict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    logger.info(f"<==[End] Saving features into cached file {cached_features_file} [took {time.time() - start:.3f} s]")

                #print(self.mydict.keys())
                #print(len(self.mydict['inputs_ids']))
                #print(self.mydict['inputs_ids'])
        
            
    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.mydict.items()}

    def __len__(self):
        return (len(self.mydict['input_ids']))
    
#=========================================================
# MLMDataset과 동일한데..단 Distilbert에는 token_type_ids 가 없음
#=========================================================
class MLMDatasetbyDistilBert(Dataset):
    
    def __init__(self, 
                 corpus_path: str,   # corpus 파일 경로 
                 tokenizer: PreTrainedTokenizer, # tokenizer 
                 CLStokeinid: int,   # [CLS] 토큰 id
                 SEPtokenid: int,    # [SEP] 토큰 id
                 UNKtokenid: int,    # [UNK] 토큰 id
                 PADtokenid: int,    # [PAD] 토큰 id
                 Masktokenid: int,   # [MASK] 토큰 id
                 max_sequence_len: int=128,  # max_sequence_len
                 mlm_probability: float=0.15,  # [MASK] 변환할 토큰 % 수
                 cache_dir: Optional[str] = None,  # 캐쉬파일 저장 경로
                 overwrite_cache=False  # True면 cache 파일 씀, False이면 캐쉬파일 있으면 캐쉬파일 이용함
                ):
        
        self.mydict = {}  
        #==========================================
        # 각 인자값 유효성 검사
        #==========================================
        
        if corpus_path is None:
            raise KeyError("corpus_path is not valid")
        else:
            self.corpus_path = corpus_path
            
        if tokenizer is None:
            raise KeyError("tokenizer is not valid")
        else:
            self.tokenizer = tokenizer
            
        if CLStokeinid is None or SEPtokenid is None or UNKtokenid is None or PADtokenid is None or Masktokenid is None:
            raise KeyError("tokenids is not valid")
        else:
            self.CLStokeinid = CLStokeinid
            self.SEPtokenid = SEPtokenid
            self.UNKtokenid = UNKtokenid
            self.PADtokenid = PADtokenid
            self.Masktokenid = Masktokenid
            
        self.max_sequence_len = max_sequence_len
        self.mlm_probability = mlm_probability   
        
        print(f'*corpus:{corpus_path}')
        print(f'*max_sequence_len:{max_sequence_len}')
        print(f'*mlm_probability:{mlm_probability}')
        print('*CLStokenid:{}, SEPtokenid:{}, UNKtokenid:{}, PADtokeinid:{}, Masktokeid:{}' \
              .format(CLStokeinid, SEPtokenid, UNKtokenid, PADtokenid, Masktokenid))
        
        # 캐쉬파일 경로 얻어옴
        directory, filename = os.path.split(corpus_path)
        cached_features_file = os.path.join(
            cache_dir if cache_dir is not None else directory,
            f"cached_lm_{tokenizer.__class__.__name__}_{max_sequence_len}_{filename}",
        )
        
        # Make sure only the first process in distributed training processes the dataset,
        # and the others will use the cache.
        lock_path = cached_features_file + ".lock"
        with FileLock(lock_path):
            
            ####################################################################
            # 캐쉬파일이 있고  overwrite_cache = False인 경우에는 캐쉬 파일을 읽어옴
            ####################################################################
            if os.path.exists(cached_features_file) and not overwrite_cache:
                
                logger.info(f"==>[Start] cached file read: {cached_features_file}")
   
                start = time.time()
                with open(cached_features_file, "rb") as handle:
                    self.mydict = pickle.load(handle)
                
                logger.info(
                    f"<==[End] Loading features from cached file {cached_features_file} [took %.3f s]", time.time() - start
                )
            ####################################################################    
            # overwrite_cache = True인 경우
            # overwrite_cache = False 인데, 캐쉬파일이 없는 경우
            ####################################################################
            else:
                #==========================================
                # corpus 파일을 로딩함    
                #==========================================
                datalist = []
                # [bong] total_line 수를 구함
                with open(self.corpus_path, encoding="utf-8") as f:
                    total_line = len(f.readlines())
                    # [bong] 총 라인수 출력
                    print('*total_line: {}'.format(total_line))

                with open(self.corpus_path, encoding="utf-8") as f:
                    for idx in tqdm(range(total_line)): 
                        line = f.readline()
                        if not line:
                            # [bong] 총 라인수 읽기 끝
                            print('*readline=>count: {} End!'.format(scount))
                            break
                        line = line.strip() # 필수!!!!
                        datalist.append([line]) #2차원으로 묶어야 함

                #==========================================
                # tokenize 시작 
                #==========================================
                count = 0
                token_ids_list = []
                attention_mask_list = []
                labels_list = []

                for tmpdata in tqdm(datalist):

                    #===========================================
                    #  # data is null 이면 continue
                    #===========================================
                    data = tmpdata[0].strip()  # tmpdata는 list 형태임
                    if not data:
                        continue

                    count += 1
                    #===========================================
                    # tokenize 처리함
                    #===========================================

                    inputs = tokenizer(data, max_length=max_sequence_len, truncation=True, padding='max_length', return_tensors='pt')

                    #print(inputs)
                    # tokeni_ids, token_type_id, attentison_mask, label 등을 얻어옴
                    token_ids = inputs['input_ids']
                    attention_mask = inputs['attention_mask']
                    labels = copy.deepcopy(token_ids) # *[bong] label를 token_ids 값을 deepcopy하여, 생성   

                    #===========================================
                    # token_ids 에 대해 MLM 생성      
                    #===========================================
                    #token_ids에 15% 확률로 [MASK] 붙임  
                    rand = torch.rand(token_ids.shape)
                    # [CLS],[SEP],[UNK],[PAD] 은 각각 특수 토큰이므로, 특수 토큰에는 [MASK]를 하지 않음
                    mask_arr = (rand < self.mlm_probability)*(token_ids != self.CLStokeinid)*(token_ids != self.SEPtokenid)* \
                                (token_ids != self.UNKtokenid)*(token_ids != self.PADtokenid)
                    #print(mask_arr)

                    # MASK 붙일 위치를 배열로 변환
                    selection = torch.flatten((mask_arr[0]).nonzero()).tolist()
                    #print('MASK Position: {}'.format(selection))

                    # [MASK] 토큰(4) 으로 변경
                    #print(f'befor:{token_ids}')
                    token_ids[0,selection] = Masktokenid
                    #print(f'after:{token_ids}')

                    token_ids_list.append(token_ids[0].tolist())
                    attention_mask_list.append(attention_mask[0].tolist())
                    labels_list.append(labels[0].tolist())

                # dict 로 만듬.(*텐서롤 만들지는 않음=>dataloader에 들어가면 텐서로 만드므로.)     
                self.mydict = {'inputs_ids':token_ids_list, 'attention_mask':attention_mask_list, 'labels':labels_list} 

                 # overwrite_cache=True 인경우에만 캐쉬파일 생성함
                if overwrite_cache:
                    logger.info(f"==>[Start] cached file create: {cached_features_file}")
                    start = time.time()
                    with open(cached_features_file, "wb") as handle:
                        pickle.dump(self.mydict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    logger.info(f"<==[End] Saving features into cached file {cached_features_file} [took {time.time() - start:.3f} s]")

                #print(self.mydict.keys())
                #print(len(self.mydict['inputs_ids']))
                #print(self.mydict['inputs_ids'])
        
            
    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.mydict.items()}

    def __len__(self):
        return (len(self.mydict['inputs_ids']))
    
    
# MLMDataset distillation 용
class MLMDatasetDistillation(Dataset):
    
    def __init__(self, 
                 corpus_path: str,   # corpus 파일 경로 
                 tokenizer: PreTrainedTokenizer, # tokenizer 
                 CLStokeinid: int,   # [CLS] 토큰 id
                 SEPtokenid: int,    # [SEP] 토큰 id
                 UNKtokenid: int,    # [UNK] 토큰 id
                 PADtokenid: int,    # [PAD] 토큰 id
                 Masktokenid: int,   # [MASK] 토큰 id
                 max_sequence_len: int=128,  # max_sequence_len
                 mlm_probability: float=0.15,  # [MASK] 변환할 토큰 % 수
                 cache_dir: Optional[str] = None,  # 캐쉬파일 저장 경로
                 overwrite_cache=False  # True면 cache 파일 씀, False이면 캐쉬파일 있으면 캐쉬파일 이용함
                ):
        
        self.mydict = {}  
        #==========================================
        # 각 인자값 유효성 검사
        #==========================================
        
        if corpus_path is None:
            raise KeyError("corpus_path is not valid")
        else:
            self.corpus_path = corpus_path
            
        if tokenizer is None:
            raise KeyError("tokenizer is not valid")
        else:
            self.tokenizer = tokenizer
            
        if CLStokeinid is None or SEPtokenid is None or UNKtokenid is None or PADtokenid is None or Masktokenid is None:
            raise KeyError("tokenids is not valid")
        else:
            self.CLStokeinid = CLStokeinid
            self.SEPtokenid = SEPtokenid
            self.UNKtokenid = UNKtokenid
            self.PADtokenid = PADtokenid
            self.Masktokenid = Masktokenid
            
        self.max_sequence_len = max_sequence_len
        self.mlm_probability = mlm_probability   
        
        print(f'*corpus:{corpus_path}')
        print(f'*max_sequence_len:{max_sequence_len}')
        print(f'*mlm_probability:{mlm_probability}')
        print('*CLStokenid:{}, SEPtokenid:{}, UNKtokenid:{}, PADtokeinid:{}, Masktokeid:{}' \
              .format(CLStokeinid, SEPtokenid, UNKtokenid, PADtokenid, Masktokenid))
        
        # 캐쉬파일 경로 얻어옴
        directory, filename = os.path.split(corpus_path)
        cached_features_file = os.path.join(
            cache_dir if cache_dir is not None else directory,
            f"cached_lm_{tokenizer.__class__.__name__}_{max_sequence_len}_{filename}",
        )
        
        # Make sure only the first process in distributed training processes the dataset,
        # and the others will use the cache.
        lock_path = cached_features_file + ".lock"
        with FileLock(lock_path):
            
            ####################################################################
            # 캐쉬파일이 있고  overwrite_cache = False인 경우에는 캐쉬 파일을 읽어옴
            ####################################################################
            if os.path.exists(cached_features_file) and not overwrite_cache:
                
                logger.info(f"==>[Start] cached file read: {cached_features_file}")
   
                start = time.time()
                with open(cached_features_file, "rb") as handle:
                    self.mydict = pickle.load(handle)
                
                logger.info(
                    f"<==[End] Loading features from cached file {cached_features_file} [took %.3f s]", time.time() - start
                )
            ####################################################################    
            # overwrite_cache = True인 경우
            # overwrite_cache = False 인데, 캐쉬파일이 없는 경우
            ####################################################################
            else:
                #==========================================
                # corpus 파일을 로딩함    
                #==========================================
                datalist = []
                # [bong] total_line 수를 구함
                with open(self.corpus_path, encoding="utf-8") as f:
                    total_line = len(f.readlines())
                    # [bong] 총 라인수 출력
                    print('*total_line: {}'.format(total_line))

                with open(self.corpus_path, encoding="utf-8") as f:
                    for idx in tqdm(range(total_line)): 
                        line = f.readline()
                        if not line:
                            # [bong] 총 라인수 읽기 끝
                            print('*readline=>count: {} End!'.format(scount))
                            break
                        line = line.strip() # 필수!!!!
                        datalist.append([line]) #2차원으로 묶어야 함

                #==========================================
                # tokenize 시작 
                #==========================================
                count = 0
                token_ids_list = []
                token_type_ids_list = []
                attention_mask_list = []
                labels_list = []

                for tmpdata in tqdm(datalist):

                    #===========================================
                    #  # data is null 이면 continue
                    #===========================================
                    data = tmpdata[0].strip()  # tmpdata는 list 형태임
                    if not data:
                        continue

                    count += 1
                    #===========================================
                    # tokenize 처리함
                    #===========================================

                    inputs = tokenizer(data, max_length=max_sequence_len, truncation=True, padding='max_length', return_tensors='pt')

                    #print(inputs)
                    # tokeni_ids, token_type_id, attentison_mask, label 등을 얻어옴
                    token_ids = inputs['input_ids']
                    token_type_ids = inputs['token_type_ids']
                    attention_mask = inputs['attention_mask']
                    labels = copy.deepcopy(token_ids) # *[bong] label를 token_ids 값을 deepcopy하여, 생성   

                    #===========================================
                    # token_ids 에 대해 MLM 생성      
                    #===========================================
                    #token_ids에 15% 확률로 [MASK] 붙임  
                    rand = torch.rand(token_ids.shape)
                    # [CLS],[SEP],[UNK],[PAD] 은 각각 특수 토큰이므로, 특수 토큰에는 [MASK]를 하지 않음
                    mask_arr = (rand < self.mlm_probability)*(token_ids != self.CLStokeinid)*(token_ids != self.SEPtokenid)* \
                                (token_ids != self.UNKtokenid)*(token_ids != self.PADtokenid)
                    #print(mask_arr)

                    # MASK 붙일 위치를 배열로 변환
                    selection = torch.flatten((mask_arr[0]).nonzero()).tolist()
                    #print('MASK Position: {}'.format(selection))

                    # [MASK] 토큰(4) 으로 변경
                    #print(f'befor:{token_ids}')
                    token_ids[0,selection] = Masktokenid
                    #print(f'after:{token_ids}')

                    token_ids_list.append(token_ids[0].tolist())
                    token_type_ids_list.append(token_type_ids[0].tolist())
                    attention_mask_list.append(attention_mask[0].tolist())
                    labels_list.append(labels[0].tolist())

                # dict 로 만듬.(*텐서롤 만들지는 않음=>dataloader에 들어가면 텐서로 만드므로.)     
                self.mydict = {'input_ids':token_ids_list, 'token_type_ids':token_type_ids_list, 'attention_mask':attention_mask_list, 'masked_lm_labels':labels_list} 

                 # overwrite_cache=True 인경우에만 캐쉬파일 생성함
                if overwrite_cache:
                    logger.info(f"==>[Start] cached file create: {cached_features_file}")
                    start = time.time()
                    with open(cached_features_file, "wb") as handle:
                        pickle.dump(self.mydict, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    logger.info(f"<==[End] Saving features into cached file {cached_features_file} [took {time.time() - start:.3f} s]")

                #print(self.mydict.keys())
                #print(len(self.mydict['inputs_ids']))
                #print(self.mydict['inputs_ids'])
        
            
    def __getitem__(self, idx):
        return {key: torch.tensor(val[idx]) for key, val in self.mydict.items()}

    def __len__(self):
        return (len(self.mydict['input_ids']))