"""
File to create and start the flask app
"""

import json
from flask import Flask, jsonify
from initapp import cors, db, mars, migr
from model import BusinessSchema, Business

app = Flask(__name__)

# Open the file contains DB info
with open('security.json', 'r') as f:
    DATA = json.load(f)
    DB_URL = DATA['DB_URL']
    DB_USER = DATA['DB_USER']
    DB_PSW = DATA['DB_PSW']

# Iinitialization the flask app
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{DB_USER}:{DB_PSW}@{DB_URL}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
cors.init_app(app)
db.init_app(app)
mars.init_app(app)
migr.init_app(app, db)

# Create the db
with app.app_context():
    db.create_all()

BUSINESS = BusinessSchema(many=True)

@app.route('/', methods=['GET'])
def index():
    """
    Path of homepage
    """
    res = BUSINESS.dump(Business.query.all())
    return jsonify(res)

@app.route('/test', methods=['GET'])
def test():
    res = BUSINESS.dump(Business.query.with_entities(Business.bid))
    return jsonify(res)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port='8765')
