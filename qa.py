from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain_community.vectorstores import Chroma
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser
import os

def load_qa_chain():
    if not os.path.exists("./chroma_db"):
        return None
    embedding_model = OllamaEmbeddings(model="llama3.2")
    vectorstore = Chroma(
        persist_directory="./chroma_db",
        embedding_function=embedding_model
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 3})
    prompt = PromptTemplate.from_template("""You are a helpful assistant that answers questions based only on the website content below.
If the answer is not in the content say "I don't have that information from this website."

Context:
{context}

Question: {question}

Answer:""")
    llm = OllamaLLM(model="llama3.2")
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)
    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    return chain, retriever
