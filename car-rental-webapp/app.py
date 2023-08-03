from flask import Flask, flash, get_flashed_messages, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import bcrypt
from pymysql import NULL

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'Young32494971'

#Enter your database connection details below
app.config['MYSQL_HOST'] = '2young.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = '2young'
app.config['MYSQL_PASSWORD'] = 'Young@32494971'
app.config['MYSQL_DB'] = '2young$COMP639'
app.config['MYSQL_PORT'] = 3306

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'rental'
# app.config['MYSQL_PORT'] = 3306

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
    
def username_crash(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE UserName = %s', (username,))
    exist_account = cursor.fetchone()
        # If account exists show error and validation checks
    if exist_account:
        return 1
    else:
        return 0
    
def get_account(userid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = '''SELECT * FROM
            (SELECT 
            user.UserID,
            user.UserName,
            user.Password,
            user.Role,
            COALESCE(staff.StaffID, NULL) AS StaffID,
            COALESCE(customer.CustomerID, NULL) AS CustomerID,
            COALESCE(staff.Email, customer.Email) AS Email,
            COALESCE(staff.DisplayName, customer.DisplayName) AS DisplayName,
            COALESCE(staff.Address, customer.Address) AS Address,
            COALESCE(staff.PhoneNumber, customer.PhoneNumber) AS PhoneNumber
            FROM user
            LEFT JOIN staff ON user.UserID = staff.UserID
            LEFT JOIN customer ON user.UserID = customer.UserID) AS user_customer_staff         
            WHERE UserID = %s;'''
    cursor.execute(sql,(userid,))
    account = cursor.fetchone()
    return account
    

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
                session['username'] = account['UserName']
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
    return render_template('index.html', msg=msg)

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
        user_role = get_user_role()
        # We need all the account info for the user so we can display it on the profile page
        account = get_account(session['id'])
        print(account)
        # Show the profile page with account info
        return render_template('profile.html', account=account,user_role=user_role)
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))
    
@app.route('/profile/<userid>')
def check_profile(userid):
    # Check if user is loggedin
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin','staff']:
            # We need all the account info for the user so we can display it on the profile page
            account = get_account(userid)
            # Show the profile page with account info
            return render_template('profile.html', account=account,user_role=user_role)
        else:
            return "unauthorized"
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))
    
    
@app.route('/edit/profile')
def edit_profile():
    if is_authenticated():
        msg = get_flashed_messages()
        account = get_account(session['id'])
        return render_template('edit_profile.html',account=account,msg=msg) 
    else:
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))

    
@app.route('/update/profile', methods=['GET', 'POST'])
def update_profile():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin','staff','customer']:
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            display_name = request.form.get('display_name')
            address = request.form.get('address')
            phone = request.form.get('phone')

            original_account = get_account(session['id'])
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #if username is changed:
            if username != original_account['UserName']:
                #check if username already exists in database
                if username_crash(username):
                    flash('Username already exists. Please choose a different username.')
                    return redirect(url_for('edit_profile'))
                else:
                    cursor.execute('UPDATE user SET UserName=%s WHERE UserID=%s',(username, session['id']))
                    mysql.connection.commit()
                    session['username'] = username

            # check if the password is changed by comparing the input password with the password stored in database
            if password != original_account['Password']:
                # if password is changed, then the new password needs to be encrypted before inserting into databse
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute('UPDATE user SET Password=%s WHERE UserID=%s',(hashed, session['id']))
                mysql.connection.commit()

            # update the other data to the database
            if user_role == 'customer':
                cursor.execute('UPDATE customer SET Email=%s, DisplayName = %s, Address = %s, PhoneNumber = %s WHERE customer.UserID = %s', (email, display_name, address, phone, session['id']))
                mysql.connection.commit()
                return redirect(url_for('profile'))
            elif user_role == 'staff':
                cursor.execute('UPDATE staff SET Email=%s, DisplayName = %s, Address = %s, PhoneNumber = %s WHERE staff.UserID = %s', (email, display_name, address, phone, session['id']))
                mysql.connection.commit()
                return redirect(url_for('profile'))
            else:
                return 'unauthorized'
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
            cursor.execute('SELECT * FROM car WHERE CustomerID is NULL')
            car_list = cursor.fetchall()
            return render_template('car_list.html', car_list=car_list, user_role=user_role )
        elif user_role in ['staff','admin']:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM car')
            car_list = cursor.fetchall()
            for car in car_list:
                if car['CarImage']:
                    car['CarImage'] = base64.b64encode(car['CarImage']).decode('utf-8')
            return render_template('car_list.html', car_list=car_list,msg=msg, user_role=user_role)
        else:
            return 'unauthorized'
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))


@app.route('/home/car/<carid>')
def check_car(carid):
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
        cursor.execute('SELECT * FROM customer LEFT JOIN user ON customer.UserID = user.UserID')
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
        cursor.execute('SELECT * FROM staff LEFT JOIN user ON staff.UserID = user.UserID')
        stafflist = cursor.fetchall()
        msg = get_flashed_messages()
        print(msg)
        if user_role == 'admin':
            return render_template('staff_list.html', stafflist=stafflist, msg=msg)
        else:
            return 'unauthorized'
    else:
        return redirect(url_for('login'))

@app.route('/edit/user/<userid>')
def edit_user(userid):
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin']:
            msg = get_flashed_messages()
            user_type = request.args.get('type')
            user_role = get_user_role()
            user_to_edit = get_account(userid)
            if user_role == 'admin':
                return render_template('edit_user.html', user_type=user_type, user_to_edit=user_to_edit,msg=msg)
            else:
                return 'unauthorized'
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
            user_id = request.form.get('user_id')
            username = request.form.get('username')
            password = request.form.get('password')
            email = request.form.get('email')
            display_name = request.form.get('display_name')
            address = request.form.get('address')
            phone = request.form.get('phone')  

            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user LEFT JOIN (SELECT * FROM customer UNION SELECT * FROM staff) AS customer_and_staff ON customer_and_staff.UserID=user.UserID WHERE user.UserID = %s',(user_id,))
            original_account = cursor.fetchone()

            #if username is changed:
            if username != original_account['UserName']:
                #check if username already exists in database
                if username_crash(username):
                    flash('Username already exists. Please choose a different username.')
                    return redirect(url_for('edit_user',userid=user_id))
                else:
                    cursor.execute('UPDATE user SET UserName=%s WHERE UserID=%s',(username, user_id))
                    mysql.connection.commit()

            # check if the password is changed by comparing the input password with the password stored in database
            if password != original_account['Password']:
                # if password is changed, then the new password needs to be encrypted before inserting into databse
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute('UPDATE user SET Password=%s WHERE UserID=%s',(hashed, user_id))
                mysql.connection.commit()

            # update the other data to the database
            if user_type == 'customer':
                cursor.execute('UPDATE customer SET Email=%s, DisplayName = %s, Address = %s, PhoneNumber = %s WHERE customer.UserID = %s', (email, display_name, address, phone, user_id))
                mysql.connection.commit()
                return redirect(url_for('customer_list'))
            elif user_type == 'staff':
                cursor.execute('UPDATE staff SET Email=%s, DisplayName = %s, Address = %s, PhoneNumber = %s WHERE staff.UserID = %s', (email, display_name, address, phone, user_id))
                mysql.connection.commit()
                return redirect(url_for('staff_list'))
            else:
                return 'unauthorized'
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

            # delete a customer
            if user_to_delete['Role'] == 3:
                # Check if the customer has rented a car, 
                cursor.execute('SELECT * FROM car WHERE CustomerID in (SELECT CustomerID FROM customer WHERE customer.UserID=%s)',(userid,))
                rented_car = cursor.fetchall()
                if rented_car:
                    flash("Cannot delete customer who has rented a car.")
                    return redirect(url_for('customer_list'))
                else:
                    cursor.execute('DELETE FROM user WHERE UserID=%s',(userid,))
                    mysql.connection.commit()
                    flash("Delete successfully")
                    return redirect(url_for('customer_list'))
            # delete a staff
            elif user_to_delete['Role'] == 2:
                    cursor.execute('DELETE FROM user WHERE UserID=%s',(userid,))
                    mysql.connection.commit()
                    flash("Delete successfully")
                    return redirect(url_for('staff_list'))
            else:
                return 'unauthorized'
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
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if user_type == 'staff':
                cursor.execute('INSERT INTO user (UserName, Password, Role) VALUES (%s, %s, %s)',(username, hashed, 2))
                user_id = cursor.lastrowid
                cursor.execute('INSERT INTO staff (UserID, Email, DisplayName, Address, PhoneNumber) VALUES (%s,%s,%s,%s,%s)',(user_id, email, display_name, address, phone))
                mysql.connection.commit()
                flash("You have successfully added a staff!")
                return redirect(url_for('staff_list'))
            elif user_type == 'customer':
                cursor.execute('INSERT INTO user (UserName, Password, Role) VALUES (%s, %s, %s)',(username, hashed, 3))
                user_id = cursor.lastrowid
                cursor.execute('INSERT INTO customer (UserID, Email, DisplayName, Address, PhoneNumber) VALUES (%s,%s,%s,%s,%s)',(user_id, email, display_name, address, phone))
                mysql.connection.commit()
                flash("You have successfully added a customer!")
                return redirect(url_for('customer_list'))
            else:
                return 'unauthorized'
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
            customer_id = request.form.get('customer_id')
            # insert the data to the database
            sql = '''INSERT INTO car (CarModel, Year, RegNumber, SeatCap, RentalPerDay, CustomerID)
                    Values (%s, %s, %s, %s, %s, %s);'''
            parameters = (model, year, registration, seat_capacity, rental_per_day, customer_id)
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
            customer_id = request.form.get('customer_id')
            if customer_id == "":
                customer_id = None
            # insert the data to the database
            sql = '''UPDATE car 
                    SET CarModel = %s, Year = %s, RegNumber = %s, SeatCap = %s, RentalPerDay = %s, CustomerID = %s
                    WHERE CarID = %s;'''
            parameters = (car_model, year, registration_number, seat_cap, rental_per_day, customer_id, carid)
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