from flask import Flask, render_template, request, session, redirect, abort
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_session import Session
from sqlite_operations import *
from validation import *
import os
from cryptography.fernet import Fernet
import logging
import bcrypt
import time
from datetime import datetime
from flask_wtf import CSRFProtect
from werkzeug.exceptions import RequestEntityTooLarge
from ORM.ORM_operations import *


#region __init__
app = Flask(__name__) #insert private keygen somewhere here


# Configure session to use server-side storage
app.config['SESSION_TYPE'] = 'filesystem'  # Stores sessions in files (can store on database, remembers sessions etc., usage statistics, no of logged in, when, etc.)
app.config['SECRET_KEY'] = os.getenv("ENV_STR")  # WARNING!!! Required for session security
app.config['UPLOAD_FOLDER'] = 'static/profile_pictures' #upload folder filepath
app.config['MAX_CONTENT_LENGTH'] = 2 * 1024 * 1024 #2Mb file size limit

csrf = CSRFProtect(app) #uses the csrfprotect module to generate tokens that inserts into forms and then checks if they match/are valid

database_dir = 'databases/database.db' #database file path

key = os.getenv("ENV_STR") #error if encryption key is not in the env
if not key:
    raise ValueError("ENV_STR not found")

cipher = Fernet(key) #generates the cipher for encryption

#error logging stuff
file_handler = logging.FileHandler('error.log')
file_handler.setLevel(logging.WARNING)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.WARNING)

Session(app)  # Initialize session
"""limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",)"""

default = "1 per second" #debug var to change the limiter

default_img_dir = 'static/erc.png'

#region Inserts

def get_products():
    con=sql.connect(database_dir)
    cur = con.cursor()
    res = cur.execute(
        "SELECT * FROM products"
    )
    products = res.fetchall()
    return products


@app.route("/", methods=['POST', 'GET'])
def product_page():
    products = get_products()
    return render_template("products.html", products=products)

@app.route("/checkout", methods=['POST', 'GET'])
def checkout_page():
    return render_template("checkout.html")

@app.route("/cart", methods=['POST', 'GET'])
def cart_page():
    # Get the cart from the session
    # Get Quantity
    # Get each product price
    # Calculate total price
    # Parse item name and image into the page once ORM is implemented
    cart=1

    return render_template("cart.html", cart=cart)

@app.route("/receipt", methods=['POST', 'GET'])
def receipt_page():
    

    return render_template("receipt.html")

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)