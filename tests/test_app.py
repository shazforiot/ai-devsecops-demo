"""
Unit tests for the fixed Flask application
"""
import pytest
from src.app_fixed import app
import json

@pytest.fixture
def client():
    """Create test client"""
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_health_check(client):
    """Test health endpoint"""
    response = client.get('/health')
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['status'] == 'healthy'

def test_calculate_valid(client):
    """Test valid division operation"""
    response = client.post('/calculate', data={'num1': '10', 'num2': '2'})
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['result'] == 5.0

def test_calculate_division_by_zero(client):
    """Test division by zero returns error"""
    response = client.post('/calculate', data={'num1': '10', 'num2': '0'})
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'Division by zero' in data['error']

def test_calculate_invalid_input(client):
    """Test invalid input handling"""
    response = client.post('/calculate', data={'num1': 'abc', 'num2': '2'})
    assert response.status_code == 400

def test_greet_with_name(client):
    """Test greeting with name parameter"""
    response = client.get('/greet?name=John')
    assert response.status_code == 200
    assert b'Hello' in response.data

def test_greet_xss_prevention(client):
    """Test XSS attack prevention"""
    response = client.get('/greet?name=<script>alert("XSS")</script>')
    # Should escape the script tags
    assert b'<script>' not in response.data or b'&lt;script&gt;' in response.data

def test_file_path_traversal_prevention(client):
    """Test path traversal attack is prevented"""
    response = client.get('/file/../../etc/passwd')
    assert response.status_code == 403
