import streamlit as st

from api import (
    get_documents,
    upload_document,
    ask_question,
)

from components.upload import upload_section
from components.documents import documents_section
from components.chat import chat_section


# -------------------- Page Config --------------------

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="",
    layout="wide",
    initial_sidebar_state="collapsed",
)


# -------------------- Sidebar --------------------

with st.sidebar:

    st.title("Documents")

    try:
        documents = get_documents()
        documents_section(documents)

    except Exception as e:
        st.error(str(e))

    st.divider()

    uploaded_file, upload_button = upload_section()


# -------------------- Upload Logic --------------------

if uploaded_file and upload_button:

    with st.spinner("Uploading document..."):

        upload_document(uploaded_file)

    st.success("Document uploaded successfully!")

    st.rerun()


# -------------------- Main Page --------------------

st.title("AI Knowledge Assistant")

question, ask_button = chat_section()


# -------------------- Chat Logic --------------------

if ask_button:

    if not question.strip():

        st.warning("Please enter a question.")

    else:

        try:

            with st.spinner("Thinking..."):

                response = ask_question(question)

            st.divider()

            st.subheader("Answer")

            st.write(response["answer"])

        except Exception as e:

            st.error(str(e))