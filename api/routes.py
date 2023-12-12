from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, current_user, logout_user
import datetime
from api.models import db, Users, Series, Watched, Role
from es_interface.query import search as es_search
from es_interface.recommendation import recommendate
from elasticsearch import Elasticsearch
from global_var import ES_ENDPOINT, ES_USER, ES_PASSWORD

REMEMBER_COOKIE_DURATION = datetime.timedelta(minutes=3)
api = Blueprint('api', __name__)
@api.route('/login', methods=['POST'], strict_slashes=False)
def login():
    data = request.get_json()
    user = Users.query.filter_by(name=data['name']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    login_user(user, remember=False, duration = REMEMBER_COOKIE_DURATION)
    return jsonify({'message': 'Login successful'}), 200
# Routes
@api.route('/admin/user/create', methods=['POST'], strict_slashes=False)
@login_required
def create_user():
    if current_user.role != Role.ADMIN.value:
        return jsonify({'message': 'You do not have permission to create users'}), 403
    data = request.get_json()
    if not data:
        return jsonify({'message': 'Missing parameters check documentation'}), 400
    username = data.get('name')
    if not username:
        return jsonify({'message': 'Missing name'}), 400
    password = data.get('password')
    if not password:
        return jsonify({'message': 'Missing password'}), 400
    if len(password) < 2:
        return jsonify({'message': 'Password must be at least 3 characters long'}), 400
    role = data.get('role')
    if role not in Role.possible_values():
        return jsonify({'message': 'Role must be 0 for user or 1 for admin'}), 400
    if Users.query.filter_by(name=data['name']).first():
        return jsonify({'message': 'User already exists, if you want to modify password use PUT method'}), 400
    new_user = Users(name=data['name'], password=data['password'], role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

@api.route('/admin/user/delete/<string:name>', methods=['DELETE'], strict_slashes=False)
@login_required
def delete_user(name):
    if current_user.role != Role.ADMIN.value:
        return jsonify({'message': 'You do not have permission to delete users'}), 403
    user = Users.query.filter_by(name=name).first()
    if not user:
        return jsonify({'message': 'User does not exist'}), 400
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'}), 200

@api.route('/admin/user/edit/<string:name>', methods=['PUT'], strict_slashes=False)
@login_required
def edit_user(name):
    if current_user.role != Role.ADMIN.value:
        return jsonify({'message': 'You do not have permission to edit users'}), 403
    data = request.get_json()
    user = Users.query.filter_by(name=name).first()
    if not user:
        return jsonify({'message': 'User does not exist'}), 400
    if 'password' in data:
        if len(data['password']) < 2:
            return jsonify({'message': 'Password must be at least 3 characters long'}), 400
        user.set_password(data['password'])
    if 'role' in data :
        if data['role'] not in Role.possible_values():
            return jsonify({'message': 'Role must be 0 for user or 1 for admin'}), 400
        user.role = data['role']
    if not 'password' in data and not 'role' in data:
        return jsonify({'message': 'Missing parameters check documentation'}), 400
    db.session.commit()
    return jsonify({'message': 'User edited successfully'}), 200

@api.route('/logout', strict_slashes=False)
@login_required
def logout():
    if not current_user or not current_user.is_authenticated:
        return jsonify({'message': 'You are not logged in, don\'t need to logout'}), 401
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@api.route('/')
def is_ready():
    if not current_user or not current_user.is_authenticated:
        return jsonify({'message': f'API is ready'}), 200
    else:
        return jsonify({'message': f'API is ready '+ current_user.name}), 200
    

@api.route('/search/<string:query>', methods=['GET'])
def search(query):
    es = Elasticsearch([ES_ENDPOINT], basic_auth=(ES_USER, ES_PASSWORD) , verify_certs=False, ssl_show_warn=False)
    results = es_search(es,query)
    return jsonify(results), 200

@api.route('/search', methods=['GET'], strict_slashes=False)
def search_empty():
    return jsonify({'message': 'Please specify a query as /search/my%20query'}), 400

@api.route('/watched', methods=['GET'], strict_slashes=False)
@login_required
def watched():
    if not current_user or not current_user.is_authenticated:
        return jsonify({'message': 'You are not logged in'}), 401
    username = current_user.name
    watched = Watched.query.filter_by(idUser=username).all()
    if not watched:
        return jsonify({'message': 'You have not watched anything'}), 200
    series = []
    for w in watched:
        series.append(db.session.query(Series).filter_by(idSerie=w.idSerie).first().title)
    return jsonify(series), 200


@api.route('/series', methods=['GET'], strict_slashes=False)
def get_all_series():
    series = []
    for serie in db.session.query(Series).all():
        series.append({ 'id': serie.idSerie, 'title': serie.title})
    return jsonify(series), 200

@api.route('/series/<int:idSerie>', methods=['GET'])
def get_serie_name(idSerie):
    serie = db.session.query(Series).filter_by(idSerie=idSerie).first()
    if not serie:
        return jsonify({'message': 'Serie not found'}), 404
    return jsonify({'id': serie.idSerie, 'title': serie.title}), 200

@login_required
@api.route('/watched/<int:idSerie>', methods=['POST'])
def watch_serie(idSerie):
    if not current_user or not current_user.is_authenticated:
        return jsonify({'message': 'You are not logged in'}), 401
    username = current_user.name
    serie = db.session.query(Series).filter_by(idSerie=idSerie).first()
    if not serie:
        return jsonify({'message': 'Serie not found'}), 404
    if db.session.query(Watched).filter_by(idUser=username, idSerie=idSerie).first():
        return jsonify({'message': 'Serie already watched'}), 400
    new_watched = Watched(db.session.query(Users).filter_by(name=username).first(), serie)
    db.session.add(new_watched)
    db.session.commit()
    return jsonify({'message': 'Serie watched successfully'}), 201

@login_required
@api.route('/watched/<int:idSerie>', methods=['DELETE'])
def delete_watched_serie(idSerie):
    if not current_user or not current_user.is_authenticated:
        return jsonify({'message': 'You are not logged in'}), 401
    username = current_user.name
    serie = db.session.query(Series).filter_by(idSerie=idSerie).first()
    if not serie:
        return jsonify({'message': 'Serie not found'}), 404
    watched = db.session.query(Watched).filter_by(idUser=username, idSerie=idSerie).first()
    if not watched:
        return jsonify({'message': 'Serie not watched'}), 400
    db.session.delete(watched)
    db.session.commit()
    return jsonify({'message': 'Serie deleted successfully'}), 200


@login_required
@api.route('/recommendation', methods=['GET'], strict_slashes=False)
def get_recommendation():
    if not current_user or not current_user.is_authenticated:
        return jsonify({'message': 'You are not logged in'}), 401
    username = current_user.name
    watched = Watched.query.filter_by(idUser=username).all()
    if not watched:
        return jsonify({'message': 'You have not watched anything'}), 200
    series = []
    for w in watched:
        series.append(db.session.query(Series).filter_by(idSerie=w.idSerie).first().title)
    if len(series) == Series.query.count():
        return jsonify({'message': 'You have watched everything'}), 200
    es = Elasticsearch([ES_ENDPOINT], basic_auth=(ES_USER, ES_PASSWORD) , verify_certs=False, ssl_show_warn=False)
    results = recommendate(es, series)
    return jsonify(results), 200