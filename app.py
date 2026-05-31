import os
import streamlit as st
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI, MistralAIEmbeddings
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.messages import SystemMessage, HumanMessage
from langgraph.graph import StateGraph, END
from typing import TypedDict, List
from langdetect import detect

api_key = st.secrets["MISTRAL_API_KEY"]

st.set_page_config(page_title="Avène Expert", page_icon="💧", layout="centered")
st.title("💧 Avène Product Expert")
st.caption("Posez vos questions en français, anglais ou espagnol")

# Init agent (une seule fois)
@st.cache_resource
def load_agent():
    llm = ChatMistralAI(model="mistral-large-latest", api_key=api_key)
    loader = PyPDFLoader("data/avene_notice.pdf")
    pages = loader.load()
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents(pages)
    embeddings = MistralAIEmbeddings(api_key=api_key)
    vectorstore = Chroma.from_documents(chunks, embeddings)
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

    class AgentState(TypedDict):
        question: str
        context: List[str]
        answer: str

    def retrieve(state: AgentState):
        docs = retriever.invoke(state["question"])
        return {"context": [d.page_content for d in docs]}

    def generate(state: AgentState):
        lang_code = detect(state["question"])
        lang_map = {"en": "English", "fr": "French", "es": "Spanish"}
        target_lang = lang_map.get(lang_code, "French")
        response = llm.invoke([
            SystemMessage(content="Tu es un expert produits Avène / Pierre Fabre."),
            HumanMessage(content=f"Contexte:\n{chr(10).join(state['context'])}\n\nQuestion: {state['question']}")
        ])
        raw_answer = response.content
        if target_lang != "French":
            translation = llm.invoke([
                SystemMessage(content=f"You are a professional translator. Translate to {target_lang}. Output ONLY the translated text."),
                HumanMessage(content=raw_answer)
            ])
            return {"answer": translation.content}
        return {"answer": raw_answer}

    graph = StateGraph(AgentState)
    graph.add_node("retrieve", retrieve)
    graph.add_node("generate", generate)
    graph.set_entry_point("retrieve")
    graph.add_edge("retrieve", "generate")
    graph.add_edge("generate", END)
    return graph.compile()

agent = load_agent()

# Interface chat
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if question := st.chat_input("Posez votre question..."):
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.write(question)
    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            result = agent.invoke({"question": question})
            answer = result["answer"]
            st.write(answer)
    st.session_state.messages.append({"role": "assistant", "content": answer})