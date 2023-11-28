from flask import Flask
from flask_login import LoginManager

from api.models import db, Users, Role
from api.routes import api

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SECRET_KEY'] = "your_secret_key"
app.register_blueprint(api, url_prefix='/serie-search')

db.init_app(app)
login_manager = LoginManager(app)

@login_manager.user_loader
def load_users(Users_id):
    return Users.query.get(Users_id)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()

    app.run(debug=True)
def run_api():
    #Create sqlite database
    with app.app_context():
        db.create_all()
        existing_user = Users.query.filter_by(name='admin').first()
        if existing_user:
            print("User already exists")
        else : 
            admin_user = Users(name='admin', password='your_password', role=Role.ADMIN.value)
            admin_user.set_password(admin_user.password)
            # Add the user to the database
            db.session.add(admin_user)
            db.session.commit()
    app.run(debug=True)
    #Print the users table