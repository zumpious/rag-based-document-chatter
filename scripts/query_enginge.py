from dotenv import load_dotenv
import os
from langchain_openai import ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.chains import ConversationalRetrievalChain

load_dotenv()

def setup_rag():
    try:
        # Load the FAISS vector store with safe deserialization
        embedding = OpenAIEmbeddings()
        vector_store_path = os.getenv('VECTOR_DB_PATH')
        
        if not os.path.exists(vector_store_path):
            raise FileNotFoundError("Vector store not found. Please run document_processor.py first.")
            
        vectorstore = FAISS.load_local(
            folder_path=vector_store_path,
            embeddings=embedding,
            allow_dangerous_deserialization=True  # Only for trusted, local files
        )
        
        # Setup RAG chain
        llm = ChatOpenAI(model_name="gpt-4", temperature=0)
        qa_chain = ConversationalRetrievalChain.from_llm(
            llm=llm,
            retriever=vectorstore.as_retriever(search_kwargs={'k': 3}),
            return_source_documents=True
        )
        return qa_chain
    
    except Exception as e:
        print(f"Error setting up RAG: {str(e)}")
        raise

def query_thesis(query: str, chat_history=[]):
    try:
        qa_chain = setup_rag()
        result = qa_chain({'question': query, 'chat_history': chat_history})
        return result['answer']
    except Exception as e:
        return f"Error processing query: {str(e)}"

if __name__ == "__main__":
    print("RAG Query System initialized. Type 'quit' to exit.")
    while True:
        try:
            query = input("\nEnter your question (or 'quit' to exit): ")
            if query.lower() == 'quit':
                break
            response = query_thesis(query)
            print("\nResponse:", response)
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except Exception as e:
            print(f"\nError: {str(e)}")