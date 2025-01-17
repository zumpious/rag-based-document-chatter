import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain

def setup_rag(vector_store_path: str):
    embedding = OpenAIEmbeddings()
    
    if not os.path.exists(vector_store_path):
        raise FileNotFoundError("Vector store not found. Please run document processing first.")
        
    vectorstore = FAISS.load_local(
        folder_path=vector_store_path,
        embeddings=embedding,
        allow_dangerous_deserialization=True
    )
    
    llm = ChatOpenAI(model_name="gpt-4", temperature=0)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
        return_source_documents=True
    )