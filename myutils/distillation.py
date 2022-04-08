import os
import torch
import torch.nn as nn
import torch.nn.functional as F
from typing import Dict, List, Any
from .utils import mlogging

from transformers.models.bert.modeling_bert import BertPreTrainedModel, BertConfig
from transformers.models.bert.modeling_bert import BertEncoder, BertModel

# [bong] mylogging 호출함
#logger = mlogging(loggername='bwpdataset',logfilname='bwdataset')

# ====================================================================
#  distil loss 함수 정의
# => loss 함수는 학생모델이 loss(1), 교사와 학생모델간 cross-entropy loss(2), 교사와 학생모델간 cosine-loss(3) 
# 3가지 인데, 이때 (2)와 (3) loss는 torch.nn.KLDivLoss 함수로 보통 대체 된다.
# 즉 증류 손실함수 = alpha*학생모델이 loss + (1-alpah)*교사/학생모델간 torch.nn.KLDivLoss 함수
#
# 이때 KLDivLoss 함수는 교사와 학생간 다크Knowledge도 학습되도록 교사loss/Temperture와 학생loss/Temperture 식으로,
# Temperture를 지정하는데, 보통 학습할때는 2~10으로 하고, 평가시에는 반드시 1로 해야 한다.
# 그리고 학생모델loss는 전체 loss에 0.1이 되도록 alpha값은 0.1이 좋다고 한다.
#
# * 아래 knowledge_distillation_loss1,2 둘중 하나를 사용하면 됨
#
# 출처 : https://re-code-cord.tistory.com/entry/Knowledge-Distillation-1 
# ====================================================================

def knowledge_distillation_loss1(student_loss, 
                                 student_logits, 
                                 teacher_logits, 
                                 alpha : float = 0.1, 
                                 Temperture : int = 10): 
    
    alpha = alpha 
    T = Temperture 
    # transformer 모델에서는 student_loss가 바로 리턴되므로 굳이 studnet_loss를 구할필요없어서, 주석처리함
    #student_loss = F.cross_entropy(input=logits, target=labels) 
   
    distillation_loss = nn.KLDivLoss(reduction='batchmean')(F.log_softmax(student_logits/T, dim=1), 
                                                            F.softmax(teacher_logits/T, dim=1)) * (T * T) 
    total_loss = alpha*student_loss + (1-alpha)*distillation_loss 
    return total_loss


def knowledge_distillation_loss2(student_loss, 
                                 student_logits, 
                                 teacher_logits, 
                                 Temperture : int = 10): 
    
    T = Temperture 
    
    student_logits = (student_logits / T).F.softmax(1)
    teacher_logits = (teacher_logits / T).F.softmax(1)
    
    crossentropyloss = nn.CrossEntropyLoss()(student_logits, teacher_logits)
    cosineloss = nn.CosineEmbeddingLoss()(teacher_logits, student_logits, torch.ones(teacher_logits.size()[0]))
    
    total_loss = (student_loss + crossentropyloss + cosineloss)/3
    return total_loss
    
    
#===================================================================
# Knowledge distillation 을 위해,
# BertModel 교사 state_dict 을 -> DistilBertMode 학생 state_dict로 복사 하는 함수
#===================================================================
def make_sate_dict_bertmodel_to_distillbertmodel(
        teacher_model,
        layers: List[int] = None
    ):
        """
        Extracts state dict from teacher model

        Args:
            teacher_model: model to extract
            layers: layers indexes to initialize
        """
        if layers is None:
            layers = [0, 2, 4, 7, 9, 11]
            
        state_dict = teacher_model.state_dict()
        compressed_sd = {}

        # extract embeddings
        # 입베딩 파라메터 복사
        for w in ["word_embeddings", "position_embeddings"]:
            compressed_sd[
                f"embeddings.{w}.weight"
            ] = state_dict[f"embeddings.{w}.weight"]
        for w in ["weight", "bias"]:
            compressed_sd[
                f"embeddings.LayerNorm.{w}"
            ] = state_dict[f"embeddings.LayerNorm.{w}"]
            
        # 레이어 파라메터 복사
        # extract encoder
        std_idx = 0
        for teacher_idx in layers:
            for w in ["weight", "bias"]:
                compressed_sd[
                    f"transformer.layer.{std_idx}.attention.q_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"encoder.layer.{teacher_idx}.attention.self.query.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"transformer.layer.{std_idx}.attention.k_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"encoder.layer.{teacher_idx}.attention.self.key.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"transformer.layer.{std_idx}.attention.v_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"encoder.layer.{teacher_idx}.attention.self.value.{w}"  # noqa: E501
                ]

                compressed_sd[
                    f"transformer.layer.{std_idx}.attention.out_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"encoder.layer.{teacher_idx}.attention.output.dense.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"transformer.layer.{std_idx}.sa_layer_norm.{w}"  # noqa: E501
                ] = state_dict[
                    f"encoder.layer.{teacher_idx}.attention.output.LayerNorm.{w}"  # noqa: E501
                ]

                compressed_sd[
                    f"transformer.layer.{std_idx}.ffn.lin1.{w}"  # noqa: E501
                ] = state_dict[
                    f"encoder.layer.{teacher_idx}.intermediate.dense.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"transformer.layer.{std_idx}.ffn.lin2.{w}"  # noqa: E501
                ] = state_dict[
                    f"encoder.layer.{teacher_idx}.output.dense.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"transformer.layer.{std_idx}.output_layer_norm.{w}"  # noqa: E501
                ] = state_dict[
                    f"encoder.layer.{teacher_idx}.output.LayerNorm.{w}"  # noqa: E501
                ]

            std_idx += 1

        return compressed_sd

#===================================================================
# Knowledge distillation 을 위해,
# BertforMaskedLM 교사 state_dict 을 -> DistilBertforMaskedLM 학생 state_dict로 복사 하는 함수
#===================================================================

def make_sate_dict_bertMaskedLM_to_distillbertMaskedLM(
        teacher_model,
        layers: List[int] = None
    ):
        """
        Extracts state dict from teacher model

        Args:
            teacher_model: model to extract
            layers: layers indexes to initialize
        """
        if layers is None:
            layers = [0, 2, 4, 7, 9, 11]
            
        state_dict = teacher_model.state_dict()
        compressed_sd = {}

        # extract embeddings
        # 입베딩 파라메터 복사
        for w in ["word_embeddings", "position_embeddings"]:
            compressed_sd[
                f"distilbert.embeddings.{w}.weight"
            ] = state_dict[f"bert.embeddings.{w}.weight"]
        for w in ["weight", "bias"]:
            compressed_sd[
                f"distilbert.embeddings.LayerNorm.{w}"
            ] = state_dict[f"bert.embeddings.LayerNorm.{w}"]
            
        # 레이어 파라메터 복사
        # extract encoder
        std_idx = 0
        for teacher_idx in layers:
            for w in ["weight", "bias"]:
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.attention.q_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.attention.self.query.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.attention.k_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.attention.self.key.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.attention.v_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.attention.self.value.{w}"  # noqa: E501
                ]

                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.attention.out_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.attention.output.dense.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.sa_layer_norm.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.attention.output.LayerNorm.{w}"  # noqa: E501
                ]

                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.ffn.lin1.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.intermediate.dense.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.ffn.lin2.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.output.dense.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.output_layer_norm.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.output.LayerNorm.{w}"  # noqa: E501
                ]

            std_idx += 1
        #=======================================================================
        # distilbertforMakedLM 일때 추가된 dict 값 설정
        #
        # 교사 BertForMaskedLM
        # 'cls.predictions.bias', 
        #'cls.predictions.transform.dense.weight', 'cls.predictions.transform.dense.bias',
        #'cls.predictions.transform.LayerNorm.weight',  'cls.predictions.transform.LayerNorm.bias', 
        #'cls.predictions.decoder.weight', 'cls.predictions.decoder.bias'
        #
        # 학생 DistilBertForMaskedLM
        #'vocab_transform.weight', 'vocab_transform.bias', 
        #'vocab_layer_norm.weight', 'vocab_layer_norm.bias', 
        #'vocab_projector.weight', 'vocab_projector.bias'
        #=======================================================================
        # => distilbert에는 'cls.predictions.decoder.bias' 값이 없으몰, bert에 해당 값은 복사하지 않음
        compressed_sd[f"vocab_projector.weight"] = state_dict[
            f"cls.predictions.decoder.weight"
        ]
        compressed_sd[f"vocab_projector.bias"] = state_dict[
            f"cls.predictions.bias"
        ]

        for w in ["weight", "bias"]:
            compressed_sd[f"vocab_transform.{w}"] = state_dict[
                f"cls.predictions.transform.dense.{w}"
            ]
            compressed_sd[f"vocab_layer_norm.{w}"] = state_dict[
                f"cls.predictions.transform.LayerNorm.{w}"
            ]
        return compressed_sd
    
#===================================================================
# Knowledge distillation 을 위해,
# BertforSequenceClassification 교사 state_dict 을 
# -> DistilBertforSequenceClassification 학생 state_dict로 복사 하는 함수
#===================================================================
def make_sate_dict_bertSequenceClass_to_distillbertSequenceClass(
        teacher_model,
        layers: List[int] = None
    ):
        """
        Extracts state dict from teacher model

        Args:
            teacher_model: model to extract
            layers: layers indexes to initialize
        """
        if layers is None:
            layers = [0, 2, 4, 7, 9, 11]
            
        state_dict = teacher_model.state_dict()
        compressed_sd = {}

        # extract embeddings
        # 입베딩 파라메터 복사
        for w in ["word_embeddings", "position_embeddings"]:
            compressed_sd[
                f"distilbert.embeddings.{w}.weight"
            ] = state_dict[f"bert.embeddings.{w}.weight"]
        for w in ["weight", "bias"]:
            compressed_sd[
                f"distilbert.embeddings.LayerNorm.{w}"
            ] = state_dict[f"bert.embeddings.LayerNorm.{w}"]
            
        # 레이어 파라메터 복사
        # extract encoder
        std_idx = 0
        for teacher_idx in layers:
            for w in ["weight", "bias"]:
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.attention.q_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.attention.self.query.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.attention.k_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.attention.self.key.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.attention.v_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.attention.self.value.{w}"  # noqa: E501
                ]

                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.attention.out_lin.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.attention.output.dense.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.sa_layer_norm.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.attention.output.LayerNorm.{w}"  # noqa: E501
                ]

                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.ffn.lin1.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.intermediate.dense.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.ffn.lin2.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.output.dense.{w}"  # noqa: E501
                ]
                compressed_sd[
                    f"distilbert.transformer.layer.{std_idx}.output_layer_norm.{w}"  # noqa: E501
                ] = state_dict[
                    f"bert.encoder.layer.{teacher_idx}.output.LayerNorm.{w}"  # noqa: E501
                ]

            std_idx += 1

          #====================================================  
          # DistilBertForSequenceClassification 일때 추가된 dict 값 설정
          #
          # 교사 BertForSequenceClassification 
          #  'bert.pooler.dense.weight',   'bert.pooler.dense.bias', 
          #  'classifier.weight', 'classifier.bias'
          #
          # 학생 DistilBertForSequenceClassification
          # 'pre_classifier.weight', 'pre_classifier.bias', 
          # 'classifier.weight', 'classifier.bias'
          #====================================================  
        for w in ["weight", "bias"]:
            compressed_sd[f"pre_classifier.{w}"] = state_dict[
                f"bert.pooler.dense.{w}"
            ]
            compressed_sd[f"classifier.{w}"] = state_dict[
                f"classifier.{w}"
            ]
            
        return compressed_sd
    
#================================================
# bert 모델 구조를 트리 형태로 보여주는 함수
# 사용법 : 
# roberta = AutoModelForMaskedLM.from_pretrained("bert-base-cased")
# visualize_children(roberta)
#================================================
def visualize_bertmodel_tree(
    object : Any,
    level : int = 0,
) -> None:
    """
    Prints the children of (object) and their children too, if there are any.
    Uses the current depth (level) to print things in a ordonnate manner.
    """
    print(f"{'   ' * level}{level}- {type(object).__name__}")
    try:
        for child in object.children():
            visualize_bertmodel_tree(child, level + 1)
    except:
        pass
    

#================================================
# 학생 bert 모델 만드는 class
# => 교사 bert모델에 12개 hidden layer를 반으로 줄여서 학생 bert를 만든다.
#
# 예시)
# distilbert = bertdistillation(tearch_model)
# student_model = distilbert.make_studentbert()
#================================================
class bertdistillation():
    #=======================================
    # 초기화 입력 인자 : BertPreTrainedModel
    #=======================================
    def __init__(self, 
                 teacher_model: BertPreTrainedModel
                ):
        
        if teacher_model is not None:
            self.teacher_model = teacher_model
        else:
            raise keyError('teacher_model is None!!')
    
    #=======================================
    # 교사 bert 12 hidden layer->6개의 hidden layer로 추출 후 학생 모델에 적용
    # 입력 : teacher : 교사모델 M
    #        student : 학생모델 
    #=======================================
    def distill_bert_weights(self, 
                             teacher : nn.Module,
                             student : nn.Module
                            ):
        """
        Recursively copies the weights of the (teacher) to the (student).
        This function is meant to be first called on a RobertaFor... model, but is then called on every children of that model recursively.
        The only part that's not fully copied is the encoder, of which only half is copied.
        """
            
        # If the part is an entire RoBERTa model or a RobertaFor..., unpack and iterate
        if isinstance(teacher, BertModel) or type(teacher).__name__.startswith('BertFor'):
            for teacher_part, student_part in zip(teacher.children(), student.children()):
                self.distill_bert_weights(teacher_part, student_part)
                
        # Else if the part is an encoder, copy one out of every layer
        elif isinstance(teacher, BertEncoder):
            teacher_encoding_layers = [layer for layer in next(teacher.children())]
            student_encoding_layers = [layer for layer in next(student.children())]
            for i in range(len(student_encoding_layers)):
                student_encoding_layers[i].load_state_dict(teacher_encoding_layers[2*i].state_dict())
                
        # Else the part is a head or something else, copy the state_dict
        else:
            student.load_state_dict(teacher.state_dict())
     
    #=======================================
    # 교사모델을 이용하여 distillate 시킨 학생 모델 생성 하는 함수
     #=======================================
    def make_studentbert(self):
        
        if self.teacher_model is None:
            raise keyError('teacher_model is None!!')
            
        """
        Distilates a RoBERTa (teacher_model) like would DistilBERT for a BERT model.
        The student model has the same configuration, except for the number of hidden layers, which is // by 2.
        The student layers are initilized by copying one out of two layers of the teacher, starting with layer 0.
        The head of the teacher is also copied.
        """
        
        # 교사 configuration 을 얻어옴
        configuration = self.teacher_model.config.to_dict()

        # 교사 configuration에서 hidden_layers 수를 얻어와서 2로 나눔
        configuration['num_hidden_layers'] //= 2

        # 학생 모델에 적용할 configuration 구조 생성(hidden layer가 6개임)
        configuration = BertConfig.from_dict(configuration)

        # 학생모델에 configuration 적용
        self.student_model = type(self.teacher_model)(configuration)

        # 교사모델  hidden_layers weigth 와 bias 값을 학생모델 state_dict에 weigth와 bias들을 적용함
        self.distill_bert_weights(teacher=self.teacher_model, student=self.student_model)

        # 학생모델 리턴
        return self.student_model

    # 교사 학생 모델 리턴 
    @property
    def get_model(self):
        return self.teacher.model, self.student_model
    
        
        
        