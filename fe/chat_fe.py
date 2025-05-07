import streamlit as st
import requests
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent))
import config

API_URL = f"http://localhost:{config.PORT_BACKEND}/api/v1/chat"  # Sửa lại endpoint nếu cần

# ====== Trang trí giao diện ======
st.set_page_config(page_title="Crypto Chatbot", page_icon="🪙", layout="centered")

st.markdown(
    """
    <style>
    .stChatBubble {
        border-radius: 18px;
        padding: 12px 18px;
        margin-bottom: 8px;
        max-width: 80%;
        word-break: break-word;
        font-size: 1.05rem;
    }
    .user-bubble {
        background: #e0f7fa;
        margin-left: auto;
        text-align: right;
        border: 1px solid #b2ebf2;
    }
    .bot-bubble {
        background: #f1f8e9;
        margin-right: auto;
        border: 1px solid #c5e1a5;
    }
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 1.5px solid #b2ebf2;
        padding: 8px 12px;
    }
    .stButton > button {
        border-radius: 12px;
        background: #009688;
        color: white;
        font-weight: bold;
        border: none;
        padding: 8px 20px;
    }
    .stButton > button:hover {
        background: #00796b;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# st.image("https://www.bgu.ac.in/wp-content/uploads/2022/07/crypto.jpg", width=200)
st.title("Cryptocurrency Assistant")
st.caption("Trò chuyện với chuyên gia AI về tiền điện tử. Hỏi gì cũng được!")

if "messages" not in st.session_state:
    st.session_state.messages = []

def get_bot_response(user_message):
    try:
        response = requests.post(API_URL, json={"message": user_message})
        if response.status_code == 200:
            return response.json().get("content", "No response")
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"Lỗi kết nối API: {e}"

# ====== Hiển thị lịch sử chat ======
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.markdown(
            f'<div class="stChatBubble user-bubble">🧑‍💻 <b>Bạn:</b><br>{msg["content"]}</div>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            f'<div class="stChatBubble bot-bubble">🤖 <b>Bot:</b><br></div>',
            unsafe_allow_html=True,
        )
        st.markdown(msg["content"], unsafe_allow_html=True)

# ====== Nhập tin nhắn mới ======
col1, col2 = st.columns([5, 1])
with col1:
    user_input = st.text_input(
        "Nhập tin nhắn...",
        key="user_input",
        placeholder="Ví dụ: Dự đoán giá BTC tuần tới?",
        label_visibility="collapsed"
    )
with col2:
    send = st.button("Gửi")

if send and user_input.strip():
    st.session_state.messages.append({"role": "user", "content": user_input})
    bot_reply = get_bot_response(user_input)
    st.session_state.messages.append({"role": "bot", "content": bot_reply})
    st.rerun() 