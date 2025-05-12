from sqlalchemy import Column, Integer, String, ForeignKey, REAL, DateTime
from sqlalchemy.orm import Relationship

try:
    from ORM.base import TimeStampedModel
except ImportError:
    from base import TimeStampedModel

class User(TimeStampedModel):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(25), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    securityQ1 = Column(String(100), nullable=False)
    securityQ2 = Column(String(100), nullable=False)
    securityQ3 = Column(String(100), nullable=False)
    securityA1 = Column(String(50), nullable=False)
    securityA2 = Column(String(50), nullable=False)
    securityA3 = Column(String(50), nullable=False)
    address = Column(String(50), nullable=False)
    phone_number = Column(Integer, nullable=False)
    picture = Column(String(100), nullable=False)
    role = Column(Integer, ForeignKey('roles.id'), nullable=False, index=True)
    attempts = Column(Integer, nullable=False)
    last_attempt = Column(REAL, nullable=False)

    # Relationships
    roles = Relationship("Role", back_populates="user", uselist=False)
    orders = Relationship('Order', back_populates='user', passive_deletes=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} username={self.username} password={self.password} securityQ1={self.securityQ1} securityQ2={self.securityQ2} securityQ3={self.securityQ3} securityA1={self.securityA1} securityA2={self.securityA2} securityA3={self.securityA3} address={self.address} phone_number={self.phone_number} picture={self.picture}>"
    
"""class (TimeStampedModel): #ONE TO ONE RELATIE (uselist=False)
    __tablename__ = 'preferences'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'), ondelete="CASCADE", nullable=False, index=True, unique=True)
    theme = Column(String(50), nullable=False)
    language = Column(String(50), nullable=False)

    user = Relationship('User', back_populates='preferences')
    addresses= Relationship('Address', back_populates='user', passive_deletes=True)

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} user_id={self.user_id} theme={self.theme} language={self.language}>"""
    
class Order(TimeStampedModel): #ONE TO MANY RELATION  uselist=True (default)
    __tablename__ = 'order_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    order_id = Column(Integer, nullable=False, index=True)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False, index=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)
    quantity = Column(Integer, nullable=False)
    price = Column(REAL, nullable=False)


    user = Relationship('User', back_populates='orders')
    product = Relationship('Product', back_populates='orders')

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} order_id={self.order_id} product_id={self.product_id} user_id={self.user_id} quantity={self.quantity} price={self.price}>"
    
class Product(TimeStampedModel):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(String, nullable=False)
    dimensions = Column(String(50), nullable=True)
    weight = Column(REAL, nullable=True)
    unit = Column(String(50), nullable=False)
    price = Column(REAL, nullable=False)
    stock_level = Column(Integer, nullable=False)
    category = Column(String(50), nullable=False)
    image = Column(String(100), nullable=False)

    orders = Relationship('Order', back_populates='product')

    def __repr__(self):
       return f"<{self.__class__.__name__} id={self.id} name={self.name} description={self.description} dimensions={self.dimensions} weight={self.weight} unit={self.unit} price={self.price} stock_level={self.stock_level} category={self.category} image={self.image}>"
    
class Role(TimeStampedModel): #MANY TO MANY RELATION 
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    role = Column(Integer, nullable=False)
    description = Column(String(50), nullable=False, unique=True)

    user = Relationship("User", back_populates="roles") #figure this out

    def __repr__(self):
        return f"<{self.__class__.__name__} id={self.id} name={self.name}>"
    
