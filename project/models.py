import datetime

from project import db


class Product(db.Model):
    __table_args__ = (
        db.UniqueConstraint('name', 'price', name='unique_name_price'),
    )
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    ordered_items = db.relationship('OrderedItem')

    def __repr__(self):
        return f'<Product {self.id} - {self.name} @ {self.price}>'


class OrderedItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    qty = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Float(precision=2), nullable=False)
    last_modified = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=True)

    def __repr__(self):
        return f'<OrderedItem {self.id} - qty {self.qty} @ product {self.product_id}>'


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    total = db.Column(db.Float(precision=2))
    date = db.Column(db.DateTime, nullable=False, default=datetime.datetime.utcnow)
    items = db.relationship('OrderedItem', backref='order', lazy=True)

    def __repr__(self):
        return f'<Order {self.id} - total {self.total}>'
