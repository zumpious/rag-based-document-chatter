from src.document.processor import process_document
from src.utils.config import get_env_vars

def main():
    """Main script to process document"""
    print("🚀 Starting Document Processing...")
    env_vars = get_env_vars()
    
    try:
        print("\n📑 Loading PDF document...")
        print(f"   Path: {env_vars['pdf_path']}")
        
        print("\n🔄 Processing document...")
        process_document(env_vars['pdf_path'], env_vars['vector_db_path'])
        
        print("\n✅ FAISS vector store created successfully!")
        print(f"   Saved to: {env_vars['vector_db_path']}")
        print("\n🎉 Document processing complete! You can now use the RAG system.")
        
    except FileNotFoundError:
        print("\n❌ Error: PDF file not found!")
        print("   Please check your PDF_PATH in .env file")
    except Exception as e:
        print(f"\n❌ Error processing document: {str(e)}")
        print("   Please check your configuration and try again.")

if __name__ == "__main__":
    main()