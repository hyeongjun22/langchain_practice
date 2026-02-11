import chromadb
from dotenv import load_dotenv
import os  
from langchain_chroma import Chroma
from langchain_openai import OpenAI
from langchain_openai import OpenAIEmbeddings
from langchain_core.runnables import RunnablePassthrough
from app.prompts import system_prompt_template, humna_prompt_template
from langchain_core.prompts import ChatPromptTemplate, HumanMessagePromptTemplate, SystemMessagePromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_openai import ChatOpenAI

class chains:
    def __init__(self):
        load_dotenv()
        host = os.environ.get('CHROMA_HOST')
        port = os.environ.get('CHROMA_PORT')
        chroma_client = chromadb.HttpClient(host = host,port = port ) 
        embeddings = OpenAIEmbeddings(model = "text-embedding-3-small")
        collection_name = "sesac0207"

        self.chroma_store = Chroma(
            client = chroma_client,
            collection_name = collection_name,
            embedding_function=embeddings
        )
    def format_docs(self,docs):
        return "\n\n".join([doc.page_content for doc in docs])
    
    def create_chain(self,query):
        prompt = ChatPromptTemplate(messages = [
            ("system",system_prompt_template),
            ("human",humna_prompt_template)
        ])
        output_parser = StrOutputParser()
        llm = ChatOpenAI(model="gpt-5-nano")
        retriever = self.chroma_store.as_retriever(search_type="similarity",search_kwargs={"k":3})
        retriever_chain = retriever | self.format_docs
        rag_chain = {"context" : retriever_chain, "question": RunnablePassthrough() } | prompt | llm | output_parser
        return rag_chain.invoke(query)