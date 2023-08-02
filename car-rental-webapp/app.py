from flask import Flask, flash, get_flashed_messages, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import bcrypt
from pymysql import NULL

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'Young32494971'

# Enter your database connection details below
# app.config['MYSQL_HOST'] = '2young.mysql.pythonanywhere-services.com'
# app.config['MYSQL_USER'] = '2young'
# app.config['MYSQL_PASSWORD'] = 'Young@32494971'
# app.config['MYSQL_DB'] = '2young$COMP639'
# app.config['MYSQL_PORT'] = 3306

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'rental'
app.config['MYSQL_PORT'] = 3306

# Intialize MySQL
mysql = MySQL(app)

def is_authenticated():
    return 'loggedin' in session

def get_user_role():
    if session['role'] == 1:
        return 'admin'
    elif session['role'] == 3:
        return 'customer'
    elif session['role'] == 2:
        return 'staff'
    else:
        return None

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
            print(user_password)
            print(password)
            if bcrypt.checkpw(user_password.encode('utf-8'),password.encode('utf-8')):
            # If account exists in accounts table in out database
            # Create session data, we can access this data in other routes
                session['loggedin'] = True
                session['id'] = account['UserID']
                session['username'] = account['UserName']
                session['role'] = account['Role']
                # Redirect to home page
                return redirect(url_for('home'))
            else:
                #password incorrect
                msg = 'Incorrect password!'
        else:
            # Account doesnt exist or username incorrect
            msg = 'Incorrect username'
    # Show the login form with message (if any)
    return render_template('index.html', msg=msg)

# http://localhost:5000/logout - this will be the logout page
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
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
            mysql.connection.commit()
            cursor.execute('UPDATE customer SET Email=%s WHERE Username=%s',(email,username))
            msg = 'You have successfully registered!'
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)


# http://localhost:5000/home - this will be the home page, only accessible for loggedin users
@app.route('/home')
def home():
    # Check if user is loggedin
    if is_authenticated():
        # User is loggedin show them the home page

        # Get the user's role.
        user_role = get_user_role()

        # Check if the user's role is allowed to access this page.
        if user_role == 'admin':
            return render_template('admin_dashboard.html', username=session['username'])
        elif user_role == 'staff':
            return render_template('staff_dashboard.html', username=session['username'])
        elif user_role == 'customer':
            return render_template('customer_dashboard.html', username=session['username'])
        else:
            return 'unauthorized'
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))

# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if is_authenticated():
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE UserId = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))
    
@app.route('/profile/<userid>')
def check_profile(userid):
    # Check if user is loggedin
    if is_authenticated():
        # We need all the account info for the user so we can display it on the profile page
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE UserId = %s', (userid,))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))
    
    
@app.route('/edit/profile')
def edit_profile():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['staff','customer','admin']:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE UserId = %s', (session['id'],))
            account = cursor.fetchone()
            return render_template('edit_profile.html',account=account)
        else:
            return "unauthorized"
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))

    
@app.route('/update/profile', methods=['GET', 'POST'])
def update_profile():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin','staff','customer']:
            userid = int(request.form.get('userid'))
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            display_name = request.form.get('display_name')
            address = request.form.get('address')
            phone = request.form.get('phone')   

            # check if the password is changed by comparing the input password with the password stored in database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute("SELECT * FROM user WHERE UserID=%s",(userid,))
            user_to_update = cursor.fetchone()
            # if password is changed, then the new password needs to be encrypted before inserting into databse
            print(password)
            print(user_to_update['Password'])
            if bcrypt.checkpw(password.encode('utf-8'),user_to_update['Password'].encode('utf-8')):
                hashed = password
            else:
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # insert the data to the database
            sql = '''UPDATE user 
                    SET UserName = %s, Email = %s, Password = %s, ProfileName = %s, Address = %s, PhoneNumber = %s
                    WHERE UserID = %s;'''
            parameters = (username, email, hashed, display_name, address, phone, userid)
            cursor.execute(sql, parameters)
            mysql.connection.commit()
            print(user_to_update['Password'])
            return redirect(url_for('profile'))
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

@app.route('/home/car_list')
def car_list():
    if is_authenticated():
        user_role = get_user_role()
        msg = get_flashed_messages()
        if  user_role == 'customer':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM car WHERE UserID is NULL')
            car_list = cursor.fetchall()
            return render_template('car_list.html', car_list=car_list)
        elif user_role == 'staff' or user_role == 'admin':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM car')
            car_list = cursor.fetchall()
            return render_template('car_list.html', car_list=car_list,msg=msg)
        else:
            return 'unauthorized'
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))


@app.route('/home/cars/<carid>')
def car(carid):
    if is_authenticated():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM car WHERE CarID = %s', (carid,))
        car = cursor.fetchone()
        return render_template('car.html', car=car)
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))
    
@app.route('/home/customer_list')
def customer_list():
    if is_authenticated():
        user_role = get_user_role()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer')
        customer_list = cursor.fetchall()
        msg = get_flashed_messages()
        if user_role in ['admin','staff']:
            return render_template('customer_list.html', customer_list=customer_list, msg=msg, user_role=user_role)
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

@app.route('/home/staff_list')
def staff_list():
    if is_authenticated():
        user_role = get_user_role()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staff')
        stafflist = cursor.fetchall()
        msg = get_flashed_messages()
        print(msg)
        if user_role == 'admin':
            return render_template('staff_list.html', stafflist=stafflist, msg=msg)
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

@app.route('/edit/user/<username>')
def edit_user(username):
    if is_authenticated():
        user_type = request.args.get('type')
        user_role = get_user_role()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM user WHERE UserName=%s',(username,))
        user_to_edit = cursor.fetchone()
        if user_role == 'admin':
            return render_template('edit_user.html', user_type=user_type, user_to_edit=user_to_edit)
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))
    
@app.route('/update/user', methods=['GET', 'POST'])
def update_user():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin']:
            user_type = request.args.get('type')
            userid = int(request.form.get('userid'))
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            display_name = request.form.get('display_name')
            address = request.form.get('address')
            phone = request.form.get('phone')   
            # insert the data to the database
            sql = '''UPDATE user 
                    SET UserName = %s, Email = %s, Password = %s, ProfileName = %s, Address = %s, PhoneNumber = %s
                    WHERE UserID = %s;'''
            parameters = (username, email, password, display_name, address, phone, userid)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, parameters)
            mysql.connection.commit()
            if user_type == 'staff':
                return redirect(url_for('staff_list'))
            elif user_type == 'customer':
                return redirect(url_for('customer_list'))
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

@app.route('/delete/user/<userid>')
def delete_user(userid):
    if is_authenticated():
        user_role = get_user_role()
        if user_role == 'admin':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE UserID=%s',(userid,))
            user_to_delete = cursor.fetchone()
            cursor.execute('SELECT * FROM car WHERE UserID=%s',(userid,))
            rented_car = cursor.fetchone()
            if rented_car:
                flash("Cannot delete customer who has rented a car.")
                return redirect(url_for('customer_list'))
            else:
                cursor.execute('DELETE FROM user WHERE UserID=%s',(userid,))
                mysql.connection.commit()
                flash("Delete successfully")
                if user_to_delete['Role'] is None:
                    return redirect(url_for('customer_list'))
                elif user_to_delete['Role'] == 2:
                    return redirect(url_for('staff_list'))
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))
    
@app.route('/add/user/page', methods=['GET'])
def add_user_page():
    if is_authenticated():
        user_role = get_user_role()
        if user_role == 'admin':
            user_type = request.args.get('type')
            return render_template('add_user.html',user_type=user_type)
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

    
@app.route('/add/user', methods=['Get', 'POST'])
def add_user():
    if is_authenticated():
        user_role = get_user_role()
        if user_role == 'admin':
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            display_name = request.form.get('display_name')
            address = request.form.get('address')
            phone = request.form.get('phone')
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_type = request.form.get('user_type')
            # insert the data to the database
            sql = '''INSERT INTO user (UserName, Password, Email, ProfileName, Address, PhoneNumber, Role)
                    Values (%s, %s, %s, %s, %s, %s, %s);'''
            if user_type == 'customer':
                parameters = (username, hashed, email, display_name, address, phone, None)
            elif user_type == 'staff':
                parameters = (username, hashed, email, display_name, address, phone, 2)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, parameters)
            mysql.connection.commit()
            if user_type == 'customer':
                flash("You have successfully added a customer!")
                return redirect(url_for('customer_list'))
            elif user_type == 'staff':
                flash("You have successfully added a staff!")
            # msg = 'You have successfully added a staff!'
                return redirect(url_for('staff_list'))
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

@app.route('/add/car/page')
def add_car_page():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin','staff']:
            return render_template('add_car.html')
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

@app.route('/add/car', methods=['GET', 'POST'])
def add_car():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin','staff']:
            model = request.form.get('model')
            year = request.form.get('year')
            registration = request.form.get('registration')
            seat_capacity = request.form.get('seat_capacity')
            rental_per_day = request.form.get('rental_per_day')
            userid = request.form.get('userid')
            if userid == "" or userid == 0:
                userid = None
            # insert the data to the database
            sql = '''INSERT INTO car (CarModel, Year, RegNumber, SeatCap, RentalPerDay, UserID)
                    Values (%s, %s, %s, %s, %s, %s);'''
            parameters = (model, year, registration, seat_capacity, rental_per_day, userid)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, parameters)
            mysql.connection.commit()
            flash("You have successfully added a car!")
            return redirect(url_for('car_list'))
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

@app.route('/edit/car/<carid>')
def edit_car(carid):
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin','staff']:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM car WHERE CarID=%s',(carid,))
            car_to_edit = cursor.fetchone()
            return render_template('edit_car.html', car_to_edit=car_to_edit)
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

@app.route('/update/car', methods=['GET', 'POST'])
def update_car():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin','staff']:
            carid = int(request.form.get('carid'))
            car_model = request.form.get('car_model')
            year = request.form.get('year')
            registration_number = request.form.get('registration_number')
            seat_cap = request.form.get('seat_cap')
            rental_per_day = request.form.get('rental_per_day')
            userid = request.form.get('userid')
            if userid == "":
                userid = None
            # insert the data to the database
            sql = '''UPDATE car 
                    SET CarModel = %s, Year = %s, RegNumber = %s, SeatCap = %s, RentalPerDay = %s, UserID = %s
                    WHERE CarID = %s;'''
            parameters = (car_model, year, registration_number, seat_cap, rental_per_day, userid, carid)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, parameters)
            mysql.connection.commit()
            return redirect(url_for('car_list'))
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

@app.route('/delete/car/<carid>')
def delete_car(carid):
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin','staff']:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM car WHERE CarID=%s',(carid,))
            car_to_delete = cursor.fetchone()
            cursor.execute('DELETE FROM car WHERE CarID=%s',(carid,))
            mysql.connection.commit()
            flash("Delete successfully")
            return redirect(url_for('car_list'))
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)