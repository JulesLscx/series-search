from api.app import create_app
from api.models import db, Users, Series, Watched
import pytest
import os


import pytest

@pytest.fixture
def user_client_with_watched_serie():
    app = create_app()
    with app.app_context():
        user = Users.query.get('user')
        if not user:
            user = Users(name='user', password='your_password', role=0)
            db.session.add(user)
            db.session.commit()
        Watched.query.filter_by(idUser=user.name).delete()
        db.session.commit()

        watched_series = [1, 4, 7, 9, 2]  # 24, angel, bionic woman, blood ties, and 90210
        for serie_id in watched_series:
            tmp_serie = Series.query.get(serie_id)
            tmp_watched = Watched(user, tmp_serie)
            db.session.add(tmp_watched)

        db.session.commit()

    with app.test_client() as test_client:
        connect = test_client.post('/serie-search/login', json={'name': 'user', 'password': 'your_password'})
        yield test_client
        logout = test_client.get('/serie-search/logout')


@pytest.fixture
def user_client_without_watched_serie():
    app = create_app()
    with app.app_context():
        user = Users.query.get('user')
        if not user:
            user = Users(name='user', password='your_password', role=0)
            db.session.add(user)
            db.session.commit()
        Watched.query.filter_by(idUser=user.name).delete()
        db.session.commit()
    with app.test_client() as test_client:
        connect = test_client.post('/serie-search/login', json={'name': 'user', 'password': 'your_password'})
        yield test_client
        logout = test_client.get('/serie-search/logout')
        
@pytest.mark.usefixtures("user_client_without_watched_serie")
def test_watched_nothing(user_client_without_watched_serie):    
    response = user_client_without_watched_serie.get('/serie-search/watched')
    assert response.status_code == 200
    assert response.json['message'] == 'You have not watched anything'
    
@pytest.mark.usefixture("user_client_with_watched_serie")
def test_watched_something(user_client_with_watched_serie):
    response = user_client_with_watched_serie.get('/serie-search/watched')
    assert response.status_code == 200
    assert len(response.json) == 5
    
def test_get_all_series():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/serie-search/series')
        assert response.status_code == 200
        assert len(response.json) == 125
        
        
def test_get_one_existing_serie():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/serie-search/series/1')
        assert response.status_code == 200
        assert response.json['id'] ==1
        
def test_get_one_non_existing_serie():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/serie-search/series/999')
        assert response.status_code == 404
        assert response.json == {'message': 'Serie not found'}
        

@pytest.mark.usefixtures("user_client_without_watched_serie")
def test_add_watched_serie(user_client_without_watched_serie):
    response = user_client_without_watched_serie.post('/serie-search/watched/1')
    response = user_client_without_watched_serie.get('/serie-search/watched')
    assert response.status_code == 200
    assert len(response.json) == 1
    
@pytest.mark.usefixtures("user_client_with_watched_serie")
def test_add_already_watched_serie(user_client_with_watched_serie):
    response = user_client_with_watched_serie.post('/serie-search/watched/1')
    assert response.status_code == 400
    assert response.json == {'message': 'Serie already watched'}
    
@pytest.mark.usefixtures("user_client_with_watched_serie")
def test_add_non_existing_serie(user_client_with_watched_serie):
    response = user_client_with_watched_serie.post('/serie-search/watched/999')
    assert response.status_code == 404
    assert response.json == {'message': 'Serie not found'}
    
@pytest.mark.usefixtures("user_client_with_watched_serie")
def test_delete_watched_serie(user_client_with_watched_serie):
    response = user_client_with_watched_serie.delete('/serie-search/watched/1')
    response = user_client_with_watched_serie.get('/serie-search/watched')
    assert response.status_code == 200
    assert len(response.json) == 4
    
@pytest.mark.usefixtures("user_client_without_watched_serie")
def test_delete_unwatched_serie(user_client_without_watched_serie):
    response = user_client_without_watched_serie.delete('/serie-search/watched/1')
    assert response.status_code == 400
    assert response.json == {'message': 'Serie not watched'}