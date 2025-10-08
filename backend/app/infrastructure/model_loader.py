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

        if torch.cuda.is_available():
            device_map = "auto"
            torch_dtype = torch.float16
            logger.info("Using CUDA device")
        elif torch.backends.mps.is_available():
            device_map = "mps"
            torch_dtype = torch.float16
            logger.info("Using MPS device")
        else:
            device_map = "cpu"
            torch_dtype = torch.float32
            logger.info("Using CPU device")

        model = AutoModelForCausalLM.from_pretrained(self.model_name, dtype=torch_dtype, device_map=device_map, low_cpu_mem_usage=True, max_memory={"mps": settings.max_memory_mps, "cpu": settings.max_memory_cpu})

        model.eval()
        for param in model.parameters():
            param.requires_grad = False
    
        logger.info(f"Model loaded successfully: {self.model_name} on {device_map}")
        return {"model": model, "tokenizer": tokenizer}