from api.app import create_app
from api.models import db, Users, Series, Watched
import pytest
import os


import pytest

@pytest.fixture
def user_client_with_watched_serie():
    app = create_app()
    with app.app_context():
        user = Users.query.filter_by(name='user').first()
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
        user = Users.query.filter_by(name='user').first()
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
def test_recommandation_without_watched(user_client_without_watched_serie):
    response = user_client_without_watched_serie.get('/serie-search/recommendation')
    assert response.status_code == 200
    assert response.json['message'] == 'You have not watched anything'
    
@pytest.mark.usefixture("user_client_with_watched_serie")
def test_recommandation_with_watched_serie(user_client_with_watched_serie):
    response = user_client_with_watched_serie.get('/serie-search/recommendation')
    assert response.status_code == 200
    assert len(response.json) == 10
    
@pytest.mark.usefixture("user_client_without_watched_serie")
def test_recommandation_for_someone_who_watched_all(user_client_without_watched_serie):
    app = create_app()
    with app.app_context():
        user = Users.query.filter_by(name='user').first()
        for serie in Series.query.all():
            tmp_watched = Watched(user, serie)
            db.session.add(tmp_watched)
        db.session.commit()
    response = user_client_without_watched_serie.get('/serie-search/recommendation')
    assert response.status_code == 200
    assert response.json['message'] == 'You have watched everything'
    

@pytest.mark.usefixture("user_client_with_watched_serie")
def test_recommendation_are_different_when_not_same_series_watched(user_client_with_watched_serie):
    response = user_client_with_watched_serie.get('/serie-search/recommendation')
    user_client_with_watched_serie.post('/serie-search/watched/40')
    user_client_with_watched_serie.delete('/serie-search/watched/1')
    response2 = user_client_with_watched_serie.get('/serie-search/recommendation')
    assert response.status_code == 200
    assert len(response.json) == 10
    assert set(response.json) != set(response2.json)
    
@pytest.mark.usefixture("user_client_without_watched_serie")
def test_recommendation_size_when_user_almost_watched_all_series(user_client_without_watched_serie):
    app = create_app()
    with app.app_context():
        user = Users.query.filter_by(name='user').first()
        for serie in Series.query.all():
            tmp_watched = Watched(user, serie)
            db.session.add(tmp_watched)
        db.session.commit()
    user_client_without_watched_serie.delete('/serie-search/watched/1')
    response = user_client_without_watched_serie.get('/serie-search/recommendation')
    assert response.status_code == 200
    assert response.json == ['24']