from flask_cache import Cache
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
mail = Mail()
cache = Cache(config={'CACHE_TYPE': 'redis'})


def init_ext(app):
    db.init_app(app)
    Migrate(app,db)
    mail.init_app(app)
    cache.init_app(app)