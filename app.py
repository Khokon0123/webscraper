import streamlit as st
from scraper import scrape_website
from indexer import index_content
from qa import load_qa_chain

st.set_page_config(page_title="Web RAG", page_icon="🌐", layout="centered")
st.title("🌐 Web Scraper RAG")
st.caption("Paste any URL, scrape it, and ask questions about its content.")
st.divider()

if "scraped" not in st.session_state:
    st.session_state.scraped = False
if "messages" not in st.session_state:
    st.session_state.messages = []
if "current_url" not in st.session_state:
    st.session_state.current_url = ""
if "qa_chain" not in st.session_state:
    st.session_state.qa_chain = None

st.subheader("Step 1 — Enter a URL to scrape")
url = st.text_input("Website URL:", placeholder="https://techcrunch.com")

if st.button("Scrape and Index", type="primary"):
    if not url.strip():
        st.warning("Please enter a URL first!")
    else:
        if not url.startswith("http"):
            url = "https://" + url
        with st.spinner(f"Scraping {url}..."):
            scraped_data = scrape_website(url)
        if "error" in scraped_data:
            st.error(f"Error scraping: {scraped_data['error']}")
        else:
            st.success(f"Scraped {scraped_data['char_count']} characters from {scraped_data['title']}")
            with st.expander("Preview scraped content"):
                st.write(scraped_data["content"][:500] + "...")
            with st.spinner("Indexing content into ChromaDB..."):
                success, result = index_content(scraped_data)
            if success:
                st.success(f"Indexed {result} chunks! Ready to answer questions.")
                st.session_state.scraped = True
                st.session_state.current_url = url
                st.session_state.messages = []
                st.session_state.qa_chain = None
            else:
                st.error(f"Indexing failed: {result}")

st.divider()
st.subheader("Step 2 — Ask questions about the website")

if not st.session_state.scraped:
    st.info("Scrape a website first to start asking questions!")
else:
    st.caption(f"Currently loaded: {st.session_state.current_url}")
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    question = st.chat_input("Ask anything about this website...")
    if question:
        with st.chat_message("user"):
            st.markdown(question)
        st.session_state.messages.append({"role": "user", "content": question})
        if st.session_state.qa_chain is None:
            with st.spinner("Loading knowledge base..."):
                st.session_state.qa_chain = load_qa_chain()
        with st.chat_message("assistant"):
            with st.spinner("Searching website content..."):
                result = st.session_state.qa_chain.invoke({"query": question})
                answer = result["result"]
                sources = [doc.page_content for doc in result["source_documents"]]
            st.markdown(answer)
            with st.expander("Sources from website"):
                for i, source in enumerate(sources):
                    st.caption(f"Chunk {i+1}:")
                    st.code(source[:300])
        st.session_state.messages.append({"role": "assistant", "content": answer})