import os
from flask import Flask




def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    #create testing message server
    app.config['MAIL_SERVER'] = 'localhost'  # <----For tests
    app.config['MAIL_PORT'] = 8025
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    if test_config is None:
        app.config.from_pyfile('config.py', silent=True)
    else:
        app.config.from_mapping(test_config)

    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #For testing
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    #register DB init command
    from . import db
    db.init_app(app)

    #register auth app
    from . import auth
    app.register_blueprint(auth.bp)

    #register main app
    from . import main
    app.register_blueprint(main.bp)
    app.add_url_rule('/', endpoint='index')
    app.add_url_rule('/search', endpoint='search')
    app.add_url_rule('/confirm/<int:id>/action', endpoint='confirm')
    app.add_url_rule('/add-friend/<int:id>', endpoint='add-friend')

    return app