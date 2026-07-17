import streamlit as st
from datetime import datetime

from api import delete_document


def format_file_size(size_bytes: int) -> str:
    if size_bytes < 1024:
        return f"{size_bytes} B"

    if size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.2f} KB"

    return f"{size_bytes / (1024 * 1024):.2f} MB"


def format_date(date_string: str) -> str:
    date = datetime.fromisoformat(
        date_string.replace("Z", "+00:00")
    )

    return date.strftime("%d %b %Y")


def documents_section(documents):

    st.subheader("Uploaded Documents")

    if not documents["documents"]:
        st.info("No documents uploaded yet.")
        return

    for document in documents["documents"]:

        with st.container(border=True):

            col1, col2 = st.columns([5, 1])

            with col1:

                st.markdown(
                    f"###  {document['filename']}"
                )

                st.write(
                    f" {format_file_size(document['size_bytes'])}"
                )

                st.write(
                    f" {format_date(document['uploaded_at'])}"
                )

            with col2:

                if st.button(
                    "🗑",
                    key=document["document_id"],
                    use_container_width=True,
                ):

                    with st.spinner("Deleting document..."):

                        delete_document(document["document_id"])

                    st.success("Document deleted successfully!")

                    st.rerun()