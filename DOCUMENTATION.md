# AI QA Genesis - Complete Project Documentation

## 📋 Table of Contents
1. [Project Overview](#project-overview)
2. [Architecture](#architecture)
3. [Directory Structure](#directory-structure)
4. [Core Components](#core-components)
5. [Data Flow](#data-flow)
6. [API Endpoints](#api-endpoints)
7. [Deployment Architecture](#deployment-architecture)
8. [Technology Stack](#technology-stack)

---

## 🎯 Project Overview

**AI QA Genesis** is an autonomous testing agent that leverages Google Gemini AI and Retrieval Augmented Generation (RAG) to automatically generate comprehensive test cases and executable Selenium automation scripts from project documentation.

### Key Features
- 📚 **Intelligent Document Ingestion**: Processes multiple file formats (MD, TXT, JSON, HTML)
- 🧠 **RAG-Powered Context Retrieval**: Uses ChromaDB for semantic search
- 🤖 **AI Test Case Generation**: Creates structured test cases using Gemini
- 📜 **Selenium Script Generation**: Produces ready-to-execute Python automation scripts
- 🎨 **Modern UI**: Premium Streamlit interface with dark/light mode
- ☁️ **Cloud-Ready**: Deployed on Render.com (backend) and Streamlit Cloud (frontend)

---

## 🏗️ Architecture

### High-Level Architecture

```
┌─────────────────┐         ┌──────────────────┐
│   Streamlit UI  │────────▶│   FastAPI Backend │
│  (Frontend)     │  HTTP   │   (Backend)       │
└─────────────────┘         └──────────────────┘
                                      │
                    ┌─────────────────┼─────────────────┐
                    ▼                 ▼                 ▼
            ┌───────────────┐  ┌──────────┐   ┌────────────┐
            │ Ingestion     │  │   RAG    │   │    LLM     │
            │ Service       │  │ Service  │   │  Service   │
            └───────────────┘  └──────────┘   └────────────┘
                    │                 │                 │
                    ▼                 ▼                 ▼
            ┌───────────────┐  ┌──────────────────────────┐
            │  ChromaDB     │  │   Google Gemini API      │
            │  (In-Memory)  │  │  - Embeddings            │
            └───────────────┘  │  - Text Generation       │
                               └──────────────────────────┘
```

### Component Layers

1. **Presentation Layer**: Streamlit UI (`app/ui.py`)
2. **API Layer**: FastAPI endpoints (`app/main.py`)
3. **Service Layer**: Business logic (`app/services/`)
4. **Utility Layer**: Helper functions (`app/utils/`)
5. **Data Layer**: ChromaDB (in-memory vector store)
6. **AI Layer**: Google Gemini API

---

## 📁 Directory Structure

```
g:/qa/
│
├── app/                          # Main application package
│   ├── main.py                   # FastAPI backend entry point
│   ├── ui.py                     # Streamlit frontend
│   │
│   ├── services/                 # Business logic layer
│   │   ├── ingestion.py          # Document ingestion & vectorization
│   │   ├── rag_service.py        # Context retrieval (RAG)
│   │   └── llm_service.py        # LLM interactions (Gemini)
│   │
│   └── utils/                    # Utility functions
│       └── parsers.py            # File parsing utilities
│
├── .env                          # Environment variables (API keys)
├── .env.example                  # Template for environment variables
├── .gitignore                    # Git ignore rules
├── Procfile                      # Render deployment configuration
├── runtime.txt                   # Python version specification
├── requirements.txt              # Python dependencies
│
├── DEPLOYMENT.md                 # Deployment guide
├── README.md                     # Project overview
│
└── [Test Assets]                 # Sample test files
    ├── checkout.html             # Sample e-commerce checkout page
    ├── product_specs.md          # Sample product specifications
    └── ui_ux_guide.txt           # Sample UI/UX guidelines
```

---

## 🔧 Core Components

### 1. Backend (`app/main.py`)

**Purpose**: FastAPI server providing REST API endpoints

**Key Features**:
- **Framework**: FastAPI
- **Port**: Dynamic (set by `$PORT` environment variable)
- **CORS**: Enabled for cross-origin requests
- **Environment**: Loads from `.env` file

**Endpoints**:
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/ingest/` | Upload and process documents |
| POST | `/clear-kb/` | Clear knowledge base |
| POST | `/retrieve/` | Retrieve context for query |
| POST | `/generate-tests/` | Generate test cases |
| POST | `/generate-selenium/` | Generate Selenium script |

**Models**:
```python
class TestGenRequest(BaseModel):
    query: str

class SeleniumGenRequest(BaseModel):
    test_case: dict
    html_content: str
```

---

### 2. Frontend (`app/ui.py`)

**Purpose**: Interactive user interface built with Streamlit

**Key Features**:
- **Multi-tab Layout**: Dashboard, Ingestion, Test Generation, Script Automation
- **Dark/Light Mode**: Toggle in sidebar
- **Hybrid Workflow Diagram**: First 4 nodes horizontal, rest vertical
- **Real-time Interaction**: Direct API calls to backend
- **Download Capability**: Download generated Selenium scripts

**Tabs**:
1. **🏠 Dashboard**: Project overview, pipeline diagram, system stats
2. **📂 Knowledge Ingestion**: Upload and vectorize documents
3. **🧪 Test Generation**: Generate test cases from queries
4. **📜 Script Automation**: Generate Selenium automation scripts

**Environment Variables**:
- `BACKEND_URL`: Backend API endpoint (defaults to `http://localhost:8000`)
- `GOOGLE_API_KEY`: Required for Streamlit Cloud deployment

---

### 3. Ingestion Service (`app/services/ingestion.py`)

**Purpose**: Handle document processing and vector storage

**Flow**:
```
File Upload → Parse Content → Chunk Text → Generate Embeddings → Store in ChromaDB
```

**Key Functions**:

#### `get_vector_store()`
- **Returns**: In-memory ChromaDB instance
- **Singleton Pattern**: Global `_vector_store` ensures single instance
- **Cloud-Compatible**: No persistent storage (data in RAM)

#### `ingest_file(filename: str, content: bytes)`
- **Input**: Filename and raw file content
- **Process**:
  1. Parse file using `parse_file()` utility
  2. Split text into chunks (1000 chars, 100 overlap)
  3. Create `Document` objects with metadata
  4. Generate embeddings using Gemini (`text-embedding-004`)
  5. Store in ChromaDB
- **Output**: Number of chunks created

#### `clear_knowledge_base()`
- **Action**: Resets global vector store to `None`
- **Effect**: All ingested data is cleared from memory

**Dependencies**:
- `langchain_google_genai`: Embeddings
- `langchain.text_splitter`: Text chunking
- `langchain_community.vectorstores.Chroma`: Vector database
- `langchain.docstore.document`: Document wrapper

---

### 4. RAG Service (`app/services/rag_service.py`)

**Purpose**: Retrieve relevant context from vector database

**Key Function**:

#### `retrieve_context(query: str, k: int = 3)`
- **Input**: User query, number of results (default 3)
- **Process**:
  1. Get vector store instance
  2. Perform similarity search
  3. Concatenate documents with metadata
- **Output**: Formatted context string

**Example Output**:
```
Source: product_specs.md
Content: Discount code SAVE15 gives 15% off...

Source: ui_ux_guide.txt
Content: Error messages should be red...
```

---

### 5. LLM Service (`app/services/llm_service.py`)

**Purpose**: Interact with Google Gemini API for AI generation

**Configuration**:
- **Model**: `gemini-flash-latest`
- **API**: `google.generativeai`
- **Temperature**: 0.7 (balanced creativity)

**Key Functions**:

#### `generate_test_cases(context: str, query: str)`
- **Input**: Retrieved context + user query
- **Prompt Engineering**:
  - Role: Expert QA engineer
  - Output: JSON array of test cases
  - Fields: `Test_ID`, `Feature`, `Test_Scenario`, `Expected_Result`, `Grounded_In`
- **Output**: Parsed list of dictionaries

**Example Output**:
```json
[
  {
    "Test_ID": "TC_001",
    "Feature": "Discount Code",
    "Test_Scenario": "Apply valid discount code SAVE15",
    "Expected_Result": "15% discount applied to cart total",
    "Grounded_In": "product_specs.md"
  }
]
```

#### `generate_selenium_script(test_case: dict, html_content: str)`
- **Input**: Test case object + target HTML
- **Prompt Engineering**:
  - Role: Expert Selenium automation engineer
  - Output: Complete Python script with WebDriver setup
  - Includes: Assertions, waits, error handling
- **Output**: Complete executable Python code

---

### 6. Utilities (`app/utils/parsers.py`)

**Purpose**: Parse different file formats into text

**Supported Formats**:
- **`.txt`**: Plain text
- **`.md`**: Markdown
- **`.json`**: JSON (stringified)
- **`.html`**: HTML (extracted text via BeautifulSoup)

**Key Function**:

#### `parse_file(filename: str, content: bytes)`
- **Logic**: Extension-based routing
- **Error Handling**: Raises exception for unsupported formats
- **Encoding**: UTF-8 decoding

---

## 🔄 Data Flow

### End-to-End Flow

```
1. User uploads documents (MD, TXT, HTML)
   ↓
2. UI sends files to /ingest/ endpoint
   ↓
3. Ingestion Service:
   - Parses each file
   - Splits into chunks
   - Generates embeddings (Gemini)
   - Stores in ChromaDB
   ↓
4. User enters test query
   ↓
5. UI sends query to /generate-tests/
   ↓
6. RAG Service retrieves relevant context
   ↓
7. LLM Service generates test cases
   ↓
8. UI displays test cases
   ↓
9. User selects test case + uploads HTML
   ↓
10. UI sends to /generate-selenium/
   ↓
11. LLM Service generates Selenium script
   ↓
12. UI displays script + download button
```

### Data Transformation Pipeline

```
Raw File (bytes)
    ↓ [Parser]
Plain Text (string)
    ↓ [Text Splitter]
Text Chunks (list)
    ↓ [Embeddings]
Vector Embeddings (arrays)
    ↓ [ChromaDB]
Stored Vectors
    ↓ [Similarity Search]
Retrieved Context (string)
    ↓ [LLM Prompt]
Generated Output (JSON/Python)
```

---

## 🌐 API Endpoints

### Complete API Reference

#### 1. Health Check
```http
GET /
```
**Response**:
```json
{
  "message": "QA Agent API is running"
}
```

---

#### 2. Ingest Documents
```http
POST /ingest/
Content-Type: multipart/form-data
```

**Request**:
- Form field: `files` (multiple files allowed)

**Response**:
```json
{
  "message": "Ingestion successful",
  "files": ["product_specs.md", "ui_ux_guide.txt"],
  "total_chunks": 25
}
```

**Error Codes**:
- `500`: Processing error

---

#### 3. Clear Knowledge Base
```http
POST /clear-kb/
```

**Response**:
```json
{
  "message": "Knowledge base cleared"
}
```

---

#### 4. Retrieve Context
```http
POST /retrieve/
Content-Type: application/json
```

**Request Body**:
```json
{
  "query": "discount code validation"
}
```

**Response**:
```json
{
  "context": "Source: product_specs.md\nContent: ..."
}
```

---

#### 5. Generate Test Cases
```http
POST /generate-tests/
Content-Type: application/json
```

**Request Body**:
```json
{
  "query": "Test discount code functionality"
}
```

**Response**:
```json
{
  "test_cases": [
    {
      "Test_ID": "TC_001",
      "Feature": "Discount Validation",
      "Test_Scenario": "Apply valid code",
      "Expected_Result": "Discount applied",
      "Grounded_In": "product_specs.md"
    }
  ]
}
```

**Error Codes**:
- `404`: No relevant context found

---

#### 6. Generate Selenium Script
```http
POST /generate-selenium/
Content-Type: application/json
```

**Request Body**:
```json
{
  "test_case": { /* test case object */ },
  "html_content": "<html>...</html>"
}
```

**Response**:
```json
{
  "selenium_script": "from selenium import webdriver\n..."
}
```

---

## ☁️ Deployment Architecture

### Production Setup

```
┌──────────────────────────────────────────────┐
│          Internet / End Users                │
└────────────┬─────────────────────────────────┘
             │
     ┌───────┴──────────┐
     │                  │
     ▼                  ▼
┌─────────────┐   ┌──────────────┐
│  Streamlit  │   │   Render     │
│   Cloud     │──▶│   Backend    │
│  Frontend   │   │   FastAPI    │
└─────────────┘   └──────────────┘
                         │
                  ┌──────┴──────┐
                  │             │
                  ▼             ▼
         ┌────────────┐  ┌──────────────┐
         │ In-Memory  │  │    Google    │
         │ ChromaDB   │  │  Gemini API  │
         └────────────┘  └──────────────┘
```

### Platform Details

**Frontend**: Streamlit Community Cloud
- **URL**: `https://[app-name].streamlit.app`
- **Free Tier**: Unlimited for public repos
- **Auto-deploy**: On GitHub push

**Backend**: Render.com
- **URL**: `https://autonomous-qa-agent-isn6.onrender.com`
- **Free Tier**: 750 hours/month
- **Spin Down**: After 15 min inactivity
- **Cold Start**: ~30 seconds

### Environment Variables

| Variable | Used By | Purpose |
|----------|---------|---------|
| `GOOGLE_API_KEY` | Both | Gemini API authentication |
| `BACKEND_URL` | Frontend | Backend endpoint URL |
| `PORT` | Backend | Dynamic port (set by platform) |

---

## 🛠️ Technology Stack

### Backend
- **Framework**: FastAPI 0.104+
- **Server**: Uvicorn (ASGI)
- **Vector DB**: ChromaDB 0.4.0+
- **Embeddings**: Google Generative AI Embeddings
- **LLM**: Google Gemini (gemini-flash-latest)

### Frontend
- **Framework**: Streamlit
- **HTTP Client**: Requests
- **Diagrams**: Graphviz
- **Styling**: Custom CSS

### AI/ML
- **LangChain**: 0.1.0+
  - `langchain-core`: Core utilities
  - `langchain-google-genai`: Gemini integration
  - `langchain-community`: Community tools
- **Google Generative AI**: 0.3.0+

### Utilities
- **File Parsing**: BeautifulSoup4
- **File Upload**: Python-multipart
- **Environment**: Python-dotenv

### Development
- **Language**: Python 3.11
- **Version Control**: Git + GitHub
- **Deployment**: Procfile + runtime.txt

---

## 📊 Key Design Decisions

### 1. In-Memory ChromaDB
**Rationale**: Free cloud platforms don't provide persistent storage
**Trade-off**: Data cleared on restart (acceptable for document-based workflow)
**Alternative**: Could upgrade to paid tier with disk persistence

### 2. Separation of Concerns
**Backend-Frontend Split**: Independent deployment and scaling
**Service Layer**: Modularity for testing and maintenance
**Utility Layer**: Reusable parsing logic

### 3. RAG Architecture
**Why RAG**: Grounds AI in actual documentation
**Benefits**: Accurate, traceable, hallucination-resistant
**K=3 Default**: Balance between context richness and token limits

### 4. Gemini Flash Model
**Choice**: `gemini-flash-latest`
**Reason**: Fast, cost-effective, sufficient for task
**Alternative**: `gemini-pro` for more complex reasoning

---

## 🔐 Security Considerations

1. **API Keys**: Never committed to Git (`.env` in `.gitignore`)
2. **CORS**: Configured for specific origins in production
3. **Input Validation**: Pydantic models enforce schema
4. **Error Handling**: Sanitized error messages (no stack traces to users)
5. **Rate Limiting**: Consider adding for production (e.g., slowapi)

---

## 🚀 Future Enhancements

1. **Persistent Storage**: Integrate with cloud vector DB (Pinecone, Weaviate)
2. **Authentication**: Add user auth for multi-tenant deployment
3. **Test Execution**: Run generated Selenium scripts directly
4. **Batch Processing**: Support bulk test generation
5. **Results Dashboard**: Track test execution results
6. **CI/CD Integration**: GitHub Actions for automated testing

---

## 📚 Dependencies Graph

```
FastAPI
  ├── Pydantic (models)
  ├── Uvicorn (server)
  └── Python-multipart (file upload)

LangChain
  ├── langchain-core
  ├── langchain-google-genai
  └── langchain-community
      └── ChromaDB

Google Generative AI
  └── Gemini API

Streamlit
  ├── Requests (HTTP)
  └── Graphviz (diagrams)

Utilities
  ├── BeautifulSoup4 (HTML parsing)
  └── Python-dotenv (env vars)
```

---

**Documentation Version**: 1.0  
**Last Updated**: 2025-11-24  
**Project Status**: Production-Ready ✅
