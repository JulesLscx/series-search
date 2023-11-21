from flask import Flask
from flask_login import LoginManager

from models import db, Users
from routes import api

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
