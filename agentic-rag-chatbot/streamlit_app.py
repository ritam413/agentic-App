import streamlit as st
from agent_core import run_agent
from langchain_core.messages import AIMessage, HumanMessage
import pandas as pd
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# ----------------------------
# Load .env
# ----------------------------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "agentic_db")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
users_col = db["users"]
chat_col = db["chats"]

# ----------------------------
# Admin Config
# ----------------------------
ADMIN_ID = "admin"
ADMIN_PASS = "admin123"

# ----------------------------
# Streamlit Page Config
# ----------------------------
st.set_page_config(page_title="Agentic RAG Chatbot", page_icon="🤖", layout="wide")

# ----------------------------
# Session State
# ----------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False
if "is_admin" not in st.session_state:
    st.session_state.is_admin = False
if "user_id" not in st.session_state:
    st.session_state.user_id = None
if "page_mode" not in st.session_state:
    st.session_state.page_mode = "login"  # can be 'login' or 'signup'

# ----------------------------
# Helper Functions
# ----------------------------
def load_user_history(user_id):
    record = chat_col.find_one({"user_id": user_id})
    if record:
        history = []
        for m in record["messages"]:
            cls = AIMessage if m["role"]=="assistant" else HumanMessage
            history.append(cls(content=m["content"]))
        return history
    return [AIMessage(content="Hello! How can I assist you today?")]

def save_user_history(user_id, history):
    msgs = [{"role":"assistant" if isinstance(m, AIMessage) else "user", "content": m.content} for m in history]
    chat_col.update_one({"user_id": user_id}, {"$set":{"messages": msgs}}, upsert=True)

# ----------------------------
# Sidebar Logout
# ----------------------------
st.sidebar.title("Agentic RAG Chatbot")
if st.session_state.logged_in:
    st.sidebar.markdown(f"**Logged in as:** {st.session_state.user_id}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.session_state.is_admin = False
        st.session_state.user_id = None
        st.session_state.page_mode = "login"

# ----------------------------
# Custom CSS for Login/Signup
# ----------------------------
page_bg = """
<style>
/* Background */
.stApp {
    background: linear-gradient(135deg, #4e1b8e, #7b3cbb, #a56edc);
    background-size: cover;
    background-attachment: fixed;
    color: white;
}

/* Center container */
.main {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh; /* full height */
}

/* Card for login/signup */
.login-card {
    background: rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: 2rem 2.5rem;
    width: 350px;
    backdrop-filter: blur(12px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.25);
    color: white;
    text-align: center;
}

/* Title */
.login-card h2 {
    font-weight: bold;
    margin-bottom: 1.5rem;
    color: white;
}

/* Input boxes */
.stTextInput > div > div > input {
    border-radius: 12px;
    padding: 10px;
    border: none;
    outline: none;
    background: rgba(255,255,255,0.9);
    color: black;
}

/* Buttons */
.stButton button {
    width: 100%;
    padding: 10px;
    border-radius: 12px;
    border: none;
    background: white;
    color: #6a0dad;
    font-weight: bold;
    cursor: pointer;
    margin-top: 1rem;
}
.stButton button:hover {
    background: #f0e6ff;
}

/* Links */
a {
    color: #fff;
    font-weight: bold;
    text-decoration: none;
}
a:hover {
    text-decoration: underline;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)




# ----------------------------
# Login / Signup UI
# ----------------------------
if not st.session_state.logged_in:
    st.title("🤖 Welcome to Agentic Chatbot")

    if st.session_state.page_mode == "login":
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2>Login</h2>", unsafe_allow_html=True)

        user_id = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if user_id == ADMIN_ID and password == ADMIN_PASS:
                st.session_state.logged_in = True
                st.session_state.is_admin = True
                st.session_state.user_id = ADMIN_ID
            else:
                user = users_col.find_one({"user_id": user_id, "password": password})
                if user:
                    st.session_state.logged_in = True
                    st.session_state.is_admin = user.get("is_admin", False)
                    st.session_state.user_id = user_id
                else:
                    st.error("Invalid credentials")

        st.markdown('<p>Don\'t have an account? <a href="#">Register</a></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)


    elif st.session_state.page_mode == "signup":
        st.markdown('<div class="login-box">', unsafe_allow_html=True)
        st.markdown("<h2>Sign Up</h2>", unsafe_allow_html=True)
        new_user = st.text_input("Choose Username")
        new_pass = st.text_input("Choose Password", type="password")

        if st.button("Sign Up"):
            if users_col.find_one({"user_id": new_user}) or new_user == ADMIN_ID:
                st.error("User already exists!")
            else:
                users_col.insert_one({"user_id": new_user, "password": new_pass, "is_admin": False})
                st.success("Account created! You can login now.")
                st.session_state.page_mode = "login"

        st.markdown('<p>Already have an account? <a href="#">Login</a></p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        if st.button("Go to Login"):
            st.session_state.page_mode = "login"

# ----------------------------
# After Login: Page Selection
# ----------------------------
if st.session_state.logged_in:
    if st.session_state.is_admin:
        page = st.sidebar.radio("Navigation", ["Admin Dashboard", "User Chat"])
    else:
        page = "User Chat"

# ----------------------------
# User Chat Page
# ----------------------------
if st.session_state.logged_in and page == "User Chat":
    st.title("🤖 Agentic RAG Chatbot")
    st.markdown("A research assistant powered by LangChain, RAG, and live web search.")
    user_history = load_user_history(st.session_state.user_id)

    # Display past messages
    for message in user_history:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

    # Chat input
    if user_query := st.chat_input("Ask me anything..."):
        user_history.append(HumanMessage(content=user_query))
        with st.chat_message("user"):
            st.markdown(user_query)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    agent_response = run_agent(user_query, user_history)
                except Exception as e:
                    agent_response = f"⚠️ Error: {e}"
                st.markdown(agent_response)
        user_history.append(AIMessage(content=agent_response))
        save_user_history(st.session_state.user_id, user_history)

# ----------------------------
# Admin Dashboard
# ----------------------------
if st.session_state.logged_in and st.session_state.is_admin and page == "Admin Dashboard":
    st.title("🛠 Admin Dashboard")
    st.markdown("Monitor all user chats and manage the system.")
    users = list(users_col.find({}, {"_id":0, "user_id":1}))
    total_users = len(users)
    total_messages = sum(len(load_user_history(u["user_id"])) for u in users)
    st.metric("Total Users", total_users)
    st.metric("Total Messages", total_messages)

    st.subheader("User Chat Histories")
    for u in users:
        user = u["user_id"]
        history = load_user_history(user)
        with st.expander(f"{user} ({len(history)} messages)"):
            df = pd.DataFrame(
                [(type(m).__name__, m.content) for m in history],
                columns=["Role", "Message"]
            )
            st.dataframe(df, use_container_width=True)
            if st.button(f"Clear {user} History"):
                chat_col.delete_one({"user_id": user})
                st.success(f"Chat history for {user} cleared.")

