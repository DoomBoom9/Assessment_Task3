try:
    from ORM.ORM_TEST import session
    from ORM.tables import *
    from ORM.base import Model
except ImportError:
    from ORM_TEST import session
    from tables import *
    from base import Model

def get_products():
    products = Product.query.all()
    return products


