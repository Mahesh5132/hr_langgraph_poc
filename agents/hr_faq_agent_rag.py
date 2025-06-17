# --- hr_langgraph_poc/agents/hr_faq_agent_rag.py ---
import pandas as pd
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain.vectorstores import Chroma
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from langchain.docstore.document import Document
from langchain.text_splitter import CharacterTextSplitter
import os

# Load FAQ CSV
def load_faq_documents():
    df = pd.read_csv("data/faq.csv")
    docs = [Document(page_content=row["answer"], metadata={"question": row["question"]}) for _, row in df.iterrows()]
    return docs

# Create or load Vector DB
def get_vectorstore():
    if not os.path.exists("vectorstore/chroma"):
        docs = load_faq_documents()
        splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=0)
        texts = splitter.split_documents(docs)

        vectorstore = Chroma.from_documents(
            documents=texts,
            embedding=OpenAIEmbeddings(),
            persist_directory="vectorstore/chroma"
        )
        vectorstore.persist()
    else:
        vectorstore = Chroma(
            persist_directory="vectorstore/chroma",
            embedding_function=OpenAIEmbeddings()
        )
    return vectorstore

# Build QA chain
retriever = get_vectorstore().as_retriever()
qa_chain = RetrievalQA.from_chain_type(
    llm=ChatOpenAI(temperature=0),
    chain_type="stuff",
    retriever=retriever,
    return_source_documents=True
)

# LangGraph-compatible node
def hr_faq_agent_rag_node(state):
    query = state.get("query")
    result = qa_chain({"query": query})
    answer = result["result"]
    return {"response": f"✅ Answer: {answer}"}
