try:
    from ORM.tables import *
    from ORM.base import Model
except ImportError:
    from tables import *
    from base import Model

def get_products():
    products = Product.query.all()
    return products

def get_product_by_id(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    return product


