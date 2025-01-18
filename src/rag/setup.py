import os
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain

def setup_rag(vector_store_path: str, model_name: str = "gpt-4o-mini") -> ConversationalRetrievalChain:
    """Set up Retrieval-Augmented Generation (RAG) system.
    
    Loads a FAISS vector store from disk, initializes OpenAI embeddings,
    and creates a conversational retrieval chain for question answering
    with document context.

    Args:
        vector_store_path: Directory path containing FAISS index

    Returns:
        ConversationalRetrievalChain configured with GPT-4 and document retriever

    Raises:
        FileNotFoundError: If vector store is not found at specified path
    """
    embedding = OpenAIEmbeddings()
    
    if not os.path.exists(vector_store_path):
        raise FileNotFoundError("Vector store not found. Please run document processing first.")
        
    vectorstore = FAISS.load_local(
        folder_path=vector_store_path,
        embeddings=embedding,
        allow_dangerous_deserialization=True
    )
    
    llm = ChatOpenAI(model_name=model_name, temperature=0)
    return ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vectorstore.as_retriever(),
        return_source_documents=True
    )