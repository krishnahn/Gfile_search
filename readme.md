# Google File Search RAG System

A production-ready RAG (Retrieval Augmented Generation) system built with Google's official File Search API. No vector databases or embedding infrastructure required.

## ✨ Features

- **🔍 Native Semantic Search** - Leverages Google's File Search API for intelligent document indexing and retrieval
- **🌐 Multi-Language Support** - Responds in the same language as the query (English, Tamil, Hindi, Malayalam, etc.)
- **📄 Multi-Format Support** - PDF, TXT, DOCX, HTML, Markdown files
- **🤖 Gemini Integration** - Uses Gemini 2.5 Flash for fast, accurate responses
- **📚 Built-in Citations** - Automatic source attribution with grounding metadata
- **⚡ Zero Infrastructure** - No vector databases or custom embedding models needed

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Key

Get your API key from [Google AI Studio](https://aistudio.google.com/apikey)

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your API key
GEMINI_API_KEY=your_api_key_here
```

### 3. Create a Document Store

```bash
python main.py create-store my-docs
```

### 4. Upload Documents

```bash
# Upload a single file
python main.py upload document.pdf my-docs

# Upload all files in a directory
python main.py upload-dir ./documents my-docs
```

### 5. Start Querying

```bash
# Interactive mode (recommended)
python main.py interactive my-docs

# Single query
python main.py search "What is the main topic?" my-docs
```

---

## 📖 CLI Commands

| Command | Description | Example |
|---------|-------------|---------|
| `create-store <name>` | Create a new document store | `python main.py create-store my-docs` |
| `list-stores` | List all available stores | `python main.py list-stores` |
| `delete-store <name>` | Delete a store | `python main.py delete-store my-docs` |
| `upload <file> <store>` | Upload a single file | `python main.py upload report.pdf my-docs` |
| `upload-dir <dir> <store>` | Upload all files in directory | `python main.py upload-dir ./docs my-docs` |
| `search "<query>" <store>` | Search and get AI response | `python main.py search "summary" my-docs` |
| `ask "<question>" <store>` | Ask a direct question | `python main.py ask "What is X?" my-docs` |
| `summarize <store>` | Generate document summary | `python main.py summarize my-docs` |
| `interactive <store>` | Start interactive Q&A session | `python main.py interactive my-docs` |

### Interactive Mode Commands

Once in interactive mode, you can use:
- **Any question** - Get AI-powered answers from your documents
- `summarize` - Generate summary of all documents
- `summarize <topic>` - Generate focused summary on a topic
- `stores` - List all available stores
- `switch <store>` - Switch to a different store
- `help` - Show available commands
- `quit` - Exit interactive mode

---

## 💻 Python API Usage

### Basic Usage

```python
from src.file_search_client import FileSearchClient
from src.search_manager import SearchManager

# Initialize clients
client = FileSearchClient()
search_manager = SearchManager(client)

# Create a store and upload documents
store_id = client.create_store("my-documents")
client.upload_document("document.pdf", store_id)

# Search and get AI-generated response
response = search_manager.search_and_generate(
    query="What is the main topic of this document?",
    store_name=store_id
)

print(response.answer)
```

### Advanced Search Options

```python
# Multi-store search
response = search_manager.search_multiple_stores(
    query="Find relevant information",
    store_names=["store1", "store2"]
)

# Batch queries with rate limiting
queries = ["Question 1", "Question 2", "Question 3"]
responses = search_manager.batch_search(
    queries=queries,
    store_name=store_id,
    delay_seconds=1.0
)

# Document summarization
summary = search_manager.summarize_documents(
    store_name=store_id,
    focus_topic="key findings"  # Optional focus
)
```

### Document Processing

```python
from src.document_processor import DocumentProcessor

processor = DocumentProcessor(client)

# Validate file before upload
is_valid, error = processor.validate_file("document.pdf")

# Upload with custom chunking
processor.upload_document(
    file_path="large_document.pdf",
    store_name=store_id,
    use_custom_chunking=True
)

# Upload entire directory
operations = processor.upload_directory(
    directory_path="./documents",
    store_name=store_id,
    recursive=True
)
```

---

## 📁 Project Structure

```
google-file-search/
├── main.py                      # CLI entry point
├── requirements.txt             # Python dependencies
├── .env.example                 # Environment template
├── setup.sh                     # Linux/Mac setup script
│
├── src/                         # Core modules
│   ├── file_search_client.py    # Google File Search API wrapper
│   ├── search_manager.py        # Search & generation logic
│   ├── document_processor.py    # Document upload & validation
│   └── response_handler.py      # Response formatting & citations
│
├── config/                      # Configuration
│   ├── settings.py              # App settings & environment
│   └── prompts.py               # System prompts for RAG
│
├── examples/                    # Usage examples
│   ├── basic_rag.py             # Basic RAG example
│   └── advanced_search.py       # Advanced features demo
│
└── data/                        # Data storage
    ├── stores.json              # Store metadata
    └── documents/               # Local document cache
```

---

## ⚙️ Configuration

### Environment Variables

Create a `.env` file with the following:

```env
# Required
GEMINI_API_KEY=your_api_key_here

# Optional (with defaults)
DEFAULT_MODEL=gemini-2.5-flash
DEFAULT_STORE_NAME=rag-documents
MAX_TOKENS_PER_CHUNK=500
MAX_OVERLAP_TOKENS=50
MAX_FILE_SIZE_MB=100
```

### Supported File Formats

| Format | Extension | Max Size | Notes |
|--------|-----------|----------|-------|
| PDF | `.pdf` | 100 MB | Max 1000 pages |
| Text | `.txt` | 100 MB | Plain text |
| Word | `.docx` | 100 MB | Microsoft Word |
| HTML | `.html`, `.htm` | 100 MB | Web pages |
| Markdown | `.md` | 100 MB | Markdown files |
| CSV | `.csv` | 100 MB | Data files |
| JSON | `.json` | 100 MB | Structured data |

---

## 🔒 API Limits

| Resource | Free Tier Limit |
|----------|-----------------|
| Storage | 1 GB total |
| File Size | 100 MB per file |
| PDF Pages | 1000 pages max |
| Stores | Unlimited |

---

## 🛠️ Troubleshooting

### Common Issues

**API Key Error**
```
GEMINI_API_KEY is required
```
→ Make sure your `.env` file has a valid API key from [Google AI Studio](https://aistudio.google.com/apikey)

**Store Not Found**
```
Store 'my-docs' not found
```
→ Run `python main.py list-stores` to see available stores, or create one with `create-store`

**File Upload Failed**
```
File type not supported
```
→ Only PDF, TXT, DOCX, HTML, MD, CSV, JSON files are supported

---

## 📝 Examples

### Example 1: Document Q&A

```bash
# Upload a research paper
python main.py upload research_paper.pdf my-docs

# Ask questions
python main.py ask "What are the main findings?" my-docs
python main.py ask "What methodology was used?" my-docs
```

### Example 2: Multi-Language Queries

The system automatically responds in the query language:

```bash
# English query → English response
python main.py search "How many colleges?" my-docs

# Tamil query → Tamil response  
python main.py search "எத்தனை கல்லூரிகள்?" my-docs

# Hindi query → Hindi response
python main.py search "कितने कॉलेज हैं?" my-docs
```

### Example 3: Batch Processing

```python
from src.file_search_client import FileSearchClient
from src.search_manager import SearchManager

client = FileSearchClient()
manager = SearchManager(client)

questions = [
    "What is the introduction about?",
    "What are the key conclusions?",
    "Who are the authors?"
]

responses = manager.batch_search(
    queries=questions,
    store_name="my-docs"
)

for q, r in zip(questions, responses):
    print(f"Q: {q}")
    print(f"A: {r.answer}\n")
```

---

## 📄 License

MIT License

---

## 🔗 Resources

- [Google AI Studio](https://aistudio.google.com/) - Get API keys
- [Gemini API Documentation](https://ai.google.dev/docs) - Official docs
- [File Search API Reference](https://ai.google.dev/api/files) - API reference