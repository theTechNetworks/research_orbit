from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager,AnonymousUserMixin,current_user
from .anonymous_user import AnonymousUser


#setting up database
db = SQLAlchemy()
DB_Name ='database.db'

def create_app():

    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'ray'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_Name}'
    db.init_app(app)

    #registering views
    from .views import views
    from .auth import auth

    app.register_blueprint(views,url_prefix='/')
    app.register_blueprint(auth,url_prefix='/')

    #creating database
    from .models import User,Papers
    create_database(app)

    

    # Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @app.context_processor
    def inject_user():
        try:
            return dict(user=current_user if current_user.is_authenticated else AnonymousUser())
        except Exception as e:
            print(f"Error in context processor: {e}")
            return dict(user=AnonymousUser())
        
    #how to log in users
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    

    return app


#check if database exists before creating it
def create_database(app):
    if not path.exists('website/'+ DB_Name):
        with app.app_context():
            db.create_all()
        print('Database created')
    else:
        print('Database Exists already')