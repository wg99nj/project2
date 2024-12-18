import pytest
from app import create_app, db
from app.models.user import User
from flask import json

@pytest.fixture
def app():
    app = create_app('testing')
    app.config['TESTING'] = True
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_update_user_profile(client, app):
    with app.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location", token="valid_token")
        user.save()
        response = client.put('/api/users/profile', headers={'Authorization': 'Bearer valid_token'}, json={
            'name': 'Updated Name',
            'bio': 'Updated Bio',
            'location': 'Updated Location'
        })
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Updated Name'
        assert data['bio'] == 'Updated Bio'
        assert data['location'] == 'Updated Location'

def test_update_user_profile_validation(client, app):
    with app.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location", token="valid_token")
        user.save()
        response = client.put('/api/users/profile', headers={'Authorization': 'Bearer valid_token'}, json={
            'name': '',
            'bio': 'Updated Bio',
            'location': 'Updated Location'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

def test_update_user_profile_missing_fields(client, app):
    with app.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location", token="valid_token")
        user.save()
        response = client.put('/api/users/profile', headers={'Authorization': 'Bearer valid_token'}, json={
            'name': 'Updated Name',
            'bio': '',
            'location': 'Updated Location'
        })
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data

def test_update_user_profile_invalid_token(client, app):
    with app.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location", token="valid_token")
        user.save()
        response = client.put('/api/users/profile', headers={'Authorization': 'Bearer invalid_token'}, json={
            'name': 'Updated Name',
            'bio': 'Updated Bio',
            'location': 'Updated Location'
        })
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data

def test_upgrade_user_to_professional(client, app):
    with app.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location", token="valid_token", role="admin")
        user.save()
        response = client.post(f'/api/users/{user.id}/upgrade', headers={'Authorization': 'Bearer valid_token'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['professional_status'] == True

def test_upgrade_user_to_professional_invalid_token(client, app):
    with app.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location", token="valid_token", role="admin")
        user.save()
        response = client.post(f'/api/users/{user.id}/upgrade', headers={'Authorization': 'Bearer invalid_token'})
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data

def test_upgrade_user_to_professional_non_admin(client, app):
    with app.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location", token="valid_token", role="user")
        user.save()
        response = client.post(f'/api/users/{user.id}/upgrade', headers={'Authorization': 'Bearer valid_token'})
        assert response.status_code == 403
        data = json.loads(response.data)
        assert 'error' in data

def test_get_user_profile(client, app):
    with app.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location", token="valid_token")
        user.save()
        user_id = user.id  # Ensure the user ID is retrieved after saving
        response = client.get(f'/api/users/{user_id}', headers={'Authorization': 'Bearer valid_token'})
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['name'] == 'Test User'
        assert data['bio'] == 'Test Bio'
        assert data['location'] == 'Test Location'

def test_get_user_profile_invalid_token(client, app):
    with app.app_context():
        user = User(name="Test User", bio="Test Bio", location="Test Location", token="valid_token")
        user.save()
        user_id = user.id  # Ensure the user ID is retrieved after saving
        response = client.get(f'/api/users/{user_id}', headers={'Authorization': 'Bearer invalid_token'})
        assert response.status_code == 401
        data = json.loads(response.data)
        assert 'error' in data

def test_get_user_profile_non_existent_user(client, app):
    with app.app_context():
        # Ensure a valid token is used for authorization
        user = User(name="Test User", bio="Test Bio", location="Test Location", token="valid_token")
        user.save()
        response = client.get('/api/users/999', headers={'Authorization': 'Bearer valid_token'})
        assert response.status_code == 404
        data = json.loads(response.data)
        assert 'error' in data

