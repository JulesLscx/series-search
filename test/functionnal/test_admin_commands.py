from api.app import create_app
from api.models import db, Users, Role
import os

def test_create_user():
    os.environ['CONFIG_TYPE'] = 'config.TestingConfig'
    app = create_app()
    with app.test_client() as test_client:
        connect = test_client.post('/serie-search/login', json={'name': 'admin', 'password': 'your_password'})
        response = test_client.post('/serie-search/admin/create_user', json={'name': 'test2', 'password': 'test2', 'role': 0})
        assert response.status_code == 200
        assert response.json['message'] == 'User created'
        #Check if user is in db
        us = db.session.query(Users).filter_by(name='test2').first()
        assert us is not None
        assert us.name == 'test2'
        assert us.check_password('test2')
        