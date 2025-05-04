import sqlite3 as sql
from static import *

database_dir = 'databases/database.db'
default_img_dir = 'static/erc.png'

#region Inserts

def insertUser( username, password, securityQ1, securityQ2, securityQ3, securityA1, securityA2, securityA3, address, phone_number, pfp, last_attempt:float): #will have to change with hashing algorithm
    con = sql.connect(database_dir)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO users (username, password, securityQ1, securityQ2, securityQ3, securityA1, securityA2, securityA3, address, phone_number, picture, role, attempts, last_attempt) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
        (username, password, securityQ1, securityQ2, securityQ3, securityA1, securityA2, securityA3, address, phone_number, pfp, 2, 5, last_attempt)
    )

    con.commit()
    con.close()
#endregion

#region check exists or gets

#checks return boolean if exists
def checkValidUser(username): #will have to change with hashing algorithm
    con = sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT username FROM users WHERE username=?;", (username, )
    )
    if len(res.fetchall()) == 0:
        con.close()
        return False
    else:
        con.close()
        return True

#gets return a list or list element since jinja2 cannot display tuples or elements of a tuple
#tuples are converted
def get_privilage(username):
    con=sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT role FROM users WHERE username=?;", (username, )
    )
    role = res.fetchone()
    con.close()
    return role[0]

def get_UID(username):
    con=sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT id FROM users WHERE username=?;", (username, )
    )
    uid = res.fetchone()
    con.close()
    return uid[0]

def get_password(id):
    con=sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT password FROM users WHERE id=?;", (id, )
    )
    hash = res.fetchone()
    con.close()
    return hash[0]


def get_displayables(username:str) -> list:
    con=sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT securityQ1, securityQ2, securityQ3, address, phone_number, picture FROM users WHERE username=?;", (username, )
    )
    user = res.fetchone()
    con.close() 
    user = list(user) #must cnvrt to list since tuples are immutable and you can't pass them into jinja2
    return user

def get_security_questions(username:str) -> list:
    con=sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT securityQ1, securityQ2, securityQ3 FROM users WHERE username=?;", (username, )
    )
    user = res.fetchone()
    con.close() 
    user = list(user) #must cnvrt to list since tuples are immutable and you can't pass them into jinja2
    return user
    
def get_security_answers(username:str) -> list:
    con=sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT securityA1, securityA2, securityA3 FROM users WHERE username=?;", (username, )
    )
    user = res.fetchone()
    con.close() 
    user = list(user) #must cnvrt to list since tuples are immutable and you can't pass them into jinja2
    return user


def get_last_attempt(username):
    con=sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT last_attempt FROM users WHERE username=?;", (username, )
    )
    last_attempt = res.fetchone()
    con.close() 
    last_attempt = list(last_attempt)
    return last_attempt[0]

def get_picture(uid) -> str:
    con=sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT picture FROM users WHERE id=?;", (uid, )
    )
    picture = res.fetchone()
    picture = list(picture)
    con.close()
    return picture[0]

def get_attempts(username) -> list:
    con=sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT attempts FROM users WHERE username=?;", (username, )
    )
    attempts = res.fetchone()
    con.close()
    attempts = list(attempts)
    return attempts[0]
#endregion

#region Updates
def update_picture(uid,file_name):
    con=sql.connect(database_dir)
    cur = con.cursor()
    cur.execute(
        "UPDATE users SET picture=? WHERE id=?;",(file_name, uid, ))
    con.commit()
    con.close()

def update_password(username, password):
    con=sql.connect(database_dir)
    cur = con.cursor()
    cur.execute(
        "UPDATE users SET password=? WHERE username=?;",(password,username , ))
    con.commit()
    con.close()

def update_last_attempt(username, last_attempt:float):
    con=sql.connect(database_dir)
    cur = con.cursor()
    cur.execute(
        "UPDATE users SET last_attempt=? WHERE username=?;",(last_attempt ,username, ))
    con.commit()
    con.close()

def update_attempts(username, attempts:int):
    con=sql.connect(database_dir)
    cur = con.cursor()
    cur.execute(
        "UPDATE users SET attempts=? WHERE username=?;",(attempts ,username, ))
    con.commit()
    con.close()
#endregion