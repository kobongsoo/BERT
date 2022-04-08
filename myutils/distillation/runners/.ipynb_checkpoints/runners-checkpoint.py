from typing import Dict
from collections import OrderedDict

from catalyst import dl
from catalyst.dl.utils import check_ddp_wrapped
import torch


class DistilMLMRunner(dl.Runner):
    """Simplified huggingface Distiller wrapped with catalyst"""

    def _handle_batch(self, batch: Dict[str, torch.Tensor]):
        if check_ddp_wrapped(self.model):
        #if is_wrapped_with_ddp(self.model):
            teacher, student = (
                self.model.module["teacher"],
                self.model.module["student"],
            )
            print('DistilMLMRunner->ddp_wrapped')
        else:
            teacher, student = self.model["teacher"], self.model["student"]
            print('DistilMLMRunner->not ddp_wrapped')

        teacher.eval()  # manually set teacher model to eval mode
        attention_mask = batch["input_ids"] != 0
        with torch.no_grad():
            #t_logits, t_hidden_states = teacher(batch["input_ids"], attention_mask)
            t_outputs = teacher(batch["input_ids"], attention_mask)
            #print('t_output:{}'.format(type(t_outputs)))
            t_logits = t_outputs[0]
            t_hidden_states = t_outputs[1]
            
            #print('t_logits:{}'.format(t_logits.shape))
            #print('t_hidden_states:{}'.format(t_hidden_states.shape))

        #s_logits, s_hidden_states = student(batch["input_ids"], attention_mask)
        s_outputs = student(batch["input_ids"], attention_mask)
        #print('s_output:{}'.format(type(s_outputs)))
        s_logits = s_outputs[0]
        s_hidden_states = s_outputs[1]
        #print('s_logits:{}'.format(s_logits.shape))
        #print('s_hidden_states:{}'.format(s_hidden_states.shape))
            
        self.output = OrderedDict()
        self.output["attention_mask"] = attention_mask
        self.output["t_hidden_states"] = t_hidden_states
        self.output["s_hidden_states"] = s_hidden_states
        self.output["s_logits"] = s_logits
        self.output["t_logits"] = t_logits
