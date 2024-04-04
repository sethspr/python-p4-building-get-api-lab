#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = Bakery.query.all()

    all_bakeries = []
    for bakes in bakeries:
        all_bakeries.append(bakes.to_dict())
    return all_bakeries, 200

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    if bakery == None:
        return {'error': 'Bakery does not exist in db'}, 404
    
    return bakery.to_dict(), 200        

@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    pricing = BakedGood.query.order_by(BakedGood.price.desc()).all()

    bakery_prices = []
    for prices in pricing:
        bakery_prices.append(prices.to_dict())
    return bakery_prices, 200


@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    pricing = BakedGood.query.order_by(BakedGood.price.desc()).limit(1).first()

    return pricing.to_dict(), 200

if __name__ == '__main__':
    app.run(port=5555, debug=True)
