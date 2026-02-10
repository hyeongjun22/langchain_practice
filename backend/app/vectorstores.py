from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import PDFPlumberLoader
import chromadb
from dotenv import load_dotenv
import os
from langchain_chroma import Chroma
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
import getpass

class vectorstores:
    def __init__(self):
        pass
    def load(self,file_path):
        loader = PDFPlumberLoader(file_path)
        return loader.load()

    def split(self,data):
        splitter = RecursiveCharacterTextSplitter(
            chunk_size = 1000,
            chunk_overlap = 150,
            separators = ["\n\n","\n",". "," ",""],
            add_start_index = True
        )
        
        chunks = splitter.split_documents(data)
        print(len(chunks),len(chunks))
        return chunks
    
    def insert(self,chunks):
        load_dotenv()
        host = os.environ.get('CHROMA_HOST')
        port = os.environ.get('CHROMA_PORT')
        chroma_client = chromadb.HttpClient(host = host,port = port ) 
        embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")
        collection_name = "sesac0207"

        chroma_store = Chroma(
            client = chroma_client,
            collection_name = collection_name,
            embedding_function=embeddings
        )

        chroma_store.add_documents(chunks)