# streamlit_app.py
import streamlit_app as st
from src.search_manager import SearchManager
from src.file_search_client import FileSearchClient
from src.document_processor import DocumentProcessor

st.set_page_config(page_title="RAG Search System", page_icon="🔍")

@st.cache_resource
def init_system():
    client = FileSearchClient()
    return SearchManager(client), DocumentProcessor(client)

search_manager, doc_processor = init_system()

st.title("🔍 Document Search System")

# Sidebar for store selection
stores = search_manager.client.list_stores()
store_names = [s['display_name'] for s in stores]
selected_store = st.sidebar.selectbox("Select Store", store_names)

# Main query interface
query = st.text_input("Ask a question:", placeholder="What information do you need?")

if st.button("Search") and query:
    with st.spinner("Searching..."):
        result = search_manager.search_and_generate(query, selected_store)
        st.success("Answer:")
        st.write(result.answer)
        
        if result.citations:
            st.subheader("📚 Sources:")
            for cite in result.citations:
                st.caption(f"• {cite.get('title', 'Document')}")

# File upload
uploaded_file = st.sidebar.file_uploader("Upload Document")
if uploaded_file:
    with st.spinner("Uploading..."):
        doc_processor.upload_file(uploaded_file, selected_store)
        st.success("Uploaded successfully!")