import os
import pytest
import requests

# URL of the FastAPI server
BASE_URL = "http://127.0.0.1:8000/ingest"

# Path to a sample document in your tests folder (updated file path)
SAMPLE_PDF_PATH = os.path.join(os.path.dirname(__file__), 'sample.pdf')

# Sample metadata for testing
SAMPLE_METADATA = {
    "author": "John Doe",
    "category": "test"
}

def test_ingest_document():
    # Open the file in binary mode
    with open(SAMPLE_PDF_PATH, 'rb') as file:
        # Send POST request with the file and metadata
        files = {'file': ('sample.pdf', file, 'application/pdf')}
        data = {'metadata': str(SAMPLE_METADATA)}
        response = requests.post(BASE_URL, files=files, data=data)

        # Check if the response status is 200 OK
        assert response.status_code == 200
        response_json = response.json()

        # Assert the response contains a success message and document ID
        assert response_json['message'] == 'Document ingested successfully'
        assert 'document_id' in response_json

def test_invalid_metadata():
    # Open the file in binary mode
    with open(SAMPLE_PDF_PATH, 'rb') as file:
        # Send POST request with invalid metadata (wrong format)
        files = {'file': ('sample.pdf', file, 'application/pdf')}
        data = {'metadata': 'invalid_metadata'}  # Invalid metadata format
        response = requests.post(BASE_URL, files=files, data=data)

        # Check if the response status is 400 Bad Request
        assert response.status_code == 400
        response_json = response.json()

        # Assert the response contains an error message indicating bad request
        assert 'detail' in response_json


def test_missing_file():
    # Send POST request with missing file
    response = requests.post(BASE_URL, data={'metadata': str(SAMPLE_METADATA)})

    # Check if the response status is 422 Unprocessable Entity (missing file)
    assert response.status_code == 422
    response_json = response.json()

    # Assert the response contains an error message
    assert response_json['detail'][0]['msg'] == 'Field required'
    assert response_json['detail'][0]['loc'] == ['body', 'file']

def test_missing_metadata():
    # Open the file in binary mode
    with open(SAMPLE_PDF_PATH, 'rb') as file:
        # Send POST request with missing metadata
        files = {'file': ('sample.pdf', file, 'application/pdf')}
        response = requests.post(BASE_URL, files=files)

        # Check if the response status is 422 Unprocessable Entity (missing metadata)
        assert response.status_code == 422
        response_json = response.json()

        # Assert the response contains an error message
        assert response_json['detail'][0]['msg'] == 'Field required'
        assert response_json['detail'][0]['loc'] == ['body', 'metadata']
