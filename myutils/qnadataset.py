import os
import time
import json
import torch
import logging
from tqdm import tqdm
from functools import partial
from filelock import FileLock
from dataclasses import dataclass
from typing import List, Optional
from multiprocessing import Pool, cpu_count
from transformers import PreTrainedTokenizer
from torch.utils.data.dataset import Dataset

from .utils import mlogging

# [bong] mylogging 호출함
logger = mlogging(loggername='qnadataset',logfilename='qnadataset')


@dataclass
class QAExample:
    # 질문 : 임종석이 여의도 농민 폭력 시위를 주도한 혐의로 지명수배 된 날은?
    question_text: str
    # (답 찾는 대상인)지문 : 1989년 2월 15일 여의도 농민 폭력 시위를 주도한 혐의 ... 서울지방경찰청 공안분실로 인계되었다.
    context_text: str
    # 답변 : 1989년 2월 15일
    answer_text: str
    # 답변의 시작 위치(음절 수 기준) : 0
    start_position_character: Optional[int] = None


class QACorpus:

    def __init__(self):
        pass

    def get_examples(self, corpus_dir, mode):
        """
        :return: List[QAExample]
        """
        raise NotImplementedError


# KorQuAD_v1.0_train.json 파일 불러와서 examples 리스트에 넣는 함수
class KorQuADCorpus(QACorpus):

    def __init__(self):
       pass

    def get_examples(self, corpus_fpath):

        examples = []
         
        # KorQuAD_v1.0_train.json 파일을 불러옴
        json_data = json.load(open(corpus_fpath, "r", encoding="utf-8"))["data"]
        for entry in tqdm(json_data):
            for paragraph in entry["paragraphs"]:
                context_text = paragraph["context"]
                for qa in paragraph["qas"]:
                    question_text = qa["question"]
                    for answer in qa["answers"]:
                        answer_text = answer["text"]
                        start_position_character = answer["answer_start"]

                        # question, context, answer, startposition 등을 설정함
                        if question_text and answer_text and context_text and start_position_character:
                            example = QAExample(
                                question_text=question_text,
                                context_text=context_text,
                                answer_text=answer_text,
                                start_position_character=start_position_character,
                            )
                            examples.append(example)
        return examples


@dataclass
class QAFeatures:
    input_ids: List[int]
    attention_mask: List[int]
    token_type_ids: List[int]
    # start_positions : 지문상 시작 토큰 위치 (wordpiece 토큰 기준)
    start_positions: int
    # end_position : 지문상 끝 토큰 위치 (wordpiece 토큰 기준)
    end_positions: int


def _squad_convert_example_to_features_init(tokenizer_for_convert):
    global tokenizer
    tokenizer = tokenizer_for_convert


def _is_whitespace(c):
    if c == " " or c == "\t" or c == "\r" or c == "\n" or ord(c) == 0x202F:
        return True
    return False


def _whitespace_tokenize(text):
    """Runs basic whitespace cleaning and splitting on a piece of text."""
    text = text.strip()
    if not text:
        return []
    tokens = text.split()
    return tokens


def _improve_answer_span(doc_tokens, input_start, input_end, tokenizer, orig_answer_text):
    """Returns tokenized answer spans that better match the annotated answer."""
    tok_answer_text = " ".join(tokenizer.tokenize(orig_answer_text))
    for new_start in range(input_start, input_end + 1):
        for new_end in range(input_end, new_start - 1, -1):
            text_span = " ".join(doc_tokens[new_start : (new_end + 1)])
            if text_span == tok_answer_text:
                return new_start, new_end
    return input_start, input_end


def _squad_convert_example_to_features(example, max_seq_length, doc_stride, max_query_length):
    features = []

    doc_tokens, char_to_word_offset = [], []
    prev_is_whitespace = True
    # Split on whitespace so that different tokens may be attributed to their original position.
    for c in example.context_text:
        if _is_whitespace(c):
            prev_is_whitespace = True
        else:
            if prev_is_whitespace:
                doc_tokens.append(c)
            else:
                doc_tokens[-1] += c
            prev_is_whitespace = False
        char_to_word_offset.append(len(doc_tokens) - 1)

    # Get start and end position
    # 정답의 시작/끝 위치 : 어절 기준
    start_position = char_to_word_offset[example.start_position_character]
    end_position = char_to_word_offset[
        min(example.start_position_character + len(example.answer_text) - 1, len(char_to_word_offset) - 1)
    ]

    # If the answer cannot be found in the text, then skip this example.
    # actual_text : 어절 단위 정답 스팬(대개 cleaned_answer_text을 포함한다), 예: 베토벤의 교향곡 9번을
    actual_text = " ".join(doc_tokens[start_position:(end_position + 1)])
    # cleaned_answer_text : 사람이 레이블한 정답 스팬, 베토벤의 교향곡 9번
    cleaned_answer_text = " ".join(_whitespace_tokenize(example.answer_text))
    # actual_text가 cleaned_answer_text를 포함할 경우 0
    # 그렇지 않을 경우 -1 (actual_text이 "베토벤 교향곡 9번" 등일 경우 이 케이스)
    if actual_text.find(cleaned_answer_text) == -1:
        logger.warning("Could not find answer: '%s' vs. '%s'", actual_text, cleaned_answer_text)
        return []

    # doc_tokens : context_text의 각 어절
    # all_doc_tokens는 doc_tokens의 각 어절별로 wordpiece를 수행한 토큰 리스트
    # tok_to_orig_index는 all_doc_tokens의 각 토큰이 context_text에서 몇 번째 어절에 위치하는지 나타내는 리스트
    # orig_to_tok_index는 context_text의 각 어절의 시작 토큰이 all_doc_tokens에서 몇 번째 토큰에 위치하는지 나타내는 리스트
    # context_text가 "아이스크림케이크 좋아하는 사람 있나요?"고
    # doc_tokens가 ["아이스크림케이크", "좋아하는", "사람", "있나요?"]라면
    # all_doc_tokens = ['아이', '##스크', '##림', '##케이', '##크', '좋아하는', '사람', '있나요', '?']
    # tok_to_orig_index = [0, 0, 0, 0, 0, 1, 2, 3, 3]라면
    # all_doc_tokens의 0~4번째 토큰('아이', '##스크', '##림', '##케이', '##크')은 context_text상 0번째 어절에 위치함을 나타냄
    # orig_to_tok_index = [0, 5, 6, 7]라면
    # context_text의 0번째 어절(아이스크림케이크)의 시작은 all_doc_tokens상 0번째 토큰
    # context_text의 1번째 어절(좋아하는)의 시작은 all_doc_tokens상 5번째 토큰
    # ...
    tok_to_orig_index = []
    orig_to_tok_index = []
    all_doc_tokens = []
    for (i, token) in enumerate(doc_tokens):
        orig_to_tok_index.append(len(all_doc_tokens))
        sub_tokens = tokenizer.tokenize(token)
        for sub_token in sub_tokens:
            tok_to_orig_index.append(i)
            all_doc_tokens.append(sub_token)

    # 학습은 어절 단위가 아니라 wordpiece 토큰 단위로 이뤄진다
    # 하지만 annotation된 레이블은 wordpiece 토큰 단위가 아니라 사람이 특정 범위를 지정한 것
    # 따라서 아래 if문 안에서 처리를 해서 wordpiece상 정답 범위를 정한다
    # all_doc_tokens[tok_start_position:tok_end_position]
    # > ['베', '##토', '##벤', '##의', '교', '##향', '##곡', '9', '##번']
    # example.start_position : 정답 토큰의 시작이 context_text에서 몇 번째 어절에 있는지 정보
    # example.end_position : 정답 토큰의 끝이 context_text에서 몇 번째 어절에 있는지 정보
    # tok_start_position = context_text상 example.start_position번째 어절이 all_doc_tokens에서 몇 번째 토큰인지 나타냄
    # tok_end_position = context_text상 example.end_position번째 어절이 all_doc_tokens에서 몇 번째 토큰인지 나타냄
    tok_start_position = orig_to_tok_index[start_position]
    if end_position < len(doc_tokens) - 1:
        tok_end_position = orig_to_tok_index[end_position + 1] - 1
    else:
        tok_end_position = len(doc_tokens) - 1

    (tok_start_position, tok_end_position) = _improve_answer_span(
        all_doc_tokens, tok_start_position, tok_end_position, tokenizer, example.answer_text
    )

    spans = []

    truncated_query = tokenizer.encode(
        example.question_text, add_special_tokens=False, truncation=True, max_length=max_query_length
    )
    sequence_added_tokens = (
        tokenizer.model_max_length - tokenizer.max_len_single_sentence + 1
        if "roberta" in str(type(tokenizer)) or "camembert" in str(type(tokenizer))
        else tokenizer.model_max_length - tokenizer.max_len_single_sentence
    )

    # [CLS] question [SEP] context [SEP] > 따라서 총 3개
    sequence_pair_added_tokens = tokenizer.model_max_length - tokenizer.max_len_sentences_pair

    span_doc_tokens = all_doc_tokens
    while len(spans) * doc_stride < len(all_doc_tokens):
        # padding_side = "right"라면 question + [SEP] + context으로 인코딩
        # padding_size = "left"라면 context + [SEP] + question으로 인코딩
        # truncated_query : token id sequence, List[int]
        # span_doc_tokens : token sequence, List[str]
        # encode_plus의 arg인 stride는 max_seq_length보다 길 경우
        # truncated 실시한 토큰화 결과(input_ids)와 넘치는 토큰 시퀀스(overflowing_tokens)가
        # 몇 개 토큰이 겹치게 만들 것인지를 정한다
        # stride = 0이라면 이 둘 사이에 겹치는 토큰 = 0
        # stride = max_seq_length라면 이 둘을 완전히 겹치게 만든다
        # 다만 이 값을 정할 때 max_seq_length에서 TrainArguments의 doc_stride만큼을 빼주고 있으므로
        # 다음 청크를 만들 때 doc_stride만큼 건너뛰는 효과가 있다
        encoded_dict = tokenizer.encode_plus(
            truncated_query if tokenizer.padding_side == "right" else span_doc_tokens,
            span_doc_tokens if tokenizer.padding_side == "right" else truncated_query,
            truncation="only_second" if tokenizer.padding_side == "right" else "only_first",
            padding="max_length",
            max_length=max_seq_length,
            return_overflowing_tokens=True,
            stride=max_seq_length - doc_stride - len(truncated_query) - sequence_pair_added_tokens,
            return_token_type_ids=True,
        )

        paragraph_len = min(
            len(all_doc_tokens) - len(spans) * doc_stride,
            max_seq_length - len(truncated_query) - sequence_pair_added_tokens,
        )

        encoded_dict["start"] = len(spans) * doc_stride
        encoded_dict["length"] = paragraph_len

        spans.append(encoded_dict)

        if "overflowing_tokens" not in encoded_dict or (
            "overflowing_tokens" in encoded_dict and len(encoded_dict["overflowing_tokens"]) == 0
        ):
            break
        # tokenizer.encode_plus에서 return_overflowing_tokens=True로 켜면
        # truncate하고 남은 토큰들을 리턴한다, 이를 span_doc_tokens에 다시 넣어 재처리한다
        # 이렇게 하는 이유는 max_seq_length보다 보통 context_text가 길기 때문에
        # 동일한 question-context pair로부터 학습 인스턴스를 stride해 가며 여러 개를 복제
        span_doc_tokens = encoded_dict["overflowing_tokens"]

    for span in spans:
        # Identify the position of the CLS token
        cls_index = span["input_ids"].index(tokenizer.cls_token_id)
        # For training, if our document chunk does not contain an annotation
        # we throw it out, since there is nothing to predict.
        doc_start = span["start"]
        doc_end = span["start"] + span["length"] - 1
        out_of_span = False

        if not (tok_start_position >= doc_start and tok_end_position <= doc_end):
            out_of_span = True

        if out_of_span:
            start_position = cls_index
            end_position = cls_index
        else:
            if tokenizer.padding_side == "left":
                doc_offset = 0
            else:
                doc_offset = len(truncated_query) + sequence_added_tokens

            start_position = tok_start_position - doc_start + doc_offset
            end_position = tok_end_position - doc_start + doc_offset

        feature = QAFeatures(
            input_ids=span["input_ids"],
            attention_mask=span["attention_mask"],
            token_type_ids=span["token_type_ids"],
            start_positions=start_position,
            end_positions=end_position,
        )

        features.append(feature)

    return features


def _squad_convert_examples_to_features(
        examples: List[QAExample],
        tokenizer: PreTrainedTokenizer,
        threads: int = 4,
        max_seq_length: int = 128,
        max_query_length: int = 32,
        doc_stride: int = 64,
        tqdm_enabled: bool = True
):
    threads = min(threads, cpu_count())

    # 병렬처리를 위해 Pool 생성_squad_convert_example_to_features_init 함수 호출함
    with Pool(threads, initializer=_squad_convert_example_to_features_init, initargs=(tokenizer,)) as p:

        # _squad_convert_example_to_features 호출하여 실제 tokenizer 수행함
        annotate_ = partial(
            _squad_convert_example_to_features,
            max_seq_length=max_seq_length,
            doc_stride=doc_stride,
            max_query_length=max_query_length,
        )

        # tokenizer 된 값을 list에 담음
        features = list(
            tqdm(
                p.imap(annotate_, examples, chunksize=32),
                total=len(examples),
                desc="convert squad examples to features",
                disable=not tqdm_enabled,
            )
        )

    new_features = []
    for feature in features:
        if not feature:
            continue
        for f in feature:
            new_features.append(f)
    features = new_features
    del new_features

    # 5개만 출력 해 봄.
    for i, example in enumerate(examples[:10]):
        logger.info("*** Example ***")
        logger.info("question & context: %s" % (" ".join(tokenizer.convert_ids_to_tokens(features[i].input_ids))))
        logger.info("answer: %s" % (" ".join(tokenizer.convert_ids_to_tokens(features[i].input_ids[features[i].start_positions:features[i].end_positions + 1]))))
        logger.info("features: %s" % features[i])

    return features




# Q&A 데이터 셋 생성 하는 함수 
class QADataset(Dataset):

    def __init__(
            self,
            file_fpath: str,      # Q&A 데이터 파일 풀경로
            tokenizer: PreTrainedTokenizer,
            corpus: QACorpus,    # CO
            max_seq_length: int = 128,
            max_query_length: int = 32,
            doc_stride: int = 64,
            overwrite_cache: bool = False,
            convert_examples_to_features_fn=_squad_convert_examples_to_features,
    ):
        # corpus가 null이면 에러 
        if corpus is not None:
            self.corpus = corpus
        else:
            raise KeyError("corpus is not valid")

        assert os.path.isfile(file_fpath), f"Input file path {file_fpath} not found"

         # 캐쉬 파일 생성
        directory, filename = os.path.split(file_fpath)
            
        cached_features_file = os.path.join(
            directory,
            "cached_{}_{}_{}_{}_{}".format(
                tokenizer.__class__.__name__,
                str(max_seq_length),
                str(max_query_length),
                str(doc_stride),
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
                logger.info(
                    f"Loading features from cached file {cached_features_file} [took %.3f s]", time.time() - start
                )
            else:
                corpus_fpath = os.path.join(directory, filename)

                logger.info(f"Creating features from dataset file at {corpus_fpath}")
               
                # corpus.get_examples 함수 호출하여, KorQuADCorpus 파일 불러옴
                examples = self.corpus.get_examples(corpus_fpath)
                
                # _squad_convert_examples_to_features 함수 호출
                self.features = convert_examples_to_features_fn(examples=examples, 
                            tokenizer=tokenizer, 
                            threads=4,
                            max_seq_length=max_seq_length,
                            max_query_length=max_query_length,
                            doc_stride=doc_stride,
                            tqdm_enabled=True)
                
                #if overwrite_cache:
                start = time.time()
                logger.info("Saving features into cached file, it could take a lot of time...")
                
                # 캐쉬 파일 저장
                torch.save(self.features, cached_features_file)
                
                logger.info("Saving features into cached file %s [took %.3f s]", cached_features_file, time.time() - start)

    def __len__(self):
        return len(self.features)

    def __getitem__(self, i):
        return self.features[i]
