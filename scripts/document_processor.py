import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

load_dotenv()

def process_document():
    # Load PDF
    loader = PyPDFLoader(os.getenv('PDF_PATH'))
    documents = loader.load()
    
    # Split text into chunks
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    splits = text_splitter.split_documents(documents)
    
    # Create FAISS vector store
    embedding = OpenAIEmbeddings()
    vectorstore = FAISS.from_documents(splits, embedding)
    
    # Save the vector store
    vectorstore.save_local(os.getenv('VECTOR_DB_PATH'))
    print("FAISS vector store created successfully!")

if __name__ == "__main__":
    process_document()