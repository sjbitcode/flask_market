import sqlalchemy
from flask import Blueprint, request, jsonify, url_for, redirect
from project import db
from project.models import Product, Order, OrderedItem

main_blueprint = Blueprint('main', __name__)


@main_blueprint.route('/')
def hello_world():
    return 'Hello World!'


@main_blueprint.route('/products', methods=['GET', 'POST'])
def all_products():
    if request.method == 'GET':
        products = Product.query.all()
        data = []
        for product in products:
            product_obj = {}
            product_obj['id'] = product.id
            product_obj['name'] = product.name
            product_obj['price'] = product.price
            data.append(product_obj)
        return jsonify(data)

    elif request.method == 'POST':
        name = request.form['name']
        price = float(request.form['price'])
        product = Product(name=name, price=price)

        try:
            db.session.add(product)
            db.session.commit()
            added_product = Product.query.filter_by(name=name).first()
            return jsonify({
                'id': added_product.id,
                'name': added_product.name,
                'price': added_product.price
            }), 201
        except sqlalchemy.exc.IntegrityError as e:
            print(e)
            return 'Product already exists', 400
        except Exception:
            return 'An error occured', 400


@main_blueprint.route('/product/<int:product_id>', methods=['GET', 'PUT', 'DELETE'])
def single_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return f'No product with id {product_id}', 400

    if request.method == 'GET':
        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price
        })

    elif request.method == 'PUT':
        name = request.form.get('name')
        price = request.form.get('price')

        product.name = name if name else product.name
        product.price = price if price else product.price
        db.session.add(product)
        db.session.commit()

        # Update cart if product exists in the cart.
        if price:
            cart_item = OrderedItem.query.filter_by(product_id=product_id, order_id=None).first()
            if cart_item:
                cart_item.price = price
                db.session.add(cart_item)
                db.session.commit()

        return jsonify({
            'id': product.id,
            'name': product.name,
            'price': product.price
        }), 200

    elif request.method == 'DELETE':

        # Delete cart items if order_id is None, else set product_id to None
        cart_items = OrderedItem.query.filter_by(product_id=product_id).all()
        unchecked = list(filter(lambda x: x.order_id is None, cart_items))
        checked_out = list(filter(lambda x: x.order_id is not None, cart_items))

        print(f'CART ITEMS AFFECTED BY PRODUCT TO BE DELETED {cart_items}')
        db.session.delete(unchecked[0])  # delete item in cart
        for item in checked_out:         # set product id to null for already checked out items
            item.product_id = None

        db.session.delete(product)
        db.session.commit()
        return f'Deleted product {product_id}', 204


@main_blueprint.route('/cart', methods=['GET', 'POST'])
def cart_detail():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        qty = int(request.form.get('qty'))

        # Check for bad request
        if not all([product_id, qty]):
            return 'Must submit a product_id and qty'

        price = Product.query.get(product_id).price

        # only create new cart item if it doesn't exist, else update existing one.
        if not OrderedItem.query.filter_by(product_id=product_id, order_id=None).all():
            item = OrderedItem(qty=qty, price=price, product_id=product_id)
            db.session.add(item)
        else:
            # item = OrderedItem.query.filter_by(product_id=product_id, order_id=None).first()
            # item.qty += qty
            return f'Cart item already exists for product id {product_id}. Please use PUT method to update it.', 400

        db.session.commit()

        return 'Cart item added', 201

    elif request.method == 'GET':
        cart_items = OrderedItem.query.filter_by(order_id=None).all()
        data = []
        for item in cart_items:
            print(item.product_id)
            data.append({
                'id': item.id,
                'qty': item.qty,
                'price': item.price,
                'modified': item.last_modified,
                'product_id': item.product_id,
                'product': Product.query.get(item.product_id).name
                # 'order_id': item.order_id
            })
        return jsonify(data)


@main_blueprint.route('/cart/<int:item_id>', methods=['PUT', 'DELETE'])
def cart_item(item_id):
    # item = OrderedItem.query.get(item_id)
    ordered_product = OrderedItem.query.filter_by(product_id=item_id, order_id=None).first()
    if not ordered_product:
        return f'No cart item with id {item_id}'

    if request.method == 'PUT':
        qty = int(request.form.get('qty'))

        # Delete cart item if quantity is 0
        if qty <= 0:
            print('Qty is less than or equal to 0, will delete')
            db.session.delete(ordered_product)
            db.session.commit()
            return f'Deleted cart item with product id {item_id}', 204
        else:
            ordered_product.qty = qty
            db.session.add(ordered_product)
            db.session.commit()
            updated_item = OrderedItem.query.filter_by(product_id=item_id, order_id=None).first()
            return jsonify({
                'id': updated_item.id,
                'qty': updated_item.qty,
                'price': updated_item.price,
                'modified': updated_item.last_modified,
                'product_id': updated_item.product_id,
                'product': Product.query.get(updated_item.product_id).name
            })
    elif request.method == 'DELETE':
        db.session.delete(item)
        db.session.commit()
        return f'Deleted cart item {item_id}', 204


@main_blueprint.route('/checkout', methods=['POST'])
def checkout():
    cart_items = OrderedItem.query.filter_by(order_id=None).all()

    if not cart_items:
        return f'No items in cart'

    get_total_query = (
        "SELECT SUM(p.price*o.qty) as total "
        "FROM ordered_item o "
        "INNER JOIN product p "
        "WHERE p.id = o.product_id and o.order_id is NULL;"
    )
    result = db.engine.execute(get_total_query)
    total = float("{:.2f}".format(result.fetchone()[0]))

    order = Order(total=total)
    db.session.add(order)
    db.session.commit()

    # Set order id on cart items, so they're no longer 'in cart'
    for item in cart_items:
        item.order_id = order.id
    db.session.commit()

    return jsonify({
        'order_id': order.id,
        'total': order.total
    })


@main_blueprint.route('/orders', methods=['GET'])
def all_orders():
    orders = Order.query.all()

    if not orders:
        return 'no orders'

    orders_info = {}  # object to return

    get_order_cart_mapping = (
        'select "order".id as order_id, group_concat(ordered_item.id) as cart_item_ids '
        'from "order" '
        'inner join ordered_item '
        'where "order".id = ordered_item.order_id '
        'group by order_id '
        'order by order_id;'
    )
    results = db.engine.execute(get_order_cart_mapping)

    # Key is order id, value is {'cart ids': <str>}
    for row in results:
        orders_info[row[0]] = {
            'cart ids': row[1]
        }

    # Iterate over order objects, add in total/time values in dict
    for order in orders:
        order_entry = orders_info[order.id]
        order_entry['total'] = f"{order.total:.2f}"
        order_entry['time'] = order.date

    return jsonify(orders_info)
