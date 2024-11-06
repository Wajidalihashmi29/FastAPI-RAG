# Lightweight FastAPI RAG Server with ChromaDB and Sentence Transformers
This project implements a lightweight FastAPI server for Retrieval Augmented Generation (RAG) using ChromaDB and Sentence Transformers.
## Problem Statement
The objective is to build a REST API server that allows users to:
- Upload documents in various formats (PDF, DOC, DOCX, TXT).
- Query the documents using natural language questions.
- Retrieve relevant information from the documents based on the query.
## Technologies
- FastAPI: A modern, fast (high-performance), and easy-to-use web framework for building APIs with Python.
- ChromaDB: A vector database for embedding-based search, designed for efficient indexing and querying of large document collections.
- Sentence Transformers: A library for efficient sentence embedding generation using pre-trained transformer models, enabling semantic similarity search.
- Hugging Face: Provides access to a wide range of pre-trained models, including the all-MiniLM-L6-v2 model used for sentence embeddings
## Working Principle
### Document Ingestion:

- When a user uploads a document, the server extracts its text using appropriate libraries (e.g., PyPDF2 for PDF).
- Sentence Transformers encode each sentence in the document into a vector representation.
- ChromaDB stores these vectors along with the corresponding text and document metadata.
### Query Processing:

- When a user submits a natural language query, the server embeds the query using Sentence Transformers.
- ChromaDB searches for the nearest neighbors of the query vector in its index.
- The server retrieves the most relevant sentences from the documents based on the search results.
### Response Generation:

- The server constructs a response containing the relevant sentences retrieved from ChromaDB.
- The response can be formatted for display, further processed for better readability, or used as input for a generative model (e.g., OpenAI's GPT-3).
## Implementation Details
### API Endpoints:

- /ingest: Accepts a file upload, extracts text, generates embeddings, and stores data in ChromaDB.
- /query: Accepts a natural language query, generates embeddings, searches ChromaDB, and returns relevant sentences.
## Running the Project

To run the FastAPI server for the RAG implementation, follow these steps:

- Clone the Repository:
```bash
git clone <repository-url>
cd <repository-directory>
```
- Set Up a Virtual Environment (optional but recommended):

```bash

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```
- Install Required Dependencies:

```bash
pip install -r requirements.txt
```

- Run the FastAPI Server:

```bash
uvicorn app.main:app --reload
```