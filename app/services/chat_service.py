from typing import List, Dict
import torch
import gc
from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)

class ChatService:

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        
    def chat(self, message: str, history: List[Dict]):

        inputs = None
        outputs = None
    
        try:
            messages = []

            for msg in history[-settings.max_history*2:]:
                messages.append({"role": msg.get("role", "user"), "content": msg.get("content", "")})

            messages.append({"role": "user", "content": message})

            input_text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

            device = next(self.model.parameters()).device
            inputs = self.tokenizer(input_text, return_tensors="pt", return_attention_mask=True, padding=True, truncation=True, max_length=2048).to(device)

            with torch.no_grad():
                with torch.amp.autocast(device_type='mps' if device.type == 'mps' else 'cpu'):
                    # Create a clean copy of inputs to avoid memory sharing
                    input_ids = inputs['input_ids'].clone().detach()
                    attention_mask = inputs['attention_mask'].clone().detach()
                    
                    outputs = self.model.generate(
                        input_ids=input_ids,
                        attention_mask=attention_mask,
                        max_new_tokens=settings.max_new_tokens,
                        do_sample=True,
                        temperature=settings.temperature,
                        top_p=settings.top_p,
                        pad_token_id=self.tokenizer.pad_token_id or self.tokenizer.eos_token_id,
                        eos_token_id=self.tokenizer.eos_token_id,
                        repetition_penalty=1.1,
                        use_cache=False,
                        return_dict_in_generate=False
                    )
                    
                    # Clean up temporary tensors
                    del input_ids, attention_mask
            
            response_text = self.tokenizer.decode(
                outputs[0][inputs['input_ids'].shape[-1]:],
                skip_special_tokens=True
            ).strip()


            if not response_text:
                response_text = "I'm not sure how to respond to that. Could you rephrase your question?"

            return response_text
            
        except Exception as e:
            logger.error(f"Error while generating response: {e}")
            gc.collect()
            return "I'm not sure how to respond to that. Could you rephrase your question?"

        finally:
            # Safely clean up tensors
            try:
                if inputs is not None:
                    if isinstance(inputs, dict):
                        for key in list(inputs.keys()):
                            if torch.is_tensor(inputs[key]):
                                inputs[key] = inputs[key].detach().cpu()
                    del inputs
                
                if outputs is not None:
                    if torch.is_tensor(outputs):
                        outputs = outputs.detach().cpu()
                    del outputs
                    
                if torch.backends.mps.is_available():
                    torch.mps.empty_cache()
                    
                gc.collect()
            except Exception as e:
                logger.error(f"Error during cleanup: {str(e)}")
                pass