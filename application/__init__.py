from os import path, makedirs
from flask import Flask


def get_app(config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='1401-0-0sfoefs)sdf12~`',
        # store the database in the instance folder
        DATABASE=path.join(app.instance_path, 'pim.sqlite'),
    )
    if config:
        # load the config if passed in
        app.config.update(config)

    # ensure the instance folder exists
    try:
        makedirs(app.instance_path)
    except OSError:
        pass

    # register the database commands
    from . import persistence
    persistence.init(app)

    # blueprints, routes
    from . import endpoints
    app.register_blueprint(endpoints.bp)

    return app
