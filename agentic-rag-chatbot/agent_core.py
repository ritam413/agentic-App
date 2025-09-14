# agent_core.py
import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain.agents import create_tool_calling_agent, AgentExecutor
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain.tools import Tool

load_dotenv()

# Check keys
print(f"Tavily API Key: {os.getenv('TAVILY_API_KEY')}")
print(f"Google API Key: {os.getenv('GOOGLE_API_KEY')}")
# Load API keys safely
os.environ["TAVILY_API_KEY"] = os.getenv("TAVILY_API_KEY", "")
os.environ["GOOGLE_API_KEY"] = os.getenv("GOOGLE_API_KEY", "")

# Create the web search tool
tavily_search = TavilySearchResults(max_results=3)

# Load the FAISS index and create a RAG tool
embedding_model = HuggingFaceEmbeddings()
vector_store = FAISS.load_local("faiss_index", embedding_model, allow_dangerous_deserialization=True)
rag_retriever = vector_store.as_retriever()

# Define the RAG chain for internal knowledge base
rag_template = ChatPromptTemplate.from_template(
    """
    Use the following context to answer the user's question.
    If the context does not provide enough info, say you don't know.

    Context:
    {context}

    Question: {input}
    """
)
document_chain = create_stuff_documents_chain(
    ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0),
    rag_template
)
retrieval_chain = create_retrieval_chain(rag_retriever, document_chain)

# Define tools
tools = [
    Tool(
        name="WebSearch",
        func=tavily_search.run,
        description="Useful for searching recent or external information from the web"
    ),
    Tool(
        name="KnowledgeBase",
        func=retrieval_chain.invoke,
        description="Useful for answering questions from internal documents"
    )
]

# Define the agent's prompt
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an AI assistant. Use the available tools to answer questions."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("user", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Initialize the LLM
llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0)

# Create the agent
agent = create_tool_calling_agent(llm, tools, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)

def run_agent(query, chat_history):
    """
    Executes the LangChain agent with a user query and chat history.
    """
    response = agent_executor.invoke({"input": query, "chat_history": chat_history})
    return response["output"]
