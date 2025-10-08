from typing import List, Dict
import torch
import gc
from app.core.logger import get_logger
from app.core.config import settings
import asyncio

logger = get_logger(__name__)

class ChatService:

    def __init__(self, model, tokenizer):
        self.model = model
        self.tokenizer = tokenizer
        self.device = next(self.model.parameters()).device

    async def chat(self, message: str, history: List[Dict]) -> str:
        # Use lock to prevent concurrent generation on same model
        async with asyncio.Lock():
            return await asyncio.to_thread(self._generate_response, message, history)
        
    def _generate_response(self, message: str, history: List[Dict]):

        inputs = None
        outputs = None
    
        try:
            messages = self._prepare_messages(message, history)
            input_text = self.tokenizer.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)

            inputs = self.tokenizer(input_text, return_tensors="pt", return_attention_mask=True, padding=True, truncation=True, max_length=2048).to(self.device)

            input_ids = inputs['input_ids'].to(self.device)
            attention_mask = inputs['attention_mask'].to(self.device)

            del inputs

            with torch.inference_mode():
                with torch.amp.autocast(device_type='mps' if self.device.type == 'mps' else 'cpu'):
                    
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
                        return_dict_in_generate=False,
                        output_attentions=False,
                        output_hidden_states=False
                    )
                    
            input_length = input_ids.shape[-1]
            response_ids = outputs[0][input_length:]
            response_text = self.tokenizer.decode(
                response_ids,
                skip_special_tokens=True
            ).strip()

            if not response_text:
                response_text = "I'm not sure how to respond to that. Could you rephrase your question?"

            return response_text
            
        except Exception as e:
            logger.error(f"Error while generating response: {e}")
            raise
        finally:
            for tensor in [input_ids, attention_mask, outputs, response_ids]:
                if tensor is not None:
                    del tensor

            if self.device.type == "mps":
                torch.mps.empty_cache()
            gc.collect()

    def _prepare_messages(self, message: str, history: List[Dict]) -> List[Dict]:
        messages = []
        for msg in history[-settings.max_history * 2:]:
            messages.append({
                "role": msg.get("role", "user"), 
                "content": msg.get("content", "")
            })
        messages.append({"role": "user", "content": message})
        return messages

    def _aggressive_cleanup(self):
        """
        Aggressive memory cleanup after each generation
        """
        try:
            # Clear model's KV cache if it exists
            if hasattr(self.model, 'past_key_values'):
                self.model.past_key_values = None

            if hasattr(self.model, 'reset_states'):
                self.model.reset_states()
            
            # Clear any cached states in the model
            if hasattr(self.model, '_reset_cache'):
                self.model._reset_cache()
                
            if self.device.type == 'mps':
                torch.mps.empty_cache()
                # MPS-specific: force synchronization
                torch.mps.synchronize()
            
            # Force Python garbage collection
            for _ in range(3):
                gc.collect()
            
        except Exception as e:
            logger.warning(f"Cleanup warning: {e}")
    
    def clear_memory(self):
        """
        Public method for manual memory clearing (can be called periodically)
        """
        logger.info("Performing deep memory cleanup")
        self._aggressive_cleanup()
        
        gc.collect()
        gc.collect() 