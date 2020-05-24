import datetime

from project import db
from project.models import Product, Order, OrderedItem


# Adding products
p1 = Product(name='Backpack', price=10.12)
p2 = Product(name='Notebooks - 3 pack', price=9.99)
p3 = Product(name='Men Socks', price=12.00)
p4 = Product(name='Vegan Toona - 6 pack', price=18.00)
p5 = Product(name='Hippeas White Cheddar', price=20.00)
p6 = Product(name='Complete Cookie - 4 flavors 16 pack', price=15.00)
p7 = Product(name='Chocolate Brownie Cliff Bar', price=10.00)
p8 = Product(name='Spicy Ramen Noodles', price=20.00)
db.session.add_all([p1, p2, p3, p4, p5, p6, p7, p8])

#Adding Orders
o1 = Order(total=18.00)
o2 = Order(total=64.00)
o3 = Order(total=15.00)
o4 = Order(total=50.00)
o5 = Order(total=10.12)
db.session.add_all([o1, o2, o3, o4, o5])

# Adding Ordered Items
oi1 = OrderedItem(qty=1, price=10.12, product_id=1)
oi2 = OrderedItem(qty=3, price=9.99, product_id=2)
oi3 = OrderedItem(qty=1, price=18.00, product_id=4, order_id=1)
oi4 = OrderedItem(qty=2, price=20.00, product_id=5, order_id=2)
oi5 = OrderedItem(qty=2, price=12.00, product_id=3, order_id=2)
oi6 = OrderedItem(qty=1, price=15.00, product_id=6, order_id=3)
oi7 = OrderedItem(qty=2, price=10.00, product_id=7, order_id=4)
oi8 = OrderedItem(qty=1, price=20.00, product_id=8, order_id=4)
oi9 = OrderedItem(qty=1, price=10.00, product_id=7)
oi10 = OrderedItem(qty=1, price=10.12, product_id=1, order_id=5)
db.session.add_all([oi1, oi2, oi3, oi4, oi5, oi6, oi7, oi8, oi9, oi10])


db.session.commit()
