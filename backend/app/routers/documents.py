from fastapi import APIRouter, UploadFile 
import uuid
import os
from ..vectorstores import vectorstores

router = APIRouter(tags = ['documents'])

@router.post("/documents")
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
    return {"filename" : filename,"splitted" : splitted[0]}