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
from datetime import datetime, date
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
limiter = Limiter(
    get_remote_address,
    app=app,
    default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",)

default = "1 per second" #debug var to change the limiter

#endregion
#region Dashboards

@app.route("/dashboard", methods = ['POST', 'GET'])
@limiter.limit(default)
def dashboard():
    if ('username' not in session):
        app.logger.warning(f'{datetime.now()} No username stored in session but dashboard was accessed @ip={request.remote_addr}')
        abort(403)
    if ('role' not in session):
        app.logger.warning(f'{datetime.now()} No role stored in session but dashboard was accessed @ip={request.remote_addr}')
        abort(403)
    if ('username' in session) & (session['role'] == 2):
        username = session['username']
        user_info = get_displayables(username) #gets the things that you'd want to display
        user_info[3] = decrypt_input(user_info[3], cipher) #decrypt addr for display
        user_info[4] = decrypt_input(user_info[4], cipher) #decrypt Phone num for display
        
        app.logger.info('Dashboard Loaded')

        return render_template("dashboard.html",username=username, securityQ1=user_info[0], securityQ2=user_info[1], securityQ3=user_info[2], address=user_info[3], phone_number=user_info[4], picture=user_info[5]) 
    else:
        abort(403) #redirects to login page if not logged in
        #realistically there should be a popup saying not logged in with some js or whatnot


@limiter.limit(default)
@app.route("/admin_dashboard")
def admin_dashboard():
    if ('username' not in session):
        abort(403)
    if ('role' not in session):
        abort(403)
    if ('username' in session) & (session['role'] == 1): #checks for valid session and role
        username = session['username']
        user_info = get_displayables(username) #gets the things that you'd want to display
        user_info[3] = decrypt_input(user_info[3], cipher) #decrypt addr for display
        user_info[4] = decrypt_input(user_info[4], cipher) #decrypt Phone num for display
        return render_template('adminDashboard.html', username=username, securityQ1=user_info[0], securityQ2=user_info[1], securityQ3=user_info[2], address=user_info[3], phone_number=user_info[4], picture=user_info[5])
    else:
        abort(403)

@limiter.limit(default)
@app.route("/checkout")
def checkout_page():
    if request.method == 'POST':

        session['checkout_info'] = checkoutInfo( #fix this somewhere
            request.form['first_name'],
            request.form['last_name'],
            request.form['country'],
            request.form['state'],
            request.form['post_code'],
            request.form['address'],
            request.form['shipping_country'],
            request.form['shipping_state'],
            request.form['shipping_post_code'],
            request.form['shipping_address'],
            request.form['payment_method'],
            request.form['card_name'],
            request.form['credit_card_number'],
            request.form['expiration_date'],
            request.form['cvv']


        )

        session['authenitcation'] = True

        redirect('/lower_stock_level') #redirects to the receipt page with the checkout info and cart items

    if ('username' not in session):
        redirect('/login')
    else:
        return render_template("checkout.html",  methods=['POST', 'GET'])

@limiter.limit(default)
@app.route("/cart",  methods=['POST', 'GET'])
def shopping_cart_page():
    if request.method == 'POST':
        redirect('/checkout')

    cart = session.get("cart", {})
    if not cart:
        return render_template("cart.html", error="Your cart is empty.")
    object_quantity_dict = {}
    for i in cart.keys():
        object_quantity_dict[get_product_by_id(i)] = cart[i] #creates a dictionary of the products in the cart
    print(object_quantity_dict)
    return render_template("cart.html", cart=object_quantity_dict) 

@limiter.limit("5 per second")
@app.route("/", methods=['POST', 'GET'])
def products_page():
    product_list = get_products()
    return render_template("products.html", products=product_list)

@limiter.limit(default)
@app.route("/about",  methods=['POST', 'GET'])
def about_page():
    return render_template("about.html")

@limiter.limit(default)
@app.route("/receipt",  methods=['POST', 'GET'])
def receipt_page(): #so you cant access this page without having bought something
    if not session.get("username"):
        abort(403)
    if session['authentication'] == False or session['authentication'] == None:
        abort(403)


    
    

    render_template("receipt.html", user=session['checkout_info'], cart=session['cart']) #pass the cart to the receipt page

#endregion

#region Non-Displayable Routes
@app.route("/add_to_cart/<int:product_id>_<int:quantity>")   # Add to cart by product_id
def add_to_cart(product_id, quantity):
    
    cart = session.get("cart", {})  # Get the cart from the session, or create a new one if it doesn't exist

    product_id_str = str(product_id)  # Convert to string
    if product_id_str not in cart:
        cart[product_id_str] = quantity
    else:
        cart[product_id_str] += quantity
 


    # IMPORTANT - Convert product_id to a string (because session keys are strings).  
    # If the product is already in the cart, increase the quantity by 1.
    # If not, start with 0 and add 1.

    print(cart)
    session["cart"] = cart
    print(session["cart"])
    # Save the updated cart back into the session.

    return redirect("/")

@app.route("/lower_stock_level")
def lower_stock_level(): #pass some authentication after purchase
    if session['authentication'] == False or session['authentication'] == None:
        abort(403)
    cart = session.get("cart", {})
    if not cart: # check if it exists or if it is empty
        return render_template("error.html", error="Your cart is empty.")
    
    order_id = last_order_id() 
    user_id = get_UID(session['username']) #gets the user id

    for product in cart:
        if (product.stock_level - cart[product])<= 0:
            return render_template("error.html", error="Not enough stock available.") #fix this error at the end
        else:     
            insert_order(order_id, product.id, user_id, session['cart'][product], product.price) #inserts the order into the database
            deplete_stock_level(product, cart[product]) #updates the stock level of the product 
                   
        session['cart'] = {}
    return redirect("/receipt") #redirects to the receipt page
    
#endregion

#region Auths


@app.route("/login", methods=['POST','GET'])
@limiter.limit(default)
def login():
    timeout = 600 #sets the time in seconds that accounts will be locked for upon too many login attempts
    if request.method == "POST":
        username = request.form['username']
        password = request.form['password']
        honeypot = request.form['honeypot']
        if honeypot != '': #if the honeypot field is filled in
            app.logger.warning(f'{datetime.now()} Honeypot field was filled in @ip={request.remote_addr}')
            return render_template('login.html')
        if check_username(username) == False: #checks if a username meets valid username requirements
            app.logger.warning(f'{datetime.now()} client side validation bypassed @ip={request.remote_addr}')
            return render_template('login.html', error='Username or Password was Invalid')
        if check_password(password) == False: #checks if a password meets valid password requirements
            app.logger.warning(f'{datetime.now()} client side validation bypassed @ip={request.remote_addr}')
            return render_template('login.html', error='Username or Password was Invalid')
        #get request hashed pword
        #compare hashed pword against user
        username = sanitise(username)
        password = sanitise(password)
        curr_time = time.time()
        last_attempt = get_last_attempt(username)
        attempts = get_attempts(username)
        delta_time = curr_time - last_attempt
        uid = get_UID(username)
        if (delta_time < timeout) and (attempts < 1): #if the time between last attempt and current attempt is less than timeout and current attempts are less than 1
            app.logger.warning(f'{datetime.now()} user: {username}, ID: {uid} has been locked due to too many login attempts. Last request @ip={request.remote_addr}')
            return render_template('login.html', error='Too many attempts please try again later')
        if (delta_time > timeout) and (attempts < 5): #if the time between last attempt and current attempt is greater than timeout and attempts are less than 5
            app.logger.debug(f'{datetime.now()} user: {username}, has had attempts reset')
            update_attempts(username, 5) # reset login attempts
        if not uid: #if uid does not exist
            return render_template('login.html', error='Username or Password was incorrect') #username is incorrect as there is no UID with corresponding username
        hash = get_password(uid)
        if not password: #if password does not exist 
            return render_template('login.html', error='Username or Password was incorrect') #username is incorrect as there is no password with corresponding UID
        if bcrypt.checkpw(password.encode('utf-8'), hash) == False: #checks the hashed and given password & is incorrect
            attempts -= 1
            update_attempts(username, attempts)
            last_attempt = time.time()
            update_last_attempt(username, last_attempt)
            return render_template('login.html', error='Username or Password was incorrect') #password is incorrects as salted hashes do not match
        else: #log in successful
            session['username'] = username
            session['role'] = get_privilage(username)
            if session['role'] == 1: #admin user
                app.logger.info('Admin user logged in')
                return redirect('/admin_dashboard')
            if session['role'] == 2: #normal user
                app.logger.info('Normal user logged in')
                return redirect('/dashboard')
            else: #invalid role
                app.logger.error(f'{datetime.now()} Invalid roleID was passed @ip={request.remote_addr}')
                raise ValueError('invalid role ID was passed')
        #Somesort of logging or page response should go here with req username and password
   
    return render_template("login.html")


@app.route("/register", methods=['POST','GET'])
@limiter.limit(default)
def register():
    if request.method == "POST":
        username = str(request.form['username'])
        honeypot = request.form['honeypot']
        if honeypot != '': #if the honeypot field is filled in
            app.logger.warning(f'{datetime.now()} Honeypot field was filled in @ip={request.remote_addr}')
            return render_template('register.html')
        if check_username(username) == False: #if username does not pass requirements
            app.logger.warning(f"{datetime.now()} client side validation bypassed @ ip={request.remote_addr}")
            raise ValueError('Something went wrong!')
        username = sanitise(username) #this could create bugs try having many << as username
        if checkValidUser(username) == True: #checks valid username
            return render_template("register.html", error='Username is taken! Try again')
        password = str(request.form['password'])
        securityQ1 = request.form['securityQ1']
        securityQ2 = request.form['securityQ2']
        securityQ3 = request.form['securityQ3']
        securityA1 = request.form['securityA1'].upper() #makes sure that security answers are converted to upper so capitalisation doesn't matter
        securityA2 = request.form['securityA2'].upper()
        securityA3 = request.form['securityA3'].upper()
        address = str(request.form['address'])
        phone_num = str(request.form['phoneNumber'])
        file = request.files['file']
        #perform server side validation here
        if check_file(file.filename) == False: #if file does not meet requirements
            app.logger.warning(f"{datetime.now()} client side validation bypassed @ ip={request.remote_addr}")
            return render_template("register.html", error='Please try again!')
        
        if check_all(username, password, securityA1, securityA2, securityA3, address, phone_num, file.filename) == True:
            #username already sanitised for form validation
            password = sanitise(password)
            securityA1 = sanitise(securityA1)
            securityA2 = sanitise(securityA2)
            securityA3 = sanitise(securityA3)
            address = sanitise(address)
            phone_num = sanitise(phone_num)

            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #hashes things that could be used as passwords
            securityA1 = bcrypt.hashpw(securityA1.encode('utf-8'), bcrypt.gensalt())
            securityA2 = bcrypt.hashpw(securityA2.encode('utf-8'), bcrypt.gensalt())
            securityA3 = bcrypt.hashpw(securityA3.encode('utf-8'), bcrypt.gensalt())
            address = encrypt_input(address,cipher) #encrypts sensitive but displayable fields
            phone_num = encrypt_input(phone_num,cipher)

            last_attempt = time.time() # so the login doesn't get angry and has a valid float type rather than none, i also thought this might be safer than a random float

            insertUser(username, password, securityQ1, securityQ2, securityQ3, securityA1, securityA2, securityA3, address, phone_num, 'placeholder', last_attempt)

            #probably could facade this but idk how high on the priorities that is
            #this is a bit funky but it uses the user UID to rename the file that way user input isn't used maliciously or not
            #and the naming is standardised for potential changing of profile picture files
            #I need to check the 


            uid = str(get_UID(username)) #gets the UID
            ext = os.path.splitext(file.filename) #splits the name and file extension
            file.filename = f"{uid}{ext[1]}" #replaces the name with the UID
            file_name = os.path.join(app.config['UPLOAD_FOLDER'], file.filename) #saves filepath
            file.save(file_name) #saves file
            uid = int(uid) 
            update_picture(uid, file_name) #uploads filepath to UID
            return redirect("/")
        
        #Somesort of logging or page response should go here
    
    return render_template("register.html")


@app.route("/forgot_password", methods=["POST", "GET"])
@limiter.limit(default)
def forgot_password(): 
    if (request.method == "POST"):
        honeypot = request.form['honeypot']
        if honeypot != '': #if the honeypot field is filled in
            app.logger.warning(f'{datetime.now()} Honeypot field was filled in @ip={request.remote_addr}')
            return render_template('forgot_password.html')
        username = request.form['username'] 
        if check_username(username) == False: #checks supplied username meets requirements
            app.logger.warning(f'{datetime.now()} client side validation bypassed @ip={request.remote_addr}')
            raise ValueError('Something went wrong!')
        username  = sanitise(username)
        if checkValidUser(username) == False: #checks if user exists
            return render_template('forgot_password.html', error='User does not exist!')
        else: #if user exists
            session['forgot_user'] = username
            return redirect('/answer_security')

    return render_template('forgot_password.html')
         

@app.route("/answer_security", methods=["POST", "GET"])
@limiter.limit(default)
def answer_security():  
    username = session['forgot_user']
    if username == None: #if no username is stored in session
        app.logger.warning(f'{datetime.now()} No username stored in session but answer_security was accessed @ip={request.remote_addr}')
        abort(403)
    if (request.method == "POST"):
        honeypot = request.form['honeypot']
        if honeypot != '': #if the honeypot field is filled in
            app.logger.warning(f'{datetime.now()} Honeypot field was filled in @ip={request.remote_addr}')
            return render_template('answer_security.html')
        securityA1 = request.form['securityA1'].upper() #so capitalisation doesn't matter
        securityA2 = request.form['securityA2'].upper()
        securityA3 = request.form['securityA3'].upper()
        securityA1 = sanitise(securityA1) #sanitisation
        securityA2 = sanitise(securityA2)
        securityA3 = sanitise(securityA3)
        answers = get_security_answers(username)

        if (check_default(securityA1)==False) or (check_default(securityA2)==False) or (check_default(securityA3)==False): #if any answers do not meet vaidation requirements
            app.logger.warning(f'{datetime.now()} client side validation bypassed @ip={request.remote_addr}')
            raise ValueError('Security answers did not pass validation')

        if (bcrypt.checkpw(securityA1.encode('utf-8'), answers[0] ) == True) and ((bcrypt.checkpw(securityA2.encode('utf-8'), answers[1] ))==True) and (bcrypt.checkpw(securityA3.encode('utf-8'), answers[2] )==True): #if answers match
            return redirect('/reset_password')
        else:
            app.logger.info(f'{datetime.now()} security answers did not match @ip{request.remote_addr}')
            return render_template('forgot_password.html', error='Security answers did not match')

    security_questions = get_security_questions(username) #gets security qs
    return render_template('answer_security.html', securityQ1=security_questions[0], securityQ2=security_questions[1], securityQ3=security_questions[2])
    
@app.route("/reset_password", methods=['POST','GET'])
@limiter.limit(default)
def reset_password():
    username = session['forgot_user']
    if 'forgot_user' not in session: #if no username is stored in session
        app.logger.warning(f'{datetime.now()} No username stored in session but reset_password was accessed @ip={request.remote_addr}')
        abort(403)
    if request.method == "POST":
        honeypot = request.form['honeypot']
        if honeypot != '': #if the honeypot field is filled in
            app.logger.warning(f'{datetime.now()} Honeypot field was filled in @ip={request.remote_addr}')
            return render_template('reset_password.html')
        password = request.form['password']
        confirm_password = request.form['confirmPassword']
        if password != confirm_password: #if new password does not match confirmation of new password
            app.logger.warning(f'{datetime.now()} Clientside Validation bypassed @ip{request.remote_addr}')
            return render_template('reset_password.html', error='Passwords do not match')
        else:
            if check_password(password) == False: #if password does not meet validation reqs
                app.logger.warning(f'{datetime.now()} Clientside Validation bypassed @ip{request.remote_addr}')
                raise ValueError('Something went wrong!') 
            password = sanitise(password)
            
            password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()) #hashes new password
            update_password(username, password)
            session.pop('forgot_user', None)
            return redirect("/")  
            

    return render_template('reset_password.html')


@app.route("/logout", methods=['POST', 'GET'])
@limiter.limit(default)
def logout():
    if session['username'] == None: #if no username is stored in session   
        app.logger.warning(f'{datetime.now()} No username stored in session but logout was accessed @ip={request.remote_addr}') 
        abort(403)
    session.pop('username', None)  # Remove session data
    return redirect("/") # url_for('home'))

#endregion

#region Security Headers

@app.after_request
def add_security_headers(resp):
    resp.headers['Content-Security-Policy'] =  "default-src 'self'; object-src 'none'; base-uri 'none';" #prevents inline scripts from running and objects
    resp.headers['X-Content-Type-Options'] = 'nosniff' #forces the browser to honour the content type instead of auto detecting
    resp.headers['X-Frame-Options'] = 'SAMEORIGIN' #prevents external sites from embedding this site in iframe, helping prevent clickjacking 
    return resp

#endregion
#region Error Handling
@app.errorhandler(Exception)
def handle_exception(e):
    app.logger.error(f'{datetime.now()} Exception @ip={request.remote_addr}: {e}')
    return render_template('error.html', error='')

@app.errorhandler(ValueError)
def value_error(e):
    app.logger.error(f'{datetime.now()} Value Error @ip={request.remote_addr}: {e}')
    return render_template('error.html', error='An invalid value was passed')

@app.errorhandler(TypeError)
def type_error(e):
    app.logger.error(f'{datetime.now()} Type Error @ip={request.remote_addr}: {e}')
    return render_template('error.html', error='An invalid type was passed')

@app.errorhandler(RequestEntityTooLarge)
def request_too_large(e):
    app.logger.error(f'{datetime.now()} Request too large @ip={request.remote_addr}: {e}')
    return render_template('error.html', error='file was too large! upload a file under 2Mb')

@app.errorhandler(403)
def forbidden(e):
    app.logger.error(f'{datetime.now()} Forbidden access @ip={request}: {e}')
    return render_template('error.html', error=403), 403

@app.errorhandler(404)
def page_not_found(e):
    app.logger.error(f'{datetime.now()} Page not found @ip={request.remote_addr}: {e}')
    return render_template('error.html', error=404), 404

@app.errorhandler(500)
def internal_error(e):
    app.logger.error(f'{datetime.now()} Internal Server Error @ip={request.remote_addr}: {e}')
    return render_template('error.html', error=500), 500
#endregion

#region misc needed in main
def encrypt_input(input:str, cipher:str) -> str:
    return cipher.encrypt(input.encode())

def decrypt_input(input:str, cipher:str) -> str:
    return cipher.decrypt(input).decode()

class checkoutInfo():
    def __init__(self, first_name, last_name, country,
                 state, post_code, address, shipping_country,
                 shipping_state, shipping_post_code,
                 shipping_address, payment_method, card_name,
                 credit_card_number, expiration_date, cvv):
        
        self.first_name = first_name
        self.last_name = last_name
        self.country = country
        self.state = state
        self.post_code = post_code
        self.address = address
        self.shipping_country = shipping_country
        self.shipping_state = shipping_state
        self.shipping_post_code = shipping_post_code
        self.shipping_address = shipping_address
        self.payment_method = payment_method
        self.card_name = card_name
        self.credit_card_number = credit_card_number
        self.expiration_date = expiration_date
        self.cvv = cvv


#endregion


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)