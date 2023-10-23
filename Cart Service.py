import requests
import os
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'products.sqlite')
db = SQLAlchemy(app)

url = "https://product-service-l24r.onrender.com"

class Cart(db.Model):
    id          = db.Column(db.Integer, primary_key = True)
    user_id     = db.Column(db.String(50))
    product_id  = db.Column(db.Integer)
    quantity    = db.Column(db.Integer)

def get_product(product_id):
    response = requests.get(f'{url}/products/{product_id}')
    data = response.json()
    return data


@app.route("/cart/<int:user_id>", methods = ['GET'])
def get_shopping_cart(user_id):
    cart = Cart.query.filter_by(user_id = user_id).all()
    result =[]
    for products in cart:
      item = get_product(products.product_id)

    result.append({
            'product_name': item['name'],
            'quantity': products.quantity,
            'total_price': item['price'] * products.quantity
    })
    return jsonify(result)



@app.route("/cart/<int:user_id>/add/<int:product_id>", methods = ['GET'])
def add_product(user_id, product_id):

    cart_product = Cart(user_id = user_id, product_id = product_id, quantity = 1)

    db.session.add(cart_product)
    db.session.commit()

    return jsonify({"message": f"Product id: {product_id} was added to the Cart"}), 201
    

@app.route('/cart/<user_id>/remove/<int:product_id>', methods = ['POST'])
def remove_from_cart(user_id, product_id):
    # QUANTITY IS 1 FOR SIMPLICITY: 
    item = Cart.query.filter_by(user_id = user_id, product_id = product_id).first_or_404()
    if item.quantity > 1:
        item.quantity -= 1
        db.session.commit()
    else:
        db.session.delete(cart_item)
        db.session.commit()
    return jsonify({"message": f"product id#: {product_id} was removed from the cart !"}), 200

if __name__ == '__main__':
    app.run(port = 3000, debug = True)