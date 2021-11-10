from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import json

app = Flask(__name__)

with open('security.json', 'r') as f:
    data = json.load(f)
    DB_URL = data['DB_URL']
    DB_USER = data['DB_USER']
    DB_PSW = data['DB_PSW']

app.config['SQLALCHEMY_DATABASE_URI'] = f"{DB_URL}{DB_USER}:{DB_PSW}@127.0.0.1:5432/nora"
print(app.config['SQLALCHEMY_DATABASE_URI'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
ma = Marshmallow(app)

class Business(db.Model):
    bid = db.Column(db.String(80), primary_key=True)
    b_name = db.Column(db.String(80), nullable=False)
    url = db.Column(db.String(80))
    rating = db.Column(db.Numeric)
    addr = db.Column(db.String(80))
    phone = db.Column(db.String(80))

    def __init__(self, bid, b_name, url, rating, addr, phone):
        self.bid = bid
        self.b_name = b_name
        self.url = url
        self.rating = rating
        self.addr = addr
        self.phone = phone



class Business_Schema(ma.Schema):
    class meta:
        # model = Business
        bid = ma.auto_field()
        b_name = ma.auto_field()
        url = ma.auto_field()
        rating = ma.auto_field()
        addr = ma.auto_field()
        phone = ma.auto_field()

business = Business_Schema(many=True)

@app.route('/', methods=['GET'])
def index():
    data = Business.query.all()
    result = business.dump(data)
    return jsonify(result)


if __name__ == '__main__':
    app.run(debug=True)
