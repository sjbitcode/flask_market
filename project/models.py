from project.db import db


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)


class OrderedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    last_modified = db.Column(db.DateTime)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float(precision=2), primary_key=True)
    date = db.Column(db.DateTime)
