import streamlit as st
import json
from langchain_ollama import ChatOllama

st.title("🥗 RAG Chatbot")

# تحميل البيانات
with open("healthy_data.json", "r", encoding="utf-8") as f:
    data = json.load(f)

llm = ChatOllama(model="llama3.2:3b")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).markdown(msg["content"])

if prompt := st.chat_input("الغذاء الصحي؟"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").markdown(prompt)
    
    with st.chat_message("assistant"):
        context = "\n".join(data[-5:])  # آخر 5 chunks
        response = llm.invoke(f"{context}\nسؤال: {prompt}").content
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})