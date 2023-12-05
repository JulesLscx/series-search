from api.app import create_app
from api.models import db, Users, Role
import pytest
import os

@pytest.fixture
def admin_client():
    app = create_app()
    with app.test_client() as test_client:
        # Log in as admin and set the remember_token cookie
        connect = test_client.post('/serie-search/login', json={'name': 'admin', 'password': 'your_password'})
        yield test_client
        # Log out after the test
        logout = test_client.get('/serie-search/logout')

@pytest.fixture
def user_client():
    app = create_app()
    with app.test_client() as test_client:
        connect = test_client.post('/serie-search/login', json={'name': 'user', 'password': 'your_password'})
        yield test_client
        logout = test_client.get('/serie-search/logout')

@pytest.mark.usefixtures("admin_client")
def test_create_user(admin_client):
    # Check if the user is not in the database
    user = db.session.query(Users).filter_by(name='test2').first()
    response = admin_client.post('/serie-search/admin/user/create', json={'name': 'test2', 'password': 'test2', 'role': 0})
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully'
    # Check if the user is in the database
    user = db.session.query(Users).filter_by(name='test2').first()
    assert user is not None
    assert user.name == 'test2'
    assert user.check_password('test2')
    assert user.role == Role.USER.value
    db.session.delete(user)
    db.session.commit()
@pytest.mark.usefixtures("user_client")
def test_create_user_not_admin(user_client):
    response = user_client.post('/serie-search/admin/user/create', json={'name': 'test2', 'password': 'test2', 'role': 0})
    assert response.status_code == 403
    assert response.json['message'] == 'You do not have permission to create users'
    
@pytest.mark.usefixtures('user_client')
def test_edit_user_unauthorized(user_client):
    response = user_client.put('/serie-search/admin/user/edit/user', json={'role': 1})
    assert response.status_code == 403
    assert response.json['message'] == 'You do not have permission to edit users'
    
@pytest.mark.usefixtures("admin_client")
def test_delete_user(admin_client):
    user = db.session.query(Users).filter_by(name='user').first()
    if user is None:
        user = Users(name='user', password='your_password', role=0)
        db.session.add(user)
        db.session.commit()
    response = admin_client.delete('/serie-search/admin/user/delete/user')
    assert response.status_code == 200
    assert response.json['message'] == 'User deleted successfully'
    user = db.session.query(Users).filter_by(name='user').first()
    assert user is None
    user = Users(name='user', password='your_password', role=0)
    db.session.add(user)
    db.session.commit()

@pytest.mark.usefixtures("user_client")
def test_delete_user_not_admin(user_client):
    response = user_client.delete('/serie-search/admin/user/delete/user')
    assert response.status_code == 403
    assert response.json['message'] == 'You do not have permission to delete users'

@pytest.mark.usefixtures("admin_client")
def test_edit_user(admin_client):
    user = db.session.query(Users).filter_by(name='user').first()
    if user is None:
        user = Users(name='user', password='your_password', role=0)
        db.session.add(user)
        db.session.commit()
    response = admin_client.put('/serie-search/admin/user/edit/user', json={'role': 1})
    assert response.status_code == 200
    assert response.json['message'] == 'User edited successfully'
    user = db.session.query(Users).filter_by(name='user').first()
    assert user.role == Role.ADMIN.value
    user.role = Role.USER.value
    db.session.commit()

@pytest.mark.usefixtures("admin_client")
def test_edit_user_not_existing(admin_client):
    response = admin_client.put('/serie-search/admin/user/edit/my_user', json={'role': 1})
    assert response.status_code == 400
    assert response.json['message'] == 'User does not exist'

@pytest.mark.usefixtures("admin_client")
def test_edit_user_wrong_role(admin_client):
    response = admin_client.put('/serie-search/admin/user/edit/user', json={'role': 2})
    assert response.status_code == 400
    assert response.json['message'] == 'Role must be 0 for user or 1 for admin'