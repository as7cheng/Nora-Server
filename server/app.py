"""
File to create and start the flask app
"""

import json
from flask import Flask, jsonify, request
from initapp import CORS, DB, MIGR, MA
from model import BusinessSchema, Business

APP = Flask(__name__)

# Open the file contains DB info
with open('security.json', 'r') as f:
    DATA = json.load(f)
    DB_URL = DATA['DB_URL']
    DB_PORT = DATA['DB_PORT']
    DB_NAME = DATA['DB_NAME']
    DB_USER = DATA['DB_USER']
    DB_PSW = DATA['DB_PSW']

# Iinitialization the flask app
SQL_URL = f"postgresql://{DB_USER}:{DB_PSW}@{DB_URL}:{DB_PORT}/{DB_NAME}"
APP.config['SQLALCHEMY_DATABASE_URI'] = SQL_URL
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
CORS.init_app(APP)
DB.init_app(APP)
MA.init_app(APP)
MIGR.init_app(APP, DB)

# Create the db
with APP.app_context():
    DB.create_all()

BUSINESS = BusinessSchema(many=True)

@APP.route('/', methods=['GET'])
def index():
    """
    Path of homepage
    """
    res = BUSINESS.dump(Business.query.all())
    return jsonify(res)

@APP.route('/dev', methods=['GET'])
def dev():
    """
    Function to haddle query with parameters
    """
    city = request.args.get('city')
    res = BUSINESS.dump(Business.query.filter_by(city=city))
    return jsonify(res)


@APP.route('/test', methods=['GET'])
def test():
    """
    Function to test
    """
    res = BUSINESS.dump(Business.query.with_entities(Business.id))
    return jsonify(res)

if __name__ == '__main__':
    APP.run(debug=True, host='0.0.0.0', port=8765)
