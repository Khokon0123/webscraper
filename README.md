# Web Scraper RAG

Paste any website URL, scrape its content, and ask questions about it. Built with a Retrieval-Augmented Generation (RAG) pipeline that runs entirely on your own machine using a local LLaMA model, so there are no API costs and no data leaves your computer.

## What it does

1. You enter a URL in the Streamlit app.
2. The scraper downloads the page and extracts the main text (paragraphs, with scripts, navigation, and footers removed).
3. The text is split into chunks, converted into embeddings, and stored in a ChromaDB vector database.
4. You ask questions in a chat interface. The app retrieves the most relevant chunks and LLaMA answers using only that content.
5. Every answer shows the source chunks it came from.

Scraping a new URL replaces the previous knowledge base, so answers always reflect the page you loaded most recently.

## How it works

```
URL -> scrape (BeautifulSoup) -> chunk (500 chars, 50 overlap)
    -> embed (Ollama llama3.2) -> store (ChromaDB)

Question -> embed -> retrieve top 3 chunks -> LLaMA 3.2 -> answer + sources
```

## Tech stack

| Component | Tool |
|---|---|
| Web scraping | requests, BeautifulSoup4 |
| Orchestration | LangChain (core, community, text-splitters) |
| Vector database | ChromaDB |
| LLM and embeddings | LLaMA 3.2 via Ollama |
| Interface | Streamlit |

## Project structure

```
web-scraper-rag/
├── app.py        # Streamlit UI: URL input and chat
├── scraper.py    # Fetches a page and extracts clean text
├── indexer.py    # Chunks text, creates embeddings, stores in ChromaDB
├── qa.py         # Builds the retrieval and answer chain
└── README.md
```

## Setup

Requires macOS or Linux, Python 3.11, and [Homebrew](https://brew.sh) (for Ollama on Mac).

### 1. Install and start Ollama

```bash
brew install ollama
brew services start ollama
ollama pull llama3.2
```

### 2. Create a virtual environment

```bash
python3.11 -m venv env
source env/bin/activate
```

### 3. Install dependencies

```bash
pip install langchain langchain-community langchain-text-splitters chromadb langchain-ollama beautifulsoup4 requests streamlit
```

### 4. Run the app

```bash
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Usage

1. Paste a URL (for example `https://news.ycombinator.com`) and click **Scrape and Index**.
2. Wait for indexing to finish. Larger pages take longer because each chunk is embedded locally.
3. Ask questions such as "What are the top stories?" or "What is being discussed about AI?"
4. Expand **Sources from website** under any answer to see the chunks it used.

## Limitations

- Pages that load their content with JavaScript may return little or no text, since the scraper reads static HTML only.
- Some sites block automated requests.
- Only one page is indexed at a time.
- Answer quality depends on the local model. LLaMA 3.2 is small, so complex questions may get imperfect answers.

## Possible improvements

- Scheduled daily scraping of a saved list of URLs (for example with the `schedule` library or a cron job)
- Crawling multiple pages or following links
- Indexing several sites at once with per-source filtering
- Handling JavaScript-rendered pages with a headless browser

## Skills demonstrated

Web scraping, text chunking, vector embeddings and semantic search, retrieval-augmented generation, running local LLMs, and building an interactive Streamlit application.
