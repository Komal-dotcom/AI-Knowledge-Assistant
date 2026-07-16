import streamlit as st


def upload_section():

    st.subheader("📄 Upload PDF")

    uploaded_file = st.file_uploader(
        "Choose a PDF",
        type=["pdf"],
    )

    upload_button = st.button(
        "Upload Document",
        use_container_width=True,
    )

    return uploaded_file, upload_button