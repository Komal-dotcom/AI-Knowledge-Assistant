import streamlit as st

from api import (
    get_documents,
    upload_document,
)
from components.upload import upload_section

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 AI Knowledge Assistant")

uploaded_file, upload_button = upload_section()

if uploaded_file and upload_button:

    with st.spinner("Uploading document..."):

        upload_document(uploaded_file)

    st.success("Document uploaded successfully!")

    st.rerun()

st.divider()

st.subheader("📚 Uploaded Documents")

try:
    documents = get_documents()

    st.json(documents)

except Exception as e:
    st.error(str(e))