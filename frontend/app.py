import streamlit as st

from api import (
    get_documents,
    upload_document,
    ask_question,
)

from components.upload import upload_section
from components.documents import documents_section
from components.chat import chat_input_section


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
st.caption("Ask questions about your uploaded documents.")

st.divider()

# Display chat history
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = chat_input_section()

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