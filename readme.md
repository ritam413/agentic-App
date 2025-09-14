# 🤖 Agentic RAG Chatbot  

A research assistant powered by **LangChain, RAG, and live web search**.  
This project demonstrates how to build an **agentic AI chatbot** with a local knowledge base (RAG) and external web search, wrapped in a **Streamlit UI**.  

---

## 📂 Project Setup  

### 1. Create a Project Directory  
```bash
mkdir agentic-rag-chatbot && cd agentic-rag-chatbot
2. Create a Virtual Environment
bash
Copy code
python -m venv venv
Activate the environment:

macOS/Linux:

bash
Copy code
source venv/bin/activate
Windows:

bash
Copy code
venv\Scripts\activate
3. Install Dependencies
bash
Copy code
pip install langchain langchain-openai langchain-community streamlit faiss-cpu sentence-transformers tavily-python
This installs:

LangChain – Agentic framework

LangChain-OpenAI – LLM integration

LangChain-Community – Tools support

Streamlit – Chat UI

FAISS + Sentence-Transformers – Local RAG pipeline

Tavily-Python – Web search tool

4. Create requirements.txt
bash
Copy code
pip freeze > requirements.txt
📚 Preparing the Knowledge Base (RAG)
1. Create a Data Folder
bash
Copy code
mkdir data
2. Add Knowledge File
Create data/knowledge.txt containing your custom knowledge base (e.g., company policies, hackathon rules, domain-specific info).

3. Build the Vector Store
Create rag_setup.py:

python
Copy code
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def create_faiss_index(file_path, index_path="faiss_index"):
    loader = TextLoader(file_path)
    documents = loader.load()

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
    docs = text_splitter.split_documents(documents)

    embedding_model = HuggingFaceEmbeddings()
    vector_store = FAISS.from_documents(docs, embedding_model)
    vector_store.save_local(index_path)

    print(f"FAISS index created and saved at {index_path}")

if __name__ == "__main__":
    create_faiss_index("data/knowledge.txt")
Run once to generate the FAISS index:

bash
Copy code
python rag_setup.py
🧠 Building the Agent's Core
Create agent_core.py:

python
Copy code
import os
from langchain_openai import ChatOpenAI
from langchain_community.tools.tavily_search import TavilySearch
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

# Load API keys (ensure you set these in your environment)
# Example: export OPENAI_API_KEY="your-key"
# Example: export TAVILY_API_KEY="your-key"

tavily_search = TavilySearch(max_results=3)

embedding_model = HuggingFaceEmbeddings()
vector_store = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)
rag_retriever = vector_store.as_retriever()

rag_template = ChatPromptTemplate.from_template(
    """
    Answer the user's question based on the provided context:
    {context}
    
    Question: {input}
    """
)

document_chain = create_stuff_documents_chain(ChatOpenAI(model="gpt-4o-mini"), rag_template)
retrieval_chain = create_retrieval_chain(rag_retriever, document_chain)

# Define tools
tools = [
    tavily_search,
    retrieval_chain
]

# Define prompt
prompt = ChatPromptTemplate.from_messages([
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}")
])

llm = ChatOpenAI(model="gpt-4o-mini", temperature=0)

agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def run_agent(query, chat_history):
    response = agent_executor.invoke({"input": query, "chat_history": chat_history})
    return response["output"]
💬 Building the Streamlit UI
Create streamlit_app.py:

python
Copy code
import streamlit as st
from agent_core import run_agent
from langchain_core.messages import AIMessage, HumanMessage

st.set_page_config(page_title="Agentic RAG Chatbot", page_icon="🤖")

st.title("🤖 Agentic RAG Chatbot")
st.markdown("A research assistant powered by LangChain, RAG, and live web search.")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = [AIMessage(content="Hello! How can I assist you today?")]

for message in st.session_state.chat_history:
    if isinstance(message, HumanMessage):
        with st.chat_message("user"):
            st.markdown(message.content)
    else:
        with st.chat_message("assistant"):
            st.markdown(message.content)

if user_query := st.chat_input("Ask me anything..."):
    st.session_state.chat_history.append(HumanMessage(content=user_query))
    with st.chat_message("user"):
        st.markdown(user_query)

    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            agent_response = run_agent(user_query, st.session_state.chat_history)
            st.markdown(agent_response)
            st.session_state.chat_history.append(AIMessage(content=agent_response))
Run locally:

bash
Copy code
streamlit run streamlit_app.py