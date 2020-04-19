# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy

from project import create_app

app = create_app()
# app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///market.sqlite3'
# db = SQLAlchemy(app)


# class Product(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     price = db.Column(db.Float(precision=2), nullable=False)


# class OrderedItem(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     qty = db.Column(db.Integer, nullable=False)
#     price = db.Column(db.Float(precision=2), nullable=False)
#     last_modified = db.Column(db.DateTime)
#     order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)


# class Order(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     total = db.Column(db.Float(precision=2), primary_key=True)
#     date = db.Column(db.DateTime)


# @app.route('/')
# def hello_world():
#     return 'Hello World! Howdy World! Greeting Bods Promods Quotes'


if __name__ == '__main__':
    # db.create_all()
    app.run('0.0.0.0', 8000, True)
