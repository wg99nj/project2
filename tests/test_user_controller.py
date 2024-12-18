import pytest
from app import create_app, db
from app.models.user import User
from app.models.notification import Notification

@pytest.fixture(scope='module')
def test_client():
    flask_app = create_app('config.TestingConfig')
    testing_client = flask_app.test_client()

    ctx = flask_app.app_context()
    ctx.push()

    yield testing_client

    ctx.pop()

@pytest.fixture(scope='module')
def init_database():
    db.create_all()

    yield db

    db.session.remove()
    db.drop_all()

def test_update_user_profile(test_client, init_database):
    user = User(name='John Doe', bio='Developer', location='NYC')
    user.save()
    response = test_client.put('/api/users/profile', json={
        'name': 'Jane Doe',
        'bio': 'Designer',
        'location': 'LA'
    }, headers={'Authorization': f'Bearer {user.generate_auth_token()}'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'Jane Doe'
    assert data['bio'] == 'Designer'
    assert data['location'] == 'LA'

def test_update_user_profile_validation(test_client, init_database):
    user = User(name='John Doe', bio='Developer', location='NYC')
    user.save()
    response = test_client.put('/api/users/profile', json={
        'name': '',
        'bio': 'Designer',
        'location': 'LA'
    }, headers={'Authorization': f'Bearer {user.generate_auth_token()}'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_update_user_profile_missing_fields(test_client, init_database):
    user = User(name='John Doe', bio='Developer', location='NYC')
    user.save()
    response = test_client.put('/api/users/profile', json={
        'name': 'Jane Doe',
        'bio': '',
        'location': 'LA'
    }, headers={'Authorization': f'Bearer {user.generate_auth_token()}'})
    assert response.status_code == 400
    data = response.get_json()
    assert 'error' in data

def test_update_user_profile_invalid_token(test_client, init_database):
    user = User(name='John Doe', bio='Developer', location='NYC')
    user.save()
    response = test_client.put('/api/users/profile', json={
        'name': 'Jane Doe',
        'bio': 'Designer',
        'location': 'LA'
    }, headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401

def test_upgrade_user_to_professional(test_client, init_database):
    user = User(name='John Doe', bio='Developer', location='NYC')
    user.save()
    response = test_client.post(f'/api/users/{user.id}/upgrade', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['professional_status'] is True
    notification = Notification.query.filter_by(user_id=user.id).first()
    assert notification is not None
    assert notification.message == 'Your account has been upgraded to professional status.'

def test_upgrade_user_to_professional_invalid_token(test_client, init_database):
    user = User(name='John Doe', bio='Developer', location='NYC')
    user.save()
    response = test_client.post(f'/api/users/{user.id}/upgrade', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401

def test_upgrade_user_to_professional_non_admin(test_client, init_database):
    user = User(name='John Doe', bio='Developer', location='NYC')
    user.save()
    non_admin_user = User(name='Jane Doe', bio='Designer', location='LA')
    non_admin_user.save()
    response = test_client.post(f'/api/users/{user.id}/upgrade', headers={'Authorization': f'Bearer {non_admin_user.generate_auth_token()}'})
    assert response.status_code == 403

def test_get_user_profile(test_client, init_database):
    user = User(name='John Doe', bio='Developer', location='NYC')
    user.save()
    response = test_client.get(f'/api/users/{user.id}', headers={'Authorization': f'Bearer {user.generate_auth_token()}'})
    assert response.status_code == 200
    data = response.get_json()
    assert data['name'] == 'John Doe'
    assert data['bio'] == 'Developer'
    assert data['location'] == 'NYC'

def test_get_user_profile_invalid_token(test_client, init_database):
    user = User(name='John Doe', bio='Developer', location='NYC')
    user.save()
    response = test_client.get(f'/api/users/{user.id}', headers={'Authorization': 'Bearer invalid_token'})
    assert response.status_code == 401

def test_get_user_profile_non_existent_user(test_client, init_database):
    response = test_client.get('/api/users/999', headers={'Authorization': f'Bearer {admin_token}'})
    assert response.status_code == 404
