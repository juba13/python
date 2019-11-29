from os import path
from flask import Flask ,render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager 
from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
basedir = path.abspath(path.dirname(__file__))



db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)

    app.config['SECRET_KEY'] = '9OLWxND4o83j4K4iuopO'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + path.join(basedir, 'db.sqlite')

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    # migrate = Migrate(app, db)
    # manager = Manager(app)
    # manager.add_command('db', MigrateCommand)


    from app.model.user_model import User

    @login_manager.user_loader
    def load_user(user_id):
        user=User.query.get(int(user_id))
        if(not user and User.getSuperAdmin().id==int(user_id)):
            user=User.getSuperAdmin()
        return user

    from app.controller.auth_controller import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.controller.home_controller import home as home_blueprint
    app.register_blueprint(home_blueprint)

    from app.controller.user_controller import user as user_blueprint
    app.register_blueprint(user_blueprint)


    @app.errorhandler(403)
    def forbidden(error):
        return render_template('errors/403.html', title='Forbidden'), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', title='Page Not Found'), 404

    @app.errorhandler(500)
    def internal_server_error(error):
        return render_template('errors/500.html', title='Server Error'), 500


    return app
