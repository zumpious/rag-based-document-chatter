import streamlit as st
from src.rag.setup import setup_rag
from src.utils.config import get_env_vars
from typing import Dict, List, Any

def init_session_state() -> None:
    """Initialize Streamlit session state variables.
    
    Sets up persistent chat history and RAG chain for the Streamlit app.
    Creates new instances if they don't exist in the session state.
    
    Returns:
        None
    """    
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "qa_chain" not in st.session_state:
        env_vars = get_env_vars()
        st.session_state.qa_chain = setup_rag(env_vars['vector_db_path'], env_vars['gpt_model'])

def process_query(query: str, chat_history: List[Dict[str, str]], k_value: int, fetch_k: int) -> Dict[str, Any]:
    """Process user query using RAG system with debug information.
    
    Args:
        query: User's input question
        chat_history: List of previous chat messages
        k_value: Number of final chunks to retrieve
        fetch_k: Number of initial candidates to consider
    
    Returns:
        Dict containing:
            - answer: Generated response
            - source_documents: Retrieved document chunks
            - has_context: Whether context was found
            - raw_docs: Raw retrieved documents
             - similarity_scores: Similarity scores for chunks
    """
    try:
        # Get retriever with parameters
        retriever = st.session_state.qa_chain.retriever
        retriever.search_kwargs['k'] = k_value
        retriever.search_kwargs['fetch_k'] = fetch_k
        
        raw_docs = retriever.get_relevant_documents(query)
        
        response = st.session_state.qa_chain({
            'question': query,
            'chat_history': [(m["content"], "") for m in chat_history if m["role"] == "user"],
            'return_source_documents': True
        })
        
        return {
            'answer': response['answer'],
            'source_documents': response.get('source_documents', []),
            'has_context': len(response.get('source_documents', [])) > 0,
            'raw_docs': raw_docs,
            'similarity_scores': [doc.metadata.get('score', 'N/A') if hasattr(doc, 'metadata') else 'N/A' 
                                for doc in raw_docs]
        }
    except Exception as e:
        st.error(f"RAG Error: {str(e)}")
        return {
            'answer': "Error processing query",
            'source_documents': [],
            'has_context': False,
            'raw_docs': [],
            'similarity_scores': []
        }

def main() -> None:
    """Main Streamlit application"""
    st.set_page_config(
        page_title="Thesis Research Assistant",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    init_session_state()

    with st.sidebar:
        st.title("🎓 Settings")
        st.divider()
        
        st.subheader("RAG Parameters")
        k_value = st.slider("Number of chunks to retrieve", 1, 10, 4)
        fetch_k = st.slider("Number of candidates to consider (fetch_k)", 
                       min_value=k_value,  # Must be >= k_value
                       max_value=20, 
                       value=max(k_value * 2, 8))         
        st.divider()
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    st.title("🎓 Local Document Research Assistant")
    st.subheader("Ask questions about your document...")

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What would you like to know about your document?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Researching..."):
                response = process_query(prompt, st.session_state.messages[:-1], k_value, fetch_k)
                
                st.markdown(response['answer'])
                
                # Use debugger mode to show retrived chunks and similarity scoers
                with st.expander("🔍 RAG Debug Information", expanded=True):
                    st.markdown("### Retrieved Context Analysis")
                    
                    if response['has_context']:
                        st.markdown(f"**Number of chunks retrieved:** {len(response['source_documents'])}")
                        
                        for idx, (doc, score) in enumerate(zip(response['raw_docs'], 
                                                             response['similarity_scores']), 1):
                            st.markdown(f"**Chunk {idx}** (Similarity: {score})")
                            st.markdown(f"```\n{doc.page_content[:300]}...\n```")
                            if hasattr(doc, 'metadata'):
                                st.json(doc.metadata)
                            st.divider()
                    else:
                        st.warning("⚠️ No context was retrieved from the document!")
                        st.markdown("This means the response was generated without RAG support.")

        st.session_state.messages.append({
            "role": "assistant", 
            "content": response['answer']
        })

if __name__ == "__main__":
    main()