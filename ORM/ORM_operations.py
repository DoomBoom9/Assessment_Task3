try:
    from ORM.tables import *
    from ORM.base import Model
    from ORM.ORM_TEST import engine, ORM_session
except ImportError:
    from tables import *
    from base import Model
    from ORM_TEST import engine, ORM_session

from sqlalchemy import text

default_image_dir = 'static/4.png'



def get_products():
    products = Product.query.all()
    return products

def get_product_by_id(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    return product

def deplete_stock_level(product_id, quantity):
    product = get_product_by_id(product_id)
    if product:
        product.stock_level -= quantity
        Model.session.commit()
        return True #for some error handling idk
    return False


def last_order_id():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT MAX(order_id) FROM order_history"))
        if result.fetchone()[0] is None:
            return 1
        else:
            return result.fetchone()[0] + 1

def insert_order(order_id, product_id, user_id, quantity, price):
    with engine.connect() as connection:
        connection.execute(text(
            "INSERT INTO order_history (order_id, product_id, user_id, quantity, price) VALUES (?, ?, ?, ?, ?, ?)",
            (order_id, product_id, user_id, quantity, price)
        ))
        connection.commit()

#region Inserts

def insertUser( username, password, securityQ1, securityQ2, securityQ3, securityA1, securityA2, securityA3, address, phone_number, pfp, last_attempt:float): #will have to change with hashing algorithm
    with engine.connect() as connection:
        connection.execute(text(
            "INSERT INTO users (username, password, securityQ1, securityQ2, securityQ3, securityA1, securityA2, securityA3, address, phone_number, picture, role, attempts, last_attempt) VALUES (:a,:b,:c,:d,:e,:f,:g,:h,:i,:j,:k,:l,:m,:n)"),
            {"a":username, "b":password, "c":securityQ1, "d":securityQ2, "e":securityQ3, "f":securityA1, "g":securityA2, "h":securityA3, "i":address, "j":phone_number, "k":pfp, "l": 2,"m": 5, "n":last_attempt}
        )
        connection.commit()
#endregion

#region check exists or gets

#checks return boolean if exists
def checkValidUser(username): #will have to change with hashing algorithm
    with engine.connect as connection:
        res = connection.execute(text(
            "SELECT username FROM users WHERE username=?;", (username, )
        ))
    if len(res.fetchall()) == 0:
        return False
    else:
        return True

#gets return a list or list element since jinja2 cannot display tuples or elements of a tuple
#tuples are converted
def get_privilage(username):
    with engine.connect as connection:
        res = connection.execute(text(
            "SELECT role FROM users WHERE username=?;", (username, )
        ))
    role = res.fetchone()
    
    return role[0]

def get_UID(username):
    with engine.connect as connection:
        res = connection.execute(text(
            "SELECT id FROM users WHERE username=?;", (username, )
        ))
    uid = res.fetchone()
    
    return uid[0]

def get_password(id):
    with engine.connect as connection:
        res = connection.execute(text(
            "SELECT password FROM users WHERE id=?;", (id, )
        ))
    hash = res.fetchone()
    
    return hash[0]


def get_displayables(username:str) -> list:
    with engine.connect as connection:
        res = connection.execute(text(
            "SELECT securityQ1, securityQ2, securityQ3, address, phone_number, picture FROM users WHERE username=?;", (username, )
        ))
    user = res.fetchone()
     
    user = list(user) #must cnvrt to list since tuples are immutable and you can't pass them into jinja2
    return user

def get_security_questions(username:str) -> list:
    with engine.connect as connection:
        res = connection.execute(text(
            "SELECT securityQ1, securityQ2, securityQ3 FROM users WHERE username=?;", (username, )
        ))
    user = res.fetchone()
     
    user = list(user) #must cnvrt to list since tuples are immutable and you can't pass them into jinja2
    return user
    
def get_security_answers(username:str) -> list:
    with engine.connect as connection:
        res = connection.execute(text(
            "SELECT securityA1, securityA2, securityA3 FROM users WHERE username=?;", (username, )
        ))
    user = res.fetchone()
     
    user = list(user) #must cnvrt to list since tuples are immutable and you can't pass them into jinja2
    return user


def get_last_attempt(username):
    with engine.connect as connection:
        res = connection.execute(text(
            "SELECT last_attempt FROM users WHERE username=?;", (username, )
        ))
    last_attempt = res.fetchone()
     
    last_attempt = list(last_attempt)
    return last_attempt[0]

def get_picture(uid) -> str:
    with engine.connect as connection:
        res = connection.execute(text(
            "SELECT picture FROM users WHERE id=?;", (uid, )
        ))
    picture = res.fetchone()
    picture = list(picture)
    
    return picture[0]

def get_attempts(username) -> list:
    with engine.connect as connection:
        res = connection.execute(text(
            "SELECT attempts FROM users WHERE username=?;", (username, )
        ))
    attempts = res.fetchone()
    
    attempts = list(attempts)
    return attempts[0]
#endregion

#region Updates
def update_picture(uid,file_name):
    with engine.connect as connection:
        connection.execute(text(
            "UPDATE users SET picture=? WHERE id=?;",(file_name, uid, )))
        connection.commit()
    
    

def update_password(username, password):
    with engine.connect as connection:
        connection.execute(text(
            "UPDATE users SET password=? WHERE username=?;",(password,username , )))
        connection.commit()
    

def update_last_attempt(username, last_attempt:float):
    with engine.connect as connection:
        connection.execute(text(
            "UPDATE users SET last_attempt=? WHERE username=?;",(last_attempt ,username, )))
        connection.commit()
    

def update_attempts(username, attempts:int):
    with engine.connect as connection:
        connection.execute(text(
            "UPDATE users SET attempts=? WHERE username=?;",(attempts ,username, )))
        connection.commit()
        
#endregion

if __name__ == "__main__":
    insertUser('test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 'test', 1234567890, default_image_dir, 0.0)