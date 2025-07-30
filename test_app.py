import pytest
from app import app

@pytest.fixture
def client():
    """Create a test client for the Flask application."""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_index_route(client):
    """Test that the index route returns a 200 status code."""
    response = client.get('/')
    assert response.status_code == 200

def test_resume_maker_route(client):
    """Test that the resume maker route returns a 200 status code."""
    response = client.get('/resume-maker')
    assert response.status_code == 200

def test_extract_keywords_empty_description(client):
    """Test extract keywords with empty job description."""
    response = client.post('/extract-keywords', 
                          json={'job_description': ''})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_extract_keywords_short_description(client):
    """Test extract keywords with short job description."""
    response = client.post('/extract-keywords', 
                          json={'job_description': 'short'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_generate_resume_missing_fields(client):
    """Test generate resume with missing required fields."""
    response = client.post('/generate-resume', 
                          json={'name': 'Test User'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_generate_pdf_missing_fields(client):
    """Test generate PDF with missing required fields."""
    response = client.post('/generate-pdf', 
                          json={'name': 'Test User'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_ai_rewrite_job_description_empty(client):
    """Test AI rewrite job description with empty bullet points."""
    response = client.post('/ai-rewrite-job-description', 
                          json={'bullet_points': []})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_ai_rewrite_project_description_empty(client):
    """Test AI rewrite project description with empty bullet points."""
    response = client.post('/ai-rewrite-project-description', 
                          json={'bullet_points': []})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data 