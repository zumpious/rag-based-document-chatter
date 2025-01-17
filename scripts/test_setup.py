# test_setup.py
from src.rag.setup import setup_rag
from src.utils.config import get_env_vars
from typing import Dict, Optional

def test_query(query: str) -> Optional[Dict]:
    """Test RAG setup with a single query"""
    try:
        env_vars = get_env_vars()
        qa_chain = setup_rag(env_vars['vector_db_path'])
        
        result = qa_chain({
            'question': query,
            'chat_history': []
        })
        
        return {
            'answer': result['answer'],
            'sources': [doc.page_content[:200] for doc in result.get('source_documents', [])]
        }
        
    except FileNotFoundError as e:
        print("❌ Vector store not found. Run document processing first.")
        return None
    except Exception as e:
        print(f"❌ Error during test: {str(e)}")
        return None

def main():
    """Test FAISS setup and RAG functionality"""
    print("🔍 Testing RAG Setup...")
    
    try:
        # Test single query
        user_input = input("\n📝 Enter a test question: ")  # Changed variable name
        result = test_query(user_input)  # Using new variable name
        
        if result:
            print("\n✅ RAG Setup Test Successful!")
            print("\n🤖 Response:", result['answer'])
            
            if result['sources']:
                print("\n📚 Sources Found:")
                for idx, source in enumerate(result['sources'], 1):
                    print(f"\nSource {idx}:\n{source}...")
        
    except KeyboardInterrupt:
        print("\n\n❌ Test cancelled by user")
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")

if __name__ == "__main__":
    main()