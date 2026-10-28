import os
import shutil
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_ollama import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_core.documents import Document

def index_content(scraped_data):
    if "error" in scraped_data:
        return False, scraped_data["error"]
    if not scraped_data["content"]:
        return False, "No content found on this page"
    if os.path.exists("./chroma_db"):
        shutil.rmtree("./chroma_db")
        print("Cleared old database")
    doc = Document(
        page_content=scraped_data["content"],
        metadata={"source": scraped_data["url"], "title": scraped_data["title"]}
    )
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    chunks = splitter.split_documents([doc])
    print(f"Created {len(chunks)} chunks from website content")
    embedding_model = OllamaEmbeddings(model="llama3.2")
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embedding_model,
        persist_directory="./chroma_db"
    )
    print(f"Indexed {len(chunks)} chunks successfully")
    return True, len(chunks)