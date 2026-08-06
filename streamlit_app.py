import streamlit as st

from app import initialize_rag, ask_question


st.title("🧠 AI Knowledge Assistant")
st.write("Ask questions about your documents!")

# Cache the expensive initialization
@st.cache_resource
def load_rag():
    return initialize_rag()

client, index, metadata = load_rag()

question = st.text_input("Enter your question:")

if st.button("Ask"):

    if question.strip():

        with st.spinner("Thinking..."):

            answer = ask_question(
                question,
                client,
                index,
                metadata
            )

        st.subheader("Answer")
        st.write(answer)