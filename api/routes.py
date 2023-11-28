from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, current_user, logout_user
import datetime
from api.models import db, Users, Series, Watched, Role

REMEMBER_COOKIE_DURATION = datetime.timedelta(minutes=3)
api = Blueprint('api', __name__)
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Users.query.filter_by(name=data['name']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    login_user(user, remember=False, duration = REMEMBER_COOKIE_DURATION)
    return jsonify({'message': 'Login successful'}), 200
# Routes
@api.route('/admin/create_user', methods=['POST'])
@login_required
def create_user():
    if current_user.role != Role.admin:
        return jsonify({'message': 'You do not have permission to create users'}), 403

    data = request.get_json()
    new_user = Users(name=data['name'], password=data['password'], role=data['role'])
    new_user.set_password(new_user.password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User created successfully'}), 201

# Add other routes...

@api.route('/logout')
@login_required
def logout():
    if not current_user or not current_user.is_authenticated:
        return jsonify({'message': 'You are not logged in, don\'t need to logout'}), 401
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@api.route('/')
def is_ready():
    myUser = Users.query.first()
    if not myUser:
        tmp = Users('admin', None,Role.admin).set_password('admin')
        db.session.add(tmp)
        db.session.commit()
        return jsonify({'message': 'API is ready but no user has been created yet'}), 200

    return jsonify({'message': f'API is ready {myUser}'}), 200