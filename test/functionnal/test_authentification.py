from api.app import create_app
import os

def test_test_env():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get('/serie-search/')
        assert response.status_code == 200
        assert response.json['message'] == 'API is ready'
def test_authentification_good_password():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.post('/serie-search/login', json={'name': 'admin', 'password': 'your_password'})
        assert response.status_code == 200
        assert response.json['message'] == 'Login successful'
def test_authentification_wrong_password():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.post('/serie-search/login', json={'name': 'admin', 'password': 'wrong_password'})
        assert response.status_code == 401
        assert response.json['message'] == 'Invalid credentials'
def test_authentification_wrong_username():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.post('/serie-search/login', json={'name': 'wrong_username', 'password': 'your_password'})
        assert response.status_code == 401
        assert response.json['message'] == 'Invalid credentials'
def test_authentification_logout():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.post('/serie-search/login', json={'name': 'admin', 'password': 'your_password'})
        assert response.status_code == 200
        assert response.json['message'] == 'Login successful'
        response = test_client.get('/serie-search/')
        assert response.status_code == 200
        assert response.json['message'] == 'API is ready admin'
        response = test_client.get('/serie-search/logout')
        assert response.status_code == 200
        assert response.json['message'] == 'Logout successful'