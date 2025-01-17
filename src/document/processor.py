from typing import List
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document

def process_document(pdf_path: str, vector_db_path: str) -> FAISS:
    """Process PDF document and create FAISS vector store"""
    # Load PDF
    loader = PyPDFLoader(pdf_path)
    documents: List[Document] = loader.load()
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=600,
        length_function=len,
        is_separator_regex=False
    )
    splits = text_splitter.split_documents(documents)
    
    # Create and save FAISS vector store
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(splits, embedding)
    vectorstore.save_local(vector_db_path)
    
    return vectorstore