from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class Role:
    admin = 1
    user = 0

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(100), nullable=False)
    role = db.Column(db.String(10), nullable=False, default=Role.user)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class Series(db.Model):
    idSerie = db.Column(db.Integer, primary_key=True, )
    title = db.Column(db.String(50), nullable=False)

class Watched(db.Model):
    idUser = db.Column(db.Integer, db.ForeignKey('users.name'), primary_key=True)
    idSerie = db.Column(db.Integer, db.ForeignKey('series.idSerie'), primary_key=True)
