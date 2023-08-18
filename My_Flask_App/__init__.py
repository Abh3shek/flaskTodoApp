from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()

def createApp():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "sskfhslkdf sdfjsdfsf"
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ToDoDatabase.db'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix="/")
    app.register_blueprint(auth, url_prefix="/")

    from .models import User, Note

    createDatabase(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.signin'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def createDatabase(app):
    if not path.exists('My_Flask_App/ToDoDatabase.db'):
        with app.app_context():
            db.create_all()
        print('Database Created!')