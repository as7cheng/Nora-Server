"""
File to create and start the flask app
"""

import json
from flask import Flask, jsonify, request
from initapp import CORS, DB, MIGR, MA
from model import BusinessSchema, Business

APP = Flask(__name__)

# Open the file contains DB info
with open('security.json', 'rb') as f:
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
    request_args = request.args.to_dict(flat=False)
    print(request_args)
    # First, pick out the term and city parameters
    args = {k : v for k, v in request_args.items() if k in ['term', 'city']}
    print(args)
    # Then, prune the parameter lists -> remove all empty strings
    if 'term' in args:
        args['term'] = list(filter(None, args['term']))
        print(args['term'])
        if args['term'] == []:
            del args['term']
    if 'city' in args:
        args['city'] = list(filter(None, args['city']))
        print(args['city'])
        if args['city'] == []:
            del args['city']
    # Now, deal with the args
    if 'city' in args and 'term' in args:
        cities = [capitalize_first(city) for city in args['city']]
        terms = [capitalize_first(term) for term in args['term']]
        res = BUSINESS.dump(Business.query.filter(
            Business.metropolitan.in_(cities),
            Business.term.in_(terms)))
    elif 'city' in args:
        cities = [capitalize_first(city) for city in args['city']]
        res = BUSINESS.dump(Business.query.filter(
            Business.metropolitan.in_(cities)))
    elif 'term' in args:
        terms = [capitalize_first(term) for term in args['term']]
        res = BUSINESS.dump(Business.query.filter(
            Business.term.in_(terms)))
    else:
        res = BUSINESS.dump(Business.query.all())
    print(len(res))
    return jsonify(res)


@APP.route('/top', methods=['GET'])
def top():
    """
    Function to haddle query with parameter term, return the top 3
    metropolitans with heighest average rating on parameter term.
    """
    term = request.args.get('term')
    print(term)
    if term is None or term == '':
        return jsonify([])
    term = capitalize_first(term)
    print(term)
    syntax = (
        f"select metropolitan, state, round(avg(rating), 2) as "
        f"score FROM business where '{term}'=term "
        f"group by metropolitan, state order by score desc limit 3;"
    )
    result = DB.session.execute(syntax)
    res = [serialize_message(data, 'metropolitan') for data in result]
    print(type(jsonify(res)))
    return jsonify(res)


@APP.route('/rank', methods=['GET'])
def rank():
    """
    Function to return the ranking queried by term
    """
    term = request.args.get('term')
    if term is None or term == '':
        return jsonify([])
    term = capitalize_first(term)
    syntax = (
        f"select city, state, round (city_population / count(*), 0) "
        f"as score from business where term='{term}' group by city, "
        f"state, city_population order by score limit 5;"

    )
    result = DB.session.execute(syntax)
    res = [serialize_message(data, 'city') for data in result]
    return jsonify(res)


def serialize_message(data, key):
    """
    Helper function to serialize query object
    """
    if key == 'metropolitan':
        return {
            "metropolitan": data.metropolitan,
            "state": data.state,
            "score": data.score
        }
    if key == 'city':
        return {
            "city": data.city,
            "state": data.state,
            "score": data.score
        }
    return {}

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
