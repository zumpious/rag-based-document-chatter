import os
from dotenv import load_dotenv

load_dotenv()


def get_env_vars() -> dict:
    """Get environment variables needed for RAG system.

    Returns:
        dict: Environment variables including:
            - pdf_path: Path to source PDF document
            - vector_db_path: Path to FAISS vector store
            - openai_key: OpenAI API key
            - gpt_model: OpenAI model name to use
    """
    return {
        "pdf_path": os.getenv("PDF_PATH"),
        "vector_db_path": os.getenv("VECTOR_DB_PATH"),
        "openai_key": os.getenv("OPENAI_API_KEY"),
        "gpt_model": os.getenv("GPT_MODEL", "gpt-4o-mini"),
    }
