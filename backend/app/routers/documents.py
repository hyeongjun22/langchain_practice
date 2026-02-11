from fastapi import APIRouter, UploadFile 
import uuid
import os
from ..vectorstores import vectorstores
from app.schemas import UploadResponse


router = APIRouter(tags = ['documents'])

@router.post("/documents/upload", response_model=UploadResponse)
async def chat(file: UploadFile):
    Upload_DIR = "./upload"
    content = await file.read()
    filename = f"{str(uuid.uuid4())}.pdf"
    with open(os.path.join(Upload_DIR,filename),"wb") as fp:
        fp.write(content)
    

    vectorstore = vectorstores()
    load = vectorstore.load(os.path.join(Upload_DIR,filename))
    splitted = vectorstore.split(load)
    vectorstore.insert(splitted)
    return UploadResponse(
        collection_name="sesac0207",
        chunks_indexed=len(splitted),
        filename=filename
    )