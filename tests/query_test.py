from fastapi.testclient import TestClient
from app.main import app  

client = TestClient(app)

def test_query_document_async():
    # Send GET request for querying with async API
    response = client.get("/query", params={"document_id": "some_document_id"})

    # Assert the status code and check the document is returned correctly
    assert response.status_code == 200
    data = response.json()
    assert data["document_id"] == "some_document_id"
    assert "content" in data 
