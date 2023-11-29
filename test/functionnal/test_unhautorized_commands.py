from api.app import create_app
import os

def test_test_env():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get('/serie-search/')
        assert response.status_code == 200
        assert response.json['message'] == 'API is ready'

def test_logout_without_login():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get('/serie-search/logout')
        assert response.status_code == 401
        
def test_create_user_for_non_admin(): 
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.post('/serie-search/login', json={'name': 'user', 'password': 'your_password'})
        assert response.status_code == 200
        assert response.json['message'] == 'Login successful'
        response = test_client.post('/serie-search/admin/create_user', json={'name': 'test2', 'password': 'test2', 'role': 0})
        assert response.status_code == 403
        assert response.json['message'] == 'You do not have permission to create users'