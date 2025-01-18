# 📚 RAG Based Local Document Chatter

A simple RAG system that enables you to have interactive conversations with your PDF documents using OpenAI's GPT models and FAISS vector storage.

## 🌟 Features

- PDF document processing and vectorization
- FAISS similarity search
- Interactive Streamlit chat interface
- Configurable RAG parameters
- Debug mode for retrieval analysis
- Chat history persistence


## 🚀 Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/zumpious/rag-based-document-chatter
   cd rag-based-document-chatter
   ```

2. Create .env and set up your environment variables:
   ```bash
   cp .env.template .env   
   ```

3. Create and activate virtual environment (Optional):
   ```bash
   python -m venv venv
   source venv/bin/activate 
   ```

4. Install dependencies (Optional):
   ```bash
   pip install -r requirements.txt
   ```


## 📖 Usage

1. Process your document and create FAISS vector embedding:
   ```bash
   python scripts/process_document.py  
   ```

2. Verify setup (optional):
   ```bash
   python scripts/test_setup.py   
   ```

3. Run the chat interface:
   ```bash
   streamlit run main.py   
   ```

## 🐳 Docker Setup

1. Build the Docker image:
   ```bash
   docker build -t rag_app .
   ```

2. Run the container:
   ```bash
   docker run -d -p 8501:8501 --name rag_app rag_app
   ```
   
3. Acess the application:
   - Open http://localhost:8501 in your browser

## 🐋 Docker Compose Setup

1. Build and start the container:
   ```bash
   docker compose up -d
   ````

2. Access the application:
   - Open http://localhost:8501 in your browser
