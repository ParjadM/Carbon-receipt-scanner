import pytest
import io
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_page(client):
    """Test that the index page loads successfully."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'<div id="root"></div>' in response.data

def test_api_scan_no_file(client):
    """Test that the /api/scan endpoint correctly rejects requests without a file."""
    response = client.post('/api/scan')
    assert response.status_code == 400
    assert b'No file uploaded' in response.data

def test_api_scan_empty_file(client):
    """Test that the /api/scan endpoint correctly handles an empty file upload."""
    data = {
        'receipt': (io.BytesIO(b""), '')
    }
    response = client.post('/api/scan', data=data, content_type='multipart/form-data')
    assert response.status_code == 400
    assert b'No selected file' in response.data
