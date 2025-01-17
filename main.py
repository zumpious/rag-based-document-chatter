# main.py
import streamlit as st
from src.rag.setup import setup_rag
from src.utils.config import get_env_vars
from typing import Dict, List, Optional, Any

def init_session_state() -> None:
    """Initialize Streamlit session state variables"""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "qa_chain" not in st.session_state:
        env_vars = get_env_vars()
        st.session_state.qa_chain = setup_rag(env_vars['vector_db_path'])

def process_query(query: str, chat_history: List[Dict[str, str]]) -> Dict[str, Any]:
    """Process user query using RAG system with debug info"""
    try:
        # Get retriever with parameters
        retriever = st.session_state.qa_chain.retriever
        retriever.search_kwargs['k'] = 4  # Get more context chunks
        retriever.search_kwargs['fetch_k'] = 8  # Fetch more candidates
        
        # Get raw documents for debugging
        raw_docs = retriever.get_relevant_documents(query)
        
        # Process query
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
    # Page configuration
    st.set_page_config(
        page_title="Thesis Research Assistant",
        page_icon="🎓",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # Initialize session
    init_session_state()

    # Sidebar
    with st.sidebar:
        st.title("🎓 Settings")
        st.divider()
        
        # RAG Settings
        st.subheader("RAG Parameters")
        k_value = st.slider("Number of chunks to retrieve", 1, 10, 4)
        fetch_k = st.slider("Number of candidates to consider", 4, 20, 8)
        
        st.divider()
        if st.button("Clear Chat History"):
            st.session_state.messages = []
            st.rerun()

    # Main chat interface
    st.title("🎓 Thesis Research Assistant")
    st.subheader("Ask questions about your thesis")

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input
    if prompt := st.chat_input("What would you like to know about your thesis?"):
        # Add user message
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate response
        with st.chat_message("assistant"):
            with st.spinner("Researching..."):
                response = process_query(prompt, st.session_state.messages[:-1])
                
                # Display main response
                st.markdown(response['answer'])
                
                # Enhanced debug expander
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

        # Add assistant response to history
        st.session_state.messages.append({
            "role": "assistant", 
            "content": response['answer']
        })

if __name__ == "__main__":
    main()