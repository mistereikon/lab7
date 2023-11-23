# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_bootstrap import Bootstrap

db = SQLAlchemy()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('D:/University/Web-Python/lab7/config.py')
    db.init_app(app)
    login_manager.init_app(app)

    from .views import bp as main_blueprint
    app.register_blueprint(main_blueprint)

    with app.app_context():
        db.create_all()

    bootstrap = Bootstrap(app)

    return app

@login_manager.user_loader
def load_user(user_id):
    from .models import User 
    return User.query.get(int(user_id))

app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
