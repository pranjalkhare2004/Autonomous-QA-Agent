# Autonomous QA Agent

This project is an Autonomous QA Agent that ingests project documentation and HTML to generate Test Cases and executable Selenium Scripts using Google Gemini API.

## Project Structure

- `app/main.py`: FastAPI Backend
- `app/ui.py`: Streamlit Frontend
- `app/services/`: Logic for Ingestion, RAG, and LLM interaction
- `app/utils/`: Helper functions
- `chroma_db/`: Persistent Vector Database storage

## Setup

1.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

2.  **Environment Variables**:
    Create a `.env` file in the root directory and add your Google Gemini API Key:
    ```
    GOOGLE_API_KEY=your_api_key_here
    ```

## Running the Application

1.  **Start the Backend (FastAPI)**:
    ```bash
    uvicorn app.main:app --reload
    ```
    The API will run at `http://localhost:8000`.

2.  **Start the Frontend (Streamlit)**:
    Open a new terminal and run:
    ```bash
    streamlit run app/ui.py
    ```
    The UI will open in your browser (usually at `http://localhost:8501`).

## Usage Guide

### Phase 1: Ingestion
1.  Go to the **Knowledge Base Ingestion** sidebar in the Streamlit UI.
2.  Upload `product_specs.md`, `ui_ux_guide.txt`, and `checkout.html`.
3.  Click **Ingest Documents**.

### Phase 2: Test Case Generation
1.  In the main area, under **Test Case Generation**, enter a query (e.g., "Generate tests for discount code").
2.  Click **Generate Test Cases**.
3.  Review the generated test cases.

### Phase 3: Selenium Script Generation
1.  Expand a generated test case to view details.
2.  Click **Generate Script for [Test ID]**.
3.  Upload the target `checkout.html` file in the **Selenium Script Generation** column.
4.  Click **Generate Selenium Script**.
5.  Copy and run the generated Python code!

## Test Assets
The following test assets are included in the root directory:
- `checkout.html`
- `product_specs.md`
- `ui_ux_guide.txt`
