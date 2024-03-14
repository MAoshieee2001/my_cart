from builtins import sum
from datetime import datetime


class Cart:
    def __init__(self, session):
        self.session = session
        cart_data = self.session.get('cart', {})
        self.subtotal = cart_data.get('subtotal', 0.00)
        self.iva = cart_data.get('iva', 0.00)
        self.total = cart_data.get('tottal', 0.00)
        self.products = cart_data.get('products', [])
        print(cart_data)

    def insert_item(self, instance):
        if any(instance['id'] in product.values() for product in self.products):
            for product in self.products:
                if instance['id'] in product.values():
                    product['quantity'] += 1
                    break
            self.calcule_invoice()
            self.save_item_session()
        else:
            self.products.append(instance)
            self.calcule_invoice()
            self.save_item_session()

    def save_item_session(self):
        cart = {
            'subtotal': self.subtotal,
            'iva': self.iva,
            'total': self.total,
            'products': self.products,
        }
        self.session['cart'] = cart
        self.session.modified = True

    def calcule_invoice(self):
        for product in self.products:
            product['subtotal'] = product['quantity'] * product['pvp']
        self.subtotal = sum(product['subtotal'] for product in self.products)
        self.iva = 0.19
        self.total = self.subtotal + (self.subtotal * self.iva)
