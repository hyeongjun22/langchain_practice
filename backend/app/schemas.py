from pydantic import BaseModel,Field
from typing import Optional

class ChatRequest(BaseModel):
    message : str 
    collection_name : Optional[str] = None

class ChatResponse(BaseModel):
    answer : str 
    collection_name: Optional[str] = None

class UploadResponse(BaseModel):
    collection_name: str
    chunks_indexed: int
    filename: str