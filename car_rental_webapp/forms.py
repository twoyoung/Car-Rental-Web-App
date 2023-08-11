from car_rental_webapp import app, mysql
from flask import request, render_template, session, redirect, url_for
import MySQLdb.cursors
import bcrypt
import re
from util import is_authenticated, get_user_role, get_account



@app.route('/')
def index():
    return render_template('index.html')


# http://localhost:5000/login/ - this will be the login page, we need to use both GET and POST requests
@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        user_password = request.form['password']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE UserName = %s', (username,))
        # Fetch one record and return result
        account = cursor.fetchone()
        if account is not None:
            password = account['Password']
            if bcrypt.checkpw(user_password.encode('utf-8'),password.encode('utf-8')):
            # If account exists in accounts table in out database
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['role'] = account['Role']
                session['id'] = account['UserID']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('index.html')

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('username', None)
   session.pop('role', None)
   # Redirect to login page
   return redirect(url_for('login'))

# http://localhost:5000/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE UserName = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            cursor.execute('INSERT INTO user (UserName, Password, Role) VALUES (%s, %s, %s)', (username, hashed, 3))
            user_id = cursor.lastrowid
            cursor.execute('INSERT INTO customer (UserID, Email) VALUES (%s, %s)',(user_id, email))
            mysql.connection.commit()
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html',msg=msg)


# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if is_authenticated():
        # User is loggedin show them the home page

        # Get the user's role.
        user_role = get_user_role()
        account = get_account(session['id'])
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM car WHERE CustomerID is NULL and Active=1')
        car_list = cursor.fetchall()
        available_car_count = sum(1 for car in car_list if car['CustomerID'] is None)
        cursor.execute('SELECT * FROM car WHERE Active=1')
        car_list = cursor.fetchall()
        total_car_count = sum(1 for car in car_list)
        cursor.execute('SELECT * FROM customer WHERE Active=1')
        customer_list = cursor.fetchall()
        customer_count = sum(1 for customer in customer_list)
        cursor.execute('SELECT * FROM staff WHERE Active=1')
        staff_list = cursor.fetchall()
        staff_count = sum(1 for staff in staff_list)
        print(total_car_count)
        print(customer_count)
        print(staff_count)

        # Check if the user's role is allowed to access this page.
        if user_role == 'admin':
            return render_template('admin_dashboard.html', customer_count=customer_count, staff_count=staff_count,car_count=total_car_count,user_role=session['role'])
        elif user_role == 'staff':
            return render_template('staff_dashboard.html',name=account['FirstName'],customer_count=customer_count,car_count=total_car_count,user_role=session['role'])
        elif user_role == 'customer':
            return render_template('customer_dashboard.html',name=account['FirstName'], car_list=car_list, user_role=session['role'], car_count=available_car_count)
        else:
            return render_template('unauthorized.html')
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))