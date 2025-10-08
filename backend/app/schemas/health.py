from pydantic import BaseModel

class Health(BaseModel):
    status: str
    model_loaded: bool