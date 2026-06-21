import pytest
from app import app, tasks

@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

@pytest.fixture(autouse=True)
def run_around_tests():
    # Setup: clear tasks before each test
    tasks.clear()
    import app as main_app
    main_app.task_id_counter = 1
    yield
    # Teardown

def test_index(client):
    response = client.get('/')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Welcome to the CI/CD Task API!"}

def test_health_check(client):
    response = client.get('/health')
    assert response.status_code == 200
    assert response.get_json() == {"status": "healthy", "version": "1.0.0"}

def test_get_tasks_empty(client):
    response = client.get('/tasks')
    assert response.status_code == 200
    assert response.get_json() == []

def test_create_task_valid(client):
    response = client.post('/tasks', json={
        "title": "Learn CI/CD",
        "description": "Understand Docker and GitHub Actions"
    })
    assert response.status_code == 201
    data = response.get_json()
    assert data['title'] == "Learn CI/CD"
    assert data['description'] == "Understand Docker and GitHub Actions"
    assert 'id' in data
    assert 'created_at' in data

def test_create_task_missing_title(client):
    response = client.post('/tasks', json={
        "description": "Missing title field"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing title or description"}

def test_create_task_missing_description(client):
    response = client.post('/tasks', json={
        "title": "Missing desc"
    })
    assert response.status_code == 400
    assert response.get_json() == {"error": "Missing title or description"}

def test_create_task_invalid_json(client):
    response = client.post('/tasks', data="not json", content_type='application/json')
    assert response.status_code == 400

def test_get_tasks_with_data(client):
    client.post('/tasks', json={"title": "T1", "description": "D1"})
    client.post('/tasks', json={"title": "T2", "description": "D2"})
    
    response = client.get('/tasks')
    assert response.status_code == 200
    assert len(response.get_json()) == 2

def test_get_specific_task(client):
    post_response = client.post('/tasks', json={"title": "T1", "description": "D1"})
    task_id = post_response.get_json()['id']
    
    response = client.get(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.get_json()['title'] == "T1"

def test_get_non_existent_task(client):
    response = client.get('/tasks/999')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}

def test_delete_task(client):
    post_response = client.post('/tasks', json={"title": "T1", "description": "D1"})
    task_id = post_response.get_json()['id']
    
    response = client.delete(f'/tasks/{task_id}')
    assert response.status_code == 200
    assert response.get_json() == {"message": "Task deleted successfully"}
    
    # Verify it's gone
    get_response = client.get(f'/tasks/{task_id}')
    assert get_response.status_code == 404

def test_delete_non_existent_task(client):
    response = client.delete('/tasks/999')
    assert response.status_code == 404
    assert response.get_json() == {"error": "Task not found"}
