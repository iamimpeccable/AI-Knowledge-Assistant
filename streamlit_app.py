
import os
import subprocess
from pathlib import Path

import streamlit as st
from dotenv import load_dotenv
from google import genai

from utils.search import search_documents
from vector_store.vector_store import load_vector_store

load_dotenv()

st.set_page_config(
    page_title="AI Knowledge Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 AI Knowledge Assistant")
st.write("Find documents on your computer using natural-language questions.")


# Load the saved index; do not rebuild it when Streamlit starts.
@st.cache_resource
def get_local_index():
    return load_vector_store()


try:
    index, metadata = get_local_index()
except Exception as error:
    st.error(f"Could not load the saved index: {error}")
    st.stop()

if index is None or index.ntotal == 0:
    st.error("No saved index found. Run `python build_index.py` first.")
    st.stop()

indexed_documents = len({
    item["file_path"] for item in metadata.values()
})

st.success(
    f"Ready to search {indexed_documents:,} documents "
    f"({index.ntotal:,} text chunks)."
)


# Keep search results across Streamlit reruns so file buttons work.
if "search_results" not in st.session_state:
    st.session_state.search_results = []

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

with st.form("document_search"):
    question = st.text_input(
        "What documents are you looking for?",
        placeholder="Find research papers about adversarial attacks",
    )
    submitted = st.form_submit_button("🔍 Search documents")

if submitted:
    if not question.strip():
        st.warning("Please enter a question.")
    else:
        with st.spinner("Searching your local documents..."):
            try:
                matches = search_documents(
                    question.strip(),
                    index,
                    metadata,
                    top_k=100,
                )

                # Keep the strongest matching chunk for each document.
                best_by_path = {}
                for match in matches:
                    path = match["file_path"]
                    if (
                        path not in best_by_path
                        or match["distance"]
                        < best_by_path[path]["distance"]
                    ):
                        best_by_path[path] = match

                # Show the five strongest document matches.
                results = sorted(
                    best_by_path.values(),
                    key=lambda item: item["distance"],
                )[:5]

                # Summaries are optional; local search works without Gemini.
                api_key = (
                    os.getenv("GEMINI_API_KEY")
                    or os.getenv("Gemini_API_KEY")
                )

                client = genai.Client(api_key=api_key) if api_key else None

                for result in results:
                    result["summary"] = result["chunk"][:700]

                    if client:
                        prompt = f"""
You help users find files on their computer.

Question: {question.strip()}
Filename: {result['filename']}

Relevant excerpt:
{result['chunk'][:4000]}

In 2-3 concise sentences, explain what this excerpt contains
and how it relates to the question. Use only information
supported by the excerpt.
"""
                        try:
                            response = client.models.generate_content(
                                model="gemini-2.5-flash",
                                contents=prompt,
                            )
                            if response.text:
                                result["summary"] = response.text
                        except Exception:
                            # Keep the local excerpt if summarization fails.
                            pass

                st.session_state.search_results = results
                st.session_state.last_question = question.strip()

            except Exception as error:
                st.error(f"Search failed: {error}")


if st.session_state.search_results:
    st.subheader("Matching documents")
    st.caption(f"Results for: {st.session_state.last_question}")

    for number, result in enumerate(
        st.session_state.search_results, start=1
    ):
        path = Path(result["file_path"])

        with st.container(border=True):
            st.subheader(f"{number}. {result['filename']}")

            st.caption(
                f"Type: {result['file_type']} · "
                f"Match distance: {result['distance']:.4f}"
            )

            st.write(result["summary"])
            st.caption("Full file path")
            st.code(str(path), language=None)

            col1, col2 = st.columns(2)

            with col1:
                if st.button(
                    "📄 Open file",
                    key=f"open_{number}",
                    use_container_width=True,
                ):
                    if path.is_file():
                        try:
                            os.startfile(str(path))
                        except OSError as error:
                            st.error(f"Could not open file: {error}")
                    else:
                        st.error("This file no longer exists.")

            with col2:
                if st.button(
                    "📂 Show location",
                    key=f"locate_{number}",
                    use_container_width=True,
                ):
                    if path.is_file():
                        try:
                            subprocess.Popen(
                                ["explorer", "/select,", str(path)]
                            )
                        except OSError as error:
                            st.error(f"Could not open Explorer: {error}")
                    else:
                        st.error("This file no longer exists.")

elif not submitted:
    st.info("Enter a question above to search your indexed documents.")
