import streamlit as st

from api import (
    get_documents,
    upload_document,
    ask_question,
)
from pathlib import Path
from components.upload import upload_section
from components.documents import documents_section
from components.chat import chat_input_section

css_path = Path(__file__).parent / "assets" / "style.css"

with open(css_path) as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True,
    )

# -------------------- Page Config --------------------

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# -------------------- Session State --------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------- Sidebar --------------------

documents = []
with st.sidebar:

    st.title("📂 Documents")

    # Upload Section
    uploaded_file, upload_button = upload_section()

    st.divider()

    # Documents Section
    try:
        documents = get_documents()

        st.caption(f"{len(documents)} document(s) uploaded")

        documents_section(documents)

    except Exception as e:
        st.error(str(e))


# -------------------- Upload Logic --------------------

if uploaded_file and upload_button:

    with st.spinner("Uploading document..."):

        upload_document(uploaded_file)

    st.success("Document uploaded successfully!")

    st.rerun()


# -------------------- Main Page --------------------

col1, col2 = st.columns([6, 1])

with col1:
    st.title("AI Knowledge Assistant")
    st.caption("Ask questions about your uploaded documents.")

with col2:
    st.write("")  # Align button vertically

    if st.button("🗑 Clear"):
        st.session_state.messages = []
        st.rerun()

st.divider()
# Welcome message
if not st.session_state.messages:
    st.subheader("Welcome to AI Knowledge Assistant")

    st.markdown(
    """
    Upload one or more PDF documents using the sidebar.

    Try asking

    - Summarize this document
    - What are the key concepts?
    - Explain this topic in simple terms etc.
    """
    )

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if documents:
    question = chat_input_section()
else:
    question = None

    st.warning(
        "Upload at least one document to start chatting."
    )

if question:

    # Display user's message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": question,
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    try:

        with st.spinner("Thinking..."):

            response = ask_question(question)

        answer = response["answer"]

        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": answer,
            }
        )

        with st.chat_message("assistant"):
            st.markdown(answer)

    except Exception as e:

        st.error(str(e))