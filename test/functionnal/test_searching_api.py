from api.app import create_app
import os
def test_empty_search():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get('/serie-search/search/')
        assert response.status_code == 400
        assert response.json['message'] == 'Please specify a query as /search/my%20query'

def test_search():
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get('/serie-search/search/lost')
        assert response.status_code == 200
        assert response.json['1'] == 'lost'

def test_search_with_space():
    app = create_app()
    with app.test_client() as test_client:
        response = test_client.get('/serie-search/search/breaking%20bad')
        assert response.status_code == 200
        assert response.json['1'] == 'breakingbad'