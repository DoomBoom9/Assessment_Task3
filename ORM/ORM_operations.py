try:
    from ORM.tables import *
    from ORM.base import Model
    from ORM.ORM_TEST import engine, ORM_session
except ImportError:
    from tables import *
    from base import Model
    from ORM_TEST import engine, ORM_session

from sqlalchemy import text, update

default_image_dir = 'static/4.png'



def get_products():
    products = Product.query.all()
    return products

def get_product_by_id(product_id):
    product = Product.query.filter(Product.id == product_id).first()
    return product

def get_user(username):
    user = User.query.filter(User.username == username).first()
    return user

def deplete_stock_level(product_id, quantity):
    product = get_product_by_id(product_id)
    if product:
        product.stock_level -= quantity
        ORM_session.commit()
        return True #for some error handling idk
    return False

def get_order_by_id(order_id):
    res = []
    order = Order.query.filter(Order.order_id == order_id).all()
    for value in order:
        res.append(value)
    return res



def last_order_id():
    with engine.connect() as connection:
        cursor = connection.execute(text("SELECT MAX(order_id) FROM order_history"))
        cursor = cursor.fetchone()
        for value in cursor:
            if value == None:
                return 0
            else: 
                return value

def insert_order(order_id, product_id, user_id, quantity, price, subtotal):
    with engine.connect() as connection:
        connection.execute(text(
            "INSERT INTO order_history (order_id, product_id, user_id, quantity, price, subtotal) VALUES (:a, :b, :c, :d, :e, :f)"),
            {"a":order_id, "b":product_id, "c":user_id, "d":quantity, "e":price, "f":subtotal}
        )
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
    with engine.connect() as connection:
        res = connection.execute(text(
            "SELECT username FROM users WHERE username=:a;"),{"a": username}
        )
        if len(res.fetchall()) == 0:
            return False
        else:
            return True

#gets return a list or list element since jinja2 cannot display tuples or elements of a tuple
#tuples are converted

def get_categories() -> list:
    res = []
    categories = Category.query.all()
    for category in categories:
        res.append(category)
    return res

def get_order_history(user_id):
    with engine.connect() as connection:
        res = []
        order = Order.query.filter(Order.user_id == user_id).all()
        for value in order:
            res.append(value)
        return res

def get_privilage(username):
    with engine.connect() as connection:
        res = connection.execute(text(
            "SELECT role FROM users WHERE username=:a;"), {"a": username}
        )

        role = []
        res = res.fetchone()
        for value in res:
            role.append(value)
        
    
        return role[0]

def get_UID(username):
    with engine.connect() as connection:
        res = connection.execute(text(
            "SELECT id FROM users WHERE username=:a;"), {"a": username}
        )
        uid = []
        res = res.fetchone()
        for value in res:
            uid.append(value)
    
        return uid[0]

def get_password(id):
    with engine.connect() as connection:
        res = connection.execute(text(
            "SELECT password FROM users WHERE id=:a;"), {"a": id}
        )
        password = []
        res = res.fetchone()
        for value in res:
            password.append(value)
    
        return password[0] #returns hashed password that's stored in the db.


def get_displayables(username:str) -> list:
    with engine.connect() as connection:
        res = connection.execute(text(
            "SELECT securityQ1, securityQ2, securityQ3, address, phone_number, picture FROM users WHERE username=:a;"), {"a": username}
        )
        user = []
        res = res.fetchone()
        for value in res:
            user.append(value)
        
        return user

def get_security_questions(username:str) -> list:
    with engine.connect() as connection:
        res = connection.execute(text(
            "SELECT securityQ1, securityQ2, securityQ3 FROM users WHERE username=:a;"), {"a": username}
        )
        user = []
        res = res.fetchone()
        for value in res:
            user.append(value)

        return user
    
def get_security_answers(username:str) -> list:
    with engine.connect() as connection:
        res = connection.execute(text(
            "SELECT securityA1, securityA2, securityA3 FROM users WHERE username=:a;"), {"a": username}
        )

        answers = []
        res = res.fetchone()

        for value in res:
            answers.append(value)
     
        return answers


def get_last_attempt(username):
    with engine.connect() as connection:
        res = connection.execute(text(
            "SELECT last_attempt FROM users WHERE username=:a;"), {"a": username}
        )
    
        last_attempt = []
        res = res.fetchone()
        for value in res:
            last_attempt.append(value)
        return last_attempt[0]

def get_picture(uid) -> str:
    with engine.connect() as connection:
        res = connection.execute(text(
            "SELECT picture FROM users WHERE id=:a;"), {"a": uid}
        )
    
        picture = []
        res = res.fetchone()
        for value in res:
            picture.append(value)
        
        return picture[0]

def get_attempts(username) -> list:
    with engine.connect() as connection:
        res = connection.execute(text(
            "SELECT attempts FROM users WHERE username=:a;"), {"a": username}
        )

        attempts = []
        res = res.fetchone()
        for value in res:
            attempts.append(value)
        return attempts[0]
#endregion

#region Updates
def update_picture(uid,file_name):
    with engine.connect() as connection:
        connection.execute(text(
            "UPDATE users SET picture=:b WHERE id=:a;"),{"a": uid, "b": file_name})
        connection.commit()
    
def update_phone_number(username:str, phone_num):   
    with engine.connect() as connection:
        connection.execute(text(
            "UPDATE users SET phone_number=:b WHERE username=:a;"),{"a": username, "b": phone_num})
        connection.commit()

def update_address(username:str, address):
    with engine.connect() as connection:
        connection.execute(text(
            "UPDATE users SET address=:b WHERE username=:a;"),{"a": username, "b": address})
        connection.commit()

def update_security_questions(username:str, security_question_1:str, security_question_2:str, security_question_3:str):
    with engine.connect() as connection:
        connection.execute(text(
            "UPDATE users SET securityQ1=:b, securityQ2=:c, securityQ3=:d  WHERE username=:a;"),{"a": username, "b": security_question_1, "c": security_question_2, "d":security_question_3 })
        connection.commit()

def update_security_answers(username:str, security_answer_1:str, security_answer_2:str, security_answer_3:str):
    with engine.connect() as connection:
        connection.execute(text(
            "UPDATE users SET securityA1=:b, securityA2=:c, securityA3=:d  WHERE username=:a;"),{"a": username, "b": security_answer_1, "c": security_answer_2, "d":security_answer_3 })
        connection.commit()
        
def update_password(username, password):
    with engine.connect() as connection:
        connection.execute(text(
            "UPDATE users SET password=:b WHERE username=:a;"),{"a": username, "b": password})
        connection.commit()
    

def update_last_attempt(username, last_attempt:float):
    with engine.connect() as connection:
        connection.execute(text(
            "UPDATE users SET last_attempt=:b WHERE username=:a;"),{"a": username, "b": last_attempt})
        connection.commit()
    

def update_attempts(username, attempts:int):
    with engine.connect() as connection:
        connection.execute(text(
            "UPDATE users SET attempts=:b WHERE username=:a;"), {"a": username, "b": attempts})
        connection.commit()
        
#endregion

if __name__ == "__main__":
    pass
