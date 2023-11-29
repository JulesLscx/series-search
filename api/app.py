from flask import Flask
from flask_login import LoginManager
from api.models import db, Users, Role
from api.routes import api



def create_admin(app):
    with app.app_context():
        db.create_all()
        if not Users.query.first():
            tmp = Users('admin', 'your_password',Role.ADMIN.value)
            db.session.add(tmp)
            db.session.commit()
        else:
            raise Exception("Admin already created")
        
def create_user(app):
    with app.app_context():
        if not Users.query.filter_by(name='user').first():
            tmp = Users('user', 'your_password',Role.USER.value)
            db.session.add(tmp)
            db.session.commit()
        else:
            raise Exception("User already created")

def create_app():
    app = Flask(__name__)
    # app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SECRET_KEY'] = "your_secret_key"
    app.register_blueprint(api, url_prefix='/serie-search')
    db.init_app(app)
    login_manager = LoginManager(app)
    @login_manager.user_loader
    def load_users(Users_id):
        return Users.query.get(Users_id)
    try : 
        create_admin(app)
    except Exception as e:
        print(e)
    try :
        create_user(app)
    except Exception as e:
        print(e)
    return app
