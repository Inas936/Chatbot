import streamlit as st
import json
import os
from langchain_ollama import ChatOllama

os.environ["OLLAMA_BASE_URL"] = "http://localhost:11434"

st.set_page_config(layout="wide", page_title="RAG Nutrition Chatbot", page_icon="🥗")

# Custom CSS للواجهة الجميلة
st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
    }
    
    .stApp, .stApp p, .stApp h1, .stApp h2, .stApp h3, 
    .stApp h4, .stApp h5, .stApp h6, .stApp label, 
    .stApp span, .stMarkdown {
        color: #1a1a2e !important;
    }
    
    [data-testid="stChatMessage"] {
        background: rgba(255,255,255,0.95) !important;
        border-radius: 20px !important;
        padding: 15px !important;
        margin: 10px 0 !important;
        box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    }
    
    [data-testid="stChatMessage"][data-testid="user"] {
        background: linear-gradient(135deg, #00b4db, #0083b0) !important;
    }
    
    [data-testid="stChatMessage"][data-testid="user"] p {
        color: white !important;
    }
    
    [data-testid="stChatMessage"][data-testid="assistant"] {
        background: white !important;
        border-left: 4px solid #00b894 !important;
    }
    
    .stChatInput textarea {
        background: white !important;
        color: #1a1a2e !important;
        border-radius: 25px !important;
        border: 2px solid #00b894 !important;
    }
    
    h1 {
        text-align: center !important;
        color: #00b894 !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("🥗 RAG Chatbot - Nutrition Assistant")

# فقرة تعريفية
st.markdown("""
<div style="background: white; padding: 20px; border-radius: 15px; margin: 10px 0; border-left: 5px solid #00b894;">
    <h3>🤖 Welcome to Nutrition Assistant Chatbot</h3>
    <p>This chatbot uses <strong>RAG (Retrieval-Augmented Generation)</strong> technology to answer your questions about healthy nutrition.</p>
    <p><strong>How can I help you?</strong><br>
    • Answer questions about healthy eating and balanced diets<br>
    • Provide information about food benefits and nutrition<br>
    • Based on scientific references about nutrition</p>
</div>
""", unsafe_allow_html=True)

# تحميل البيانات
try:
    with open("healthy_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)
    st.success(f"✅ Loaded {len(data)} knowledge chunks")
except FileNotFoundError:
    st.error("❌ File 'healthy_data.json' not found!")
    st.info("Please make sure the file exists in the same directory")
    st.stop()

# استخدام نموذج أسرع
llm = ChatOllama(
    model="llama3.2:1b",  # أسرع من 3b
    temperature=0.1,
    num_predict=150
)

# الدردشة
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "👋 Hello! Ask me anything about healthy nutrition 🥗"}
    ]

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Ask about healthy nutrition..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    
    with st.chat_message("assistant"):
        with st.spinner("🔍 Searching knowledge base..."):
            # استخدام أول 10 chunks أو آخر 10 للحصول على سياق أفضل
            context = "\n".join(data[:10])  # أول 10 chunks
            
            response = llm.invoke(
                f"""You are a nutrition expert. Use the following information to answer:

Context from knowledge base:
{context}

Question: {prompt}

Answer helpfully (3-4 sentences):"""
            ).content
            
        st.markdown(response)
        st.session_state.messages.append({"role": "assistant", "content": response})

# شريط جانبي
with st.sidebar:
    st.markdown("### 📊 Information")
    st.metric("📚 Knowledge Chunks", len(data))
    st.metric("🧠 Model", "llama3.2:1b")
    st.markdown("---")
    st.markdown("### 💡 Suggested Questions")
    st.markdown("- What are the benefits of healthy eating?")
    st.markdown("- How to plan a balanced meal?")
    st.markdown("- ما هي فوائد الأكل الصحي؟")
    st.markdown("---")
    st.caption("🎓 Graduation Project - RAG Pipeline")
