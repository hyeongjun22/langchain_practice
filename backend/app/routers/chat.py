from fastapi import APIRouter
from app.schemas import ChatResponse
from app.chains import chains
router = APIRouter(tags = ['chat'])

@router.post("/chat" , response_model=ChatResponse)
async def chat(query: str):
    chains_instance = chains()
    answer = chains_instance.create_chain(query)
    return {"answer": answer , "collection_name": "sesac0207"}