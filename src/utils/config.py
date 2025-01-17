import os
from dotenv import load_dotenv

load_dotenv()

def get_env_vars():
    return {
        'pdf_path': os.getenv('PDF_PATH'),
        'vector_db_path': os.getenv('VECTOR_DB_PATH'),
        'openai_key': os.getenv('OPENAI_API_KEY')
    }