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
    return "Welcom to Nora's restaurants recommendation"


@APP.route('/sample', methods=['GET'])
def sample():
    """
    Function to return basic quries filter by cusine and/or city
    """
    args = request.args.to_dict(flat=False)

    if 'city' in args and 'term' in args:
        cities = [capitalize_first(city) for city in args['city']]
        terms = [capitalize_first(term) for term in args['term']]
        res = BUSINESS.dump(Business.query.filter(
            Business.city.in_(cities),
            Business.term.in_(terms)))
    elif 'city' in args:
        cities = [capitalize_first(city) for city in args['city']]
        res = BUSINESS.dump(Business.query.filter(
            Business.city.in_(cities)))
    elif 'term' in args:
        terms = [capitalize_first(term) for term in args['term']]
        res = BUSINESS.dump(Business.query.filter(
            Business.term.in_(terms)))
    else:
        res = BUSINESS.dump(Business.query.all())
    return jsonify(res)


@APP.route('/top', methods=['GET'])
def top() -> list:
    """
    Function to haddle query with parameters
    """
    term = request.args.get('term')
    print(term)
    term = capitalize_first(term)
    print(term)
    syntax = (
        f"select city, state, round(avg(rating), 2) as "
        f"score FROM business where '{term}'=term "
        f"group by city, state order by score desc limit 3;"
    )
    result = DB.session.execute(syntax)
    res = [serialize_message(data) for data in result]
    return jsonify(res)


@APP.route('/rank', methods=['GET'])
def rank() -> list:
    """
    Function to return the ranking quied by term
    """
    term = request.args.get('term')
    term = capitalize_first(term)
    syntax = (
        f"select city, state, (count(*)/city_population * 1000) "
        f"as score from business where term='{term}' group by city, "
        f"state, city_population order by score desc;"

    )
    result = DB.session.execute(syntax)
    res = [serialize_message(data) for data in result]
    return jsonify(res)


def serialize_message(data) -> json:
    """
    Helper function to serialize query object
    """
    return {
        "city": data.city,
        "state": data.state,
        "score": data.score
    }


def capitalize_first(words):
    """
    Helper function to capitalize the first letter for each word
    """
    word_list = [i[0].upper() + i[1:] for i in words.split(' ')]
    return ' '.join(word_list)


@APP.route('/test', methods=['GET'])
def test():
    """
    Function to test
    """
    city = request.args.get('city')
    print(city)
    city = capitalize_first(city)
    print(city)
    res = BUSINESS.dump(Business.query.filter_by(city=city))
    return jsonify(res)


if __name__ == '__main__':
    APP.run(debug=True, host='0.0.0.0', port=8765)
