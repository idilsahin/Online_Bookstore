from flask import Flask
from os import path
from flask_login import LoginManager
from .Utils.config import Config
from .Utils.database import db
from .models.user_model import User
DB_NAME = "onlinebookstore.db"

def create_app():
    try:
        app = Flask(__name__)
        app.config.from_object(Config)
        db.init_app(app)

        from .auth import auth
        from .routes import routes
        from .controllers.bookcontroller import bookcontroller
        from .controllers.ordercontroller import ordercontroller
        from .controllers.wishlistcontroller import wishlistcontroller
        from .controllers.cardcontroller import cardcontroller
        from .controllers.usercontroller import usercontroller

        #app.register_blueprint(noteviews, url_prefix='/')
        app.register_blueprint(auth, url_prefix='/')
        app.register_blueprint(routes, url_prefix='/')
        app.register_blueprint(bookcontroller, url_prefix='/')
        app.register_blueprint(ordercontroller, url_prefix='/')
        app.register_blueprint(wishlistcontroller, url_prefix='/')
        app.register_blueprint(cardcontroller, url_prefix='/')
        app.register_blueprint(usercontroller, url_prefix='/')

        with app.app_context():
            db.create_all()
        
        login_manager = LoginManager()
        login_manager.login_view = 'auth.login'
        login_manager.init_app(app)

        @login_manager.user_loader
        def load_user(id):
            return User.query.get(int(id))
        

        return app
    except ValueError as ve:
        return "There is an errorrrrr"
# Create the Flask app instance
app = create_app()

def create_database(app):
    if not path.exists('onlinebookstore/' + DB_NAME):
        db.create_all(app=app)
        print('Created Database!')