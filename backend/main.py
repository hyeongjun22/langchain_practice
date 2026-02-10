from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.documents import router as documents_router
from app.routers.chat import router as chat_router


app = FastAPI(title = "RAG chat API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials = True
)

@app.get("/health")
def health():
    return{"msg": "ok"}

app.include_router(documents_router)
app.include_router(chat_router)