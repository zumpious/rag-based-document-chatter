from src.document.processor import process_document
from src.utils.config import get_env_vars

def main():
    """Main script to process document"""
    env_vars = get_env_vars()
    try:
        process_document(env_vars['pdf_path'], env_vars['vector_db_path'])
        print("FAISS vector store created successfully!")
    except Exception as e:
        print(f"Error processing document: {str(e)}")

if __name__ == "__main__":
    main()