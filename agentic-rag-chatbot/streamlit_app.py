# import streamlit as st
# from agent_core import run_agent
# from langchain_core.messages import AIMessage, HumanMessage
# import pandas as pd
# import os
# from pymongo import MongoClient
# from dotenv import load_dotenv
#
# # ----------------------------
# # Load .env
# # ----------------------------
# load_dotenv()
# MONGO_URI = os.getenv("MONGO_URI")
# DB_NAME = os.getenv("DB_NAME", "agentic_db")
#
# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# chat_col = db["chats"]
#
# # ----------------------------
# # Streamlit Page Config
# # ----------------------------
# st.set_page_config(page_title="Agentic RAG Chatbot", page_icon="🤖", layout="wide")
#
# # ----------------------------
# # Session State
# # ----------------------------
# if "user_id" not in st.session_state:
#     # Express should pass user_id in query params when redirecting
#     st.session_state.user_id = st.query_params.get("user_id", "guest")
#
# # ----------------------------
# # Helper Functions
# # ----------------------------
# def load_user_history(user_id):
#     record = chat_col.find_one({"user_id": user_id})
#     if record:
#         history = []
#         for m in record["messages"]:
#             cls = AIMessage if m["role"] == "assistant" else HumanMessage
#             history.append(cls(content=m["content"]))
#         return history
#     return [AIMessage(content="Hello! How can I assist you today?")]
#
# def save_user_history(user_id, history):
#     msgs = [
#         {"role": "assistant" if isinstance(m, AIMessage) else "user", "content": m.content}
#         for m in history
#     ]
#     chat_col.update_one({"user_id": user_id}, {"$set": {"messages": msgs}}, upsert=True)
#
# # ----------------------------
# # Chat UI
# # ----------------------------
# st.title("🤖 Agentic RAG Chatbot")
# st.markdown("A research assistant powered by LangChain, RAG, and live web search.")
#
# user_id = st.session_state.user_id
# user_history = load_user_history(user_id)
#
# # Display past messages
# for message in user_history:
#     role = "user" if isinstance(message, HumanMessage) else "assistant"
#     with st.chat_message(role):
#         st.markdown(message.content)
#
# # Chat input
# if user_query := st.chat_input("Ask me anything..."):
#     user_history.append(HumanMessage(content=user_query))
#     with st.chat_message("user"):
#         st.markdown(user_query)
#     with st.chat_message("assistant"):
#         with st.spinner("Thinking..."):
#             try:
#                 agent_response = run_agent(user_query, user_history)
#             except Exception as e:
#                 agent_response = f"⚠️ Error: {e}"
#             st.markdown(agent_response)
#     user_history.append(AIMessage(content=agent_response))
#     save_user_history(user_id, user_history)

# # 2nd most usefull except the dlete chat and logout
# import streamlit as st
# from agent_core import run_agent
# from langchain_core.messages import AIMessage, HumanMessage
# import os, uuid
# from pymongo import MongoClient
# from dotenv import load_dotenv
#
# # ----------------------------
# # Load .env
# # ----------------------------
# load_dotenv()
# MONGO_URI = os.getenv("MONGO_URI")
# DB_NAME = os.getenv("DB_NAME", "agentic_db")
# CHAT_COLLECTION = os.getenv("CHAT_COLLECTION", "chats")
# ADMIN_USER = os.getenv("ADMIN_USER", "admin@example.com")
# ADMIN_PASS = os.getenv("ADMIN_PASS", "admin123")
#
# client = MongoClient(MONGO_URI)
# db = client[DB_NAME]
# chat_col = db[CHAT_COLLECTION]
#
# # ----------------------------
# # Page Config
# # ----------------------------
# st.set_page_config(page_title="Agentic RAG Chatbot", page_icon="🤖", layout="wide")
#
# # ----------------------------
# # Session State Setup
# # ----------------------------
# query_params = st.experimental_get_query_params()
# if "user_id" not in st.session_state:
#     st.session_state.user_id = query_params.get("user_id", [None])[0]
#
# user_id = st.session_state.user_id or "guest"
#
# if "active_chat" not in st.session_state:
#     st.session_state.active_chat = None   # currently selected chat id
# if "history" not in st.session_state:
#     st.session_state.history = []
#
# # ----------------------------
# # Helper Functions
# # ----------------------------
# def load_chats(user_id):
#     record = chat_col.find_one({"user_id": user_id})
#     if record and "chats" in record:
#         return record["chats"]
#     return []
#
# def save_chats(user_id, chats):
#     chat_col.update_one({"user_id": user_id}, {"$set": {"chats": chats}}, upsert=True)
#
# def create_new_chat(user_id):
#     chats = load_chats(user_id)
#     new_chat = {
#         "chat_id": str(uuid.uuid4()),
#         "title": "New Chat",
#         "messages": []
#     }
#     chats.append(new_chat)
#     save_chats(user_id, chats)
#     return new_chat["chat_id"]
#
# def update_chat(user_id, chat_id, history):
#     chats = load_chats(user_id)
#     for chat in chats:
#         if chat["chat_id"] == chat_id:
#             chat["messages"] = [
#                 {"role": "assistant" if isinstance(m, AIMessage) else "user", "content": m.content}
#                 for m in history
#             ]
#             if len(history) > 0 and isinstance(history[0], HumanMessage):
#                 chat["title"] = history[0].content[:30]  # title = first user msg
#     save_chats(user_id, chats)
#
# def get_chat_by_id(user_id, chat_id):
#     chats = load_chats(user_id)
#     for chat in chats:
#         if chat["chat_id"] == chat_id:
#             messages = []
#             for m in chat["messages"]:
#                 cls = AIMessage if m["role"] == "assistant" else HumanMessage
#                 messages.append(cls(content=m["content"]))
#             return messages
#     return []
#
# # ----------------------------
# # Sidebar - Chat List
# # ----------------------------
# st.sidebar.title("📜 Your Chats")
#
# chats = load_chats(user_id)
#
# # Show all chats as buttons
# for chat in chats:
#     if st.sidebar.button(chat["title"], key=chat["chat_id"]):
#         st.session_state.active_chat = chat["chat_id"]
#         st.session_state.history = get_chat_by_id(user_id, chat["chat_id"])
#         st.rerun()
#
# # New chat button
# if st.sidebar.button("➕ New Chat"):
#     new_chat_id = create_new_chat(user_id)
#     st.session_state.active_chat = new_chat_id
#     st.session_state.history = []
#     st.rerun()
#
# # ----------------------------
# # Main Chat UI
# # ----------------------------
# st.title("🤖 Agentic RAG Chatbot")
#
# if st.session_state.active_chat:
#     # Display messages
#     for message in st.session_state.history:
#         role = "user" if isinstance(message, HumanMessage) else "assistant"
#         with st.chat_message(role):
#             st.markdown(message.content)
#
#     # Chat input
#     if user_query := st.chat_input("Ask me anything..."):
#         st.session_state.history.append(HumanMessage(content=user_query))
#         with st.chat_message("user"):
#             st.markdown(user_query)
#
#         with st.chat_message("assistant"):
#             with st.spinner("Thinking..."):
#                 try:
#                     agent_response = run_agent(user_query, st.session_state.history)
#                 except Exception as e:
#                     agent_response = f"⚠️ Error: {e}"
#                 st.markdown(agent_response)
#
#         st.session_state.history.append(AIMessage(content=agent_response))
#         update_chat(user_id, st.session_state.active_chat, st.session_state.history)
#
# else:
#     st.info("Start a new chat from the sidebar ➕")

import streamlit as st
from agent_core import run_agent
from langchain_core.messages import AIMessage, HumanMessage
import os, uuid
from pymongo import MongoClient
from dotenv import load_dotenv

# ----------------------------
# Load .env
# ----------------------------
load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DB_NAME = os.getenv("DB_NAME", "agentic_db")
CHAT_COLLECTION = os.getenv("CHAT_COLLECTION", "chats")
ADMIN_USER = os.getenv("ADMIN_USER", "admin@example.com")
ADMIN_PASS = os.getenv("ADMIN_PASS", "admin123")

client = MongoClient(MONGO_URI)
db = client[DB_NAME]
chat_col = db[CHAT_COLLECTION]

# ----------------------------
# Page Config
# ----------------------------
st.set_page_config(page_title="Agentic RAG Chatbot", page_icon="🤖", layout="wide")

# ----------------------------
# Session State Setup
# ----------------------------
query_params = st.query_params
if "user_id" not in st.session_state:
    st.session_state.user_id = query_params.get("user_id", ["guest"])[0]

user_id = st.session_state.user_id or "guest"

if "active_chat" not in st.session_state:
    st.session_state.active_chat = None   # currently selected chat id
if "history" not in st.session_state:
    st.session_state.history = []

# ----------------------------
# Helper Functions
# ----------------------------
def load_chats(user_id):
    record = chat_col.find_one({"user_id": user_id})
    if record and "chats" in record:
        return record["chats"]
    return []

def save_chats(user_id, chats):
    chat_col.update_one({"user_id": user_id}, {"$set": {"chats": chats}}, upsert=True)

def create_new_chat(user_id):
    chats = load_chats(user_id)
    new_chat = {
        "chat_id": str(uuid.uuid4()),
        "title": "New Chat",
        "messages": []
    }
    chats.append(new_chat)
    save_chats(user_id, chats)
    return new_chat["chat_id"]

def update_chat(user_id, chat_id, history):
    chats = load_chats(user_id)
    for chat in chats:
        if chat["chat_id"] == chat_id:
            chat["messages"] = [
                {"role": "assistant" if isinstance(m, AIMessage) else "user", "content": m.content}
                for m in history
            ]
            if len(history) > 0 and isinstance(history[0], HumanMessage):
                chat["title"] = history[0].content[:30]  # title = first user msg
    save_chats(user_id, chats)

def get_chat_by_id(user_id, chat_id):
    chats = load_chats(user_id)
    for chat in chats:
        if chat["chat_id"] == chat_id:
            messages = []
            for m in chat["messages"]:
                cls = AIMessage if m["role"] == "assistant" else HumanMessage
                messages.append(cls(content=m["content"]))
            return messages
    return []

def delete_chat(user_id, chat_id):
    chats = load_chats(user_id)
    chats = [c for c in chats if c["chat_id"] != chat_id]
    save_chats(user_id, chats)
    if st.session_state.active_chat == chat_id:
        st.session_state.active_chat = None
        st.session_state.history = []

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.query_params.clear()
    st.rerun()

# ----------------------------
# Sidebar - Chat List
# ----------------------------
# Show who is logged in
role_label = "👤 User"
if user_id == "guest":
    role_label = "🌐 Guest"
elif user_id == "admin":
    role_label = "🛠️ Admin"

st.sidebar.markdown(f"**Logged in as:** {role_label}")
st.sidebar.markdown("---")

st.sidebar.title("📜 Your Chats")

chats = load_chats(user_id)

# Show all chats with delete option
for chat in chats:
    col1, col2 = st.sidebar.columns([0.8, 0.2])
    with col1:
        if st.button(chat["title"], key=f"chat-{chat['chat_id']}"):
            st.session_state.active_chat = chat["chat_id"]
            st.session_state.history = get_chat_by_id(user_id, chat["chat_id"])
            st.rerun()
    with col2:
        if st.button("🗑️", key=f"del-{chat['chat_id']}"):
            delete_chat(user_id, chat["chat_id"])
            st.rerun()

# New chat button
if st.sidebar.button("➕ New Chat"):
    new_chat_id = create_new_chat(user_id)
    st.session_state.active_chat = new_chat_id
    st.session_state.history = []
    st.rerun()

# Spacer + Logout pinned bottom
st.sidebar.markdown("---")
st.sidebar.write("")
st.sidebar.markdown(" " * 20)  # push logout to bottom

if user_id == "guest":
    #Redirect to signup( auth forntend )
    login_url = "http://localhost:5173/login"
    st.sidebar.markdown(
        f"[ Sign up / Log in ]({login_url})",
        unsafe_allow_html=True
    )
else:
    if st.sidebar.button("🚪 Logout"):
        logout()


# ----------------------------
# Main Chat UI
# ----------------------------
st.title("🤖 Agentic RAG Chatbot")

if st.session_state.active_chat:
    # Display messages
    for message in st.session_state.history:
        role = "user" if isinstance(message, HumanMessage) else "assistant"
        with st.chat_message(role):
            st.markdown(message.content)

    # Chat input
    if user_query := st.chat_input("Ask me anything..."):
        st.session_state.history.append(HumanMessage(content=user_query))
        with st.chat_message("user"):
            st.markdown(user_query)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    agent_response = run_agent(user_query, st.session_state.history)
                except Exception as e:
                    agent_response = f"⚠️ Error: {e}"
                st.markdown(agent_response)

        st.session_state.history.append(AIMessage(content=agent_response))
        update_chat(user_id, st.session_state.active_chat, st.session_state.history)

else:
    st.info("Start a new chat from the sidebar ➕")
