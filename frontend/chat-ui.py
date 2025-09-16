import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="Document Chatbot", layout="wide")

st.title("📄 Document Chatbot")

# Sidebar: Upload documents
st.sidebar.header("Upload Document")

from PyPDF2 import PdfReader   # at the top of the file

def extract_text_from_pdf(pdf_file):
    reader = PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        page_text = page.extract_text()
        if page_text:
            text += page_text
    return text

uploaded_file = st.file_uploader("Upload PDF/TXT")
if uploaded_file is not None:
    file_bytes = uploaded_file.read()
    with open("temp.pdf", "wb") as f:
        f.write(file_bytes)
    st.success("Uploaded file saved")


# Chat UI
if "messages" not in st.session_state:
    st.session_state.messages = []

st.subheader("💬 Chat with your document")

# Display conversation
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# User input
if prompt := st.chat_input("Ask a question about the document..."):
    # Save user message
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Call backend
    try:
        response = requests.post(
            f"{API_URL}/ask",
            json={"query": prompt}   # 👈 send JSON, not form-data
        )
        if response.status_code == 200:
            answer = response.json().get("answer", "⚠️ No answer returned")
        else:
            answer = f"Error {response.status_code}: {response.text}"
    except Exception as e:
        answer = f"⚠️ Request failed: {e}"

    # Save and display assistant response
    st.session_state.messages.append({"role": "assistant", "content": answer})
    with st.chat_message("assistant"):
        st.markdown(answer)
