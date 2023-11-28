from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from enum import Enum
db = SQLAlchemy()

class Role(Enum):
    USER = 0
    ADMIN = 1

    def __str__(self) -> str:
        return self.name

    @classmethod
    def from_value(cls, value: int) -> str:
        if value == 0:
            return Role.USER
        elif value == 1:
            return Role.ADMIN

    def to_value(self) -> int:
        return self.value

class Users(UserMixin, db.Model):
    __tablename__ = 'users'
    name = db.Column(db.String(50), primary_key=True)
    password = db.Column(db.String(256), nullable=False)
    role = db.Column(db.Integer, nullable=False, default=Role.USER.value)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)
    def get_id(self):
        return self.name
    
    def __repr__(self):
        if self.role == Role.ADMIN.value:
            intitule = "Admin"
        else:
            intitule = "User"
        return f"<User {self.name}> <Role {intitule}>"
    

class Series(db.Model):
    idSerie = db.Column(db.Integer, primary_key=True, )
    title = db.Column(db.String(50), nullable=False)

class Watched(db.Model):
    idUser = db.Column(db.Integer, db.ForeignKey('users.name'), primary_key=True)
    idSerie = db.Column(db.Integer, db.ForeignKey('series.idSerie'), primary_key=True)
