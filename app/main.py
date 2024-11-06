from fastapi import FastAPI, HTTPException, File, UploadFile, Form
from fastapi.responses import JSONResponse
from pydantic import BaseModel
import chromadb
from sentence_transformers import SentenceTransformer
import uuid
import os
from io import StringIO
from PyPDF2 import PdfReader
from docx import Document

# Initialize the app and Chroma client
app = FastAPI()
client = chromadb.Client()
collection = client.create_collection("documents")

# Load the sentence transformer model
model = SentenceTransformer('all-MiniLM-L6-v2')

# Helper function to extract text from different document formats
def extract_text_from_pdf(file):
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    return text

def extract_text_from_docx(file):
    doc = Document(file)
    text = ""
    for para in doc.paragraphs:
        text += para.text
    return text

def extract_text_from_txt(file):
    text = file.read().decode("utf-8")
    return text

# Define the Pydantic model for the request body
class DocumentRequest(BaseModel):
    text: str
    metadata: dict

# Endpoint to ingest documents
@app.post("/ingest")
async def ingest_document(
    file: UploadFile = File(...),
    metadata: str = Form(...)
):
    # Parse the metadata from string to dictionary
    try:
        metadata_dict = eval(metadata)  # Use eval cautiously, consider using json.loads instead
    except Exception as e:
        raise HTTPException(status_code=400, detail="Invalid metadata format")

    # Extract text based on the file extension
    filename = file.filename.lower()
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file.file)
    elif filename.endswith(".docx"):
        text = extract_text_from_docx(file.file)
    elif filename.endswith(".txt"):
        text = extract_text_from_txt(file.file)
    else:
        raise HTTPException(status_code=400, detail="Unsupported file type")

    # Generate embedding for the document text
    embedding = model.encode(text)

    # Create a unique ID for the document
    doc_id = str(uuid.uuid4())

    # Add the document to the Chroma collection
    collection.add(
        documents=[text],
        metadatas=[metadata_dict],
        embeddings=[embedding],
        ids=[doc_id]
    )

    return JSONResponse(content={"message": "Document ingested successfully", "document_id": doc_id})

# Endpoint to query documents
@app.get("/query")
async def query_document(query: str):
    # Generate embedding for the query text
    query_embedding = model.encode(query)

    # Perform search on Chroma collection
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=5
    )

    # Structure the response
    structured_results = []
    for doc, meta in zip(results['documents'], results['metadatas']):
        structured_results.append({
            "document": doc,
            "metadata": meta
        })

    # Return structured results
    return {"results": structured_results}