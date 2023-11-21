from flask import Blueprint, request, jsonify
from flask_login import login_user, login_required, current_user, logout_user

from models import db, Users, Series, Watched, Role

api = Blueprint('api', __name__)
@api.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = Users.query.filter_by(name=data['name']).first()
    if not user or not user.check_password(data['password']):
        return jsonify({'message': 'Invalid credentials'}), 401

    login_user(user)
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
    logout_user()
    return jsonify({'message': 'Logout successful'}), 200

@api.route('/')
def is_ready():
    return jsonify({'message': 'API is ready'}), 200