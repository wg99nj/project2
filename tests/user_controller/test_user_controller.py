import pytest
from app import create_app, db
from app.models.user import User
from flask import json

@pytest.fixture
def client():
    app = create_app('testing')
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

def test_update_user_profile(client):
    with client.application.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location")
        user.save()
        response = client.put('/api/users/profile', json={
            'name': 'Updated Name',
            'bio': 'Updated Bio',
            'location': 'Updated Location'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Updated Name'
        assert data['bio'] == 'Updated Bio'
        assert data['location'] == 'Updated Location'

def test_update_user_profile_validation(client):
    with client.application.app_context():
        response = client.put('/api/users/profile', json={
            'name': '',
            'bio': 'Updated Bio',
            'location': 'Updated Location'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

def test_update_user_profile_missing_fields(client):
    with client.application.app_context():
        response = client.put('/api/users/profile', json={
            'name': 'Updated Name',
            'bio': '',
            'location': 'Updated Location'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

def test_update_user_profile_invalid_token(client):
    with client.application.app_context():
        response = client.put('/api/users/profile', headers={'Authorization': 'Bearer invalid_token'}, json={
            'name': 'Updated Name',
            'bio': 'Updated Bio',
            'location': 'Updated Location'
        })
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data

def test_upgrade_user_to_professional(client):
    with client.application.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location")
        user.save()
        response = client.post(f'/api/users/{user.id}/upgrade')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['professional_status'] == True

def test_upgrade_user_to_professional_invalid_token(client):
    with client.application.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location")
        user.save()
        response = client.post(f'/api/users/{user.id}/upgrade', headers={'Authorization': 'Bearer invalid_token'})
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data

def test_upgrade_user_to_professional_non_admin(client):
    with client.application.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location")
        user.save()
        response = client.post(f'/api/users/{user.id}/upgrade', headers={'Authorization': 'Bearer non_admin_token'})
        assert response.status_code == 403
        data = json.loads(response.data)
        assert 'error' in data

def test_get_user_profile(client):
    with client.application.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location")
        user.save()
        response = client.get(f'/api/users/{user.id}')
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Test User'
        assert data['bio'] == 'Test Bio'
        assert data['location'] == 'Test Location'

def test_get_user_profile_invalid_token(client):
    with client.application.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location")
        user.save()
        response = client.get(f'/api/users/{user.id}', headers={'Authorization': 'Bearer invalid_token'})
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data

def test_get_user_profile_non_existent_user(client):
    response = client.get('/api/users/999')
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'error' in data
