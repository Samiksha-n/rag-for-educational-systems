"""
RAG for Educational Systems
------------------------------
Frontend built with Streamlit (Python only).

Covers:
  - Task 1 (Week 4): Implement Client-Server Communication
  - Task 5 (Week 4): Build Conversation History Feature

Run with:
    pip install streamlit requests
    streamlit run frontend.py
"""

import streamlit as st
import requests
from datetime import datetime

st.set_page_config(
    page_title="RAG - Educational AI System",
    page_icon="🎓",
    layout="centered"
)

BACKEND_URL = "http://localhost:5000"

if "history" not in st.session_state:
    st.session_state.history = []

def send_prompt(prompt: str):
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json={"prompt": prompt},
            timeout=10
        )
        if response.status_code == 200:
            return response.json().get("response", "No response from server.")
        else:
            return f"Error {response.status_code}: {response.text}"
    except requests.exceptions.ConnectionError:
        return "❌ Cannot connect to backend. Make sure Flask (app.py) is running on port 5000."
    except Exception as e:
        return f"❌ Unexpected error: {str(e)}"

st.title("🎓 RAG Educational AI System")
st.markdown("Ask any educational question and get an AI-powered answer.")
st.divider()

st.subheader("💬 Ask a Question")
user_input = st.text_area(
    label="Type your question here:",
    placeholder="e.g. What is Retrieval Augmented Generation?",
    height=120
)

if st.button("🚀 Submit", use_container_width=True):
    if user_input.strip() == "":
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("⏳ Getting answer from AI..."):
            answer = send_prompt(user_input)

        st.session_state.history.append({
            "question": user_input,
            "answer": answer,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })

        st.success("✅ Response received!")
        st.markdown("### 🤖 AI Response")
        st.info(answer)

st.divider()

st.subheader("📜 Conversation History")

if len(st.session_state.history) == 0:
    st.caption("No conversations yet. Ask a question above to get started!")
else:
    for i, entry in enumerate(reversed(st.session_state.history)):
        with st.expander(f"Q{len(st.session_state.history) - i}: {entry['question'][:60]}...  |  🕐 {entry['timestamp']}"):
            st.markdown(f"**❓ Question:** {entry['question']}")
            st.markdown(f"**🤖 Answer:** {entry['answer']}")

    if st.button("🗑️ Clear History", use_container_width=True):
        st.session_state.history = []
        st.rerun()
