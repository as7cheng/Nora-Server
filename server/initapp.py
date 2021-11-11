"""
File to initialize all things needde by the app
"""

from flask_cors import CORS
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

CORS = CORS()
DB = SQLAlchemy()
MIGR = Migrate()
MA = Marshmallow()
