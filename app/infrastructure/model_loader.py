from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from app.core.logger import get_logger
from app.core.config import settings

logger = get_logger(__name__)

class ModelLoader:

    def __init__(self, model_name):
        self.model_name = model_name

    def load(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForCausalLM.from_pretrained(self.model_name, torch_dtype=torch.float16, device_map="auto", low_cpu_mem_usage=True, max_memory={"mps": settings.max_memory_mps, "cpu": settings.max_memory_cpu})

        model.eval()
        for param in model.parameters():
            param.requires_grad = False
    
        logger.info(f"Model loaded successfully: {self.model_name}")
        return {"model": model, "tokenizer": tokenizer}