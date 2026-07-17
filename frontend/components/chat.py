import streamlit as st


def chat_section():

    st.subheader("💬 Ask a Question")

    question = st.text_area(
        "Question",
        placeholder="Ask anything about your uploaded documents...",
        height=120,
        label_visibility="collapsed",
    )

    ask_button = st.button(
        "Ask AI",
        use_container_width=True,
    )

    return question, ask_button