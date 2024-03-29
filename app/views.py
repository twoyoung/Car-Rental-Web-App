from app import app
from flask_mysqldb import MySQL
from flask import request, render_template, session, redirect, url_for, flash
import MySQLdb.cursors
import bcrypt
import re
import os
import bcrypt
from werkzeug.utils import secure_filename

# Intialize MySQL
mysql = MySQL(app)

# for uploading car images
# UPLOAD_FOLDER = './static/car_images'
UPLOAD_FOLDER = '/home/2young/COMP639-Rental-Car-Web-App/app/static/car_images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS

# function to judge if user has logged in
def is_authenticated():
    return 'loggedin' in session

# function to get user's role
def get_user_role():
    if session['role'] == 1:
        return 'admin'
    elif session['role'] == 3:
        return 'customer'
    elif session['role'] == 2:
        return 'staff'
    else:
        return 'guest'
    
# function to get all of user's information from userID
def get_account(userid):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    sql = '''SELECT * FROM
            (SELECT 
            user.UserID,
            user.UserName,
            user.Password,
            user.Role,
            user.Active,
            COALESCE(staff.StaffID, NULL) AS StaffID,
            COALESCE(customer.CustomerID, NULL) AS CustomerID,
            COALESCE(staff.Email, customer.Email) AS Email,
            COALESCE(staff.FirstName, customer.FirstName) AS FirstName,
            COALESCE(staff.LastName, customer.LastName) AS LastName,
            COALESCE(staff.PhoneNumber, customer.PhoneNumber) AS PhoneNumber,
            COALESCE(staff.Address, customer.Address) AS Address
            FROM user
            LEFT JOIN staff ON user.UserID = staff.UserID
            LEFT JOIN customer ON user.UserID = customer.UserID) AS user_customer_staff         
            WHERE Active = 1 and UserID = %s;'''
    cursor.execute(sql,(userid,))
    account = cursor.fetchone()
    return account

# function to check if username has already been registered
def username_crash(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE Active = 1 and UserName = %s', (username,))
    exist_account = cursor.fetchone()
        # If account exists show error and validation checks
    if exist_account:
        return 1
    else:
        return 0

# redirect all 404 pages to my bootstrapped one.
@app.errorhandler(404)
def pageNotFound(error):
    return render_template('404.html',user_role=session['role']), 404

# http://localhost:5000/ - display home page
@app.route('/')
def index():
    return render_template('index.html')


# http://localhost:5000/ - user login
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
            msg = 'Incorrect username!'
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


# http://localhost:5000/register - this will be the registration page
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
            return render_template('unauthorized.html', user_role=session['role'])
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))
    

# http://localhost:5000/home/car_list - Display list of cars with function of add/edit/delete for admin and staff
@app.route('/home/car_list')
def car_list():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['staff','admin']:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM car WHERE Active=1')
            car_list = cursor.fetchall()
            return render_template('car_list.html', car_list=car_list, user_role=session['role'])
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))


# http://localhost:5000/home/car/<carid> - View a car's detailed information
@app.route('/home/car/<carid>')
def check_car(carid):
    if is_authenticated():
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM car WHERE CarID = %s and Active = 1', (carid,))
        car = cursor.fetchone()
        if car:
            return render_template('car.html', car=car, user_role=session['role'])
            # return render_template('car_test.html')
        else:
            return render_template('404.html',user_role=session['role']), 404
    else:
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))
    

# http://localhost:5000/add/car - function to add a new car
@app.route('/add/car', methods=['GET', 'POST'])
def add_car():
    if is_authenticated():
        user_role = get_user_role()
        # only admin or staff can add a new car
        if user_role in ['admin','staff']:
            model = request.form.get('model')
            year = request.form.get('year')
            registration = request.form.get('registration')
            seat_capacity = request.form.get('seat_capacity')
            rental_per_day = request.form.get('rental_per_day')
            customer_id = request.form.get('customer_id')
            if not customer_id:
                customer_id = None
            carimage = ''
            if 'car_image' in request.files:
                file = request.files['car_image']
                if not file:
                    carimage = 'replace.gif'
                elif allowed_file(file.filename):
                    filename = secure_filename(file.filename)
                    file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                    carimage = file.filename
                else:
                    flash("To change the image, please select a valid image file (jpg, jpeg, png, gif).")
                    return redirect(url_for('car_list'))

            # insert the data to the database
            sql = '''INSERT INTO car (CarImage, CarModel, Year, RegNumber, SeatCap, RentalPerDay, CustomerID)
                    Values (%s, %s, %s, %s, %s, %s, %s);'''
            parameters = (carimage, model, year, registration, seat_capacity, rental_per_day, customer_id)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, parameters)
            mysql.connection.commit()
            flash("You have successfully added a car!",'success')
            return redirect(url_for('car_list'))
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        return redirect(url_for('login'))


# http://localhost:5000/update/car - function to edit a car's information
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
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if not customer_id:
                customer_id = None
            else:
                cursor.execute("SELECT CustomerID FROM customer WHERE Active = 1;")
                customerIDList = [row['CustomerID'] for row in cursor.fetchall()]
                if customer_id not in customerIDList:
                    flash("Failed updating car information. Customer ID does not exist.", "error")
                    return redirect(url_for('car_list'))
            cursor.execute('SELECT * from car WHERE CarID=%s',(carid,))
            car=cursor.fetchone()
            car_image = car['CarImage']
            file = request.files['car_image']
            if not file:
                carimage = car_image
            elif allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'],filename))
                carimage = file.filename
            else:
                flash("To change the image, please select a valid image file (jpg, jpeg, png, gif).")
                return redirect(url_for('car_list'))
            # insert the data to the database
            sql = '''UPDATE car 
                    SET CarImage = %s, CarModel = %s, Year = %s, RegNumber = %s, SeatCap = %s, RentalPerDay = %s, CustomerID = %s
                    WHERE CarID = %s;'''
            parameters = (carimage, car_model, year, registration_number, seat_cap, rental_per_day, customer_id, carid)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(sql, parameters)
            mysql.connection.commit()
            flash('Car information changed successfully!','success')
            return redirect(url_for('car_list'))
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        return redirect(url_for('login'))


# http://localhost:5000//delete/car/<carid> - function to delete a car
@app.route('/delete/car/<carid>')
def delete_car(carid):
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin','staff']:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('UPDATE car SET Active=%s WHERE CarID=%s',(0,carid))
            mysql.connection.commit()
            flash("Delete successfully!",'success')
            return redirect(url_for('car_list'))
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        return redirect(url_for('login'))


# http://localhost:5000/profile - this will be the profile page, only accessible for loggedin users 
@app.route('/profile')
def profile():
    # Check if user is loggedin
    if is_authenticated():
        user_role = get_user_role()
        # We need all the account info for the user so we can display it on the profile page
        account = get_account(session['id'])
        # Show the profile page with account info
        return render_template('profile.html', account=account,user_role=session['role'])
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))
    
# http://localhost:5000/profile/<userid> - check user's profile by userID
@app.route('/profile/<userid>')
def check_profile(userid):
    # Check if user is loggedin
    if is_authenticated():
        account = get_account(userid)
        userid = int(userid)
        if account:
            user_role = get_user_role()
            # admin can check any user's profile
            if user_role == 'admin':
                return render_template('profile.html', account=account,user_role=session['role'])
            # staff can only check customers' or own profile
            elif user_role == 'staff':
                if account['Role'] == 3 or userid == session['id']:
                    return render_template('profile.html', account=account,user_role=session['role'])
                else:
                    return render_template('unauthorized.html', user_role=session['role'])
            # customer can only check own profile
            elif user_role == 'customer':
                if session['id'] == userid:
                    return render_template('profile.html', account=account,user_role=session['role'])
                else:
                    return render_template('unauthorized.html', user_role=session['role'])
            else:
                return render_template('unauthorized.html', user_role=session['role'])
        else:
            return render_template('404.html',user_role=session['role']), 404
    else:
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))


# http://localhost:5000/edit/profile/<userid> - function for admin to change password
@app.route('/edit/profile/<userid>')
def change_password(userid):
    userid = int(userid)
    if is_authenticated():
        if session['id'] == 1:
            account = get_account(userid)
            return render_template('change_password.html',account=account,user_role=session['role']) 
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))


# http://localhost:5000/update/profile - function to edit profile information 
@app.route('/update/profile', methods=['GET', 'POST'])
def update_profile():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin','staff','customer']:
            userid = request.form.get('user_id')
            username = request.form.get('username')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')
            password = request.form.get('password')
            account = get_account(userid)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #if username is changed:
            if username != account['UserName']:
                #check if username already exists in database
                if username_crash(username):
                    flash('Username already exists. Please choose a different username.','error')
                    return redirect(url_for('check_profile',userid=userid))
                else:
                    cursor.execute('UPDATE user SET UserName=%s WHERE UserID=%s',(username, userid))
                    mysql.connection.commit()

            # check if the password is changed by comparing the input password with the password stored in database
            if password != account['Password']:
                # if password is changed, then the new password needs to be encrypted before inserting into databse
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute('UPDATE user SET Password=%s WHERE UserID=%s',(hashed, userid))
                mysql.connection.commit()

            if account['Role'] == 3:
                cursor.execute('UPDATE customer SET Email=%s,FirstName=%s,LastName=%s,PhoneNumber=%s,Address=%s WHERE customer.UserID=%s',(email,firstname,lastname,phone,address,userid))
                mysql.connection.commit()
                flash('Profile information changed successfully!','success')
                return redirect(url_for('check_profile',userid=userid))
            elif account['Role'] == 2:
                cursor.execute('UPDATE staff SET Email=%s,FirstName=%s,LastName=%s,PhoneNumber=%s,Address=%s WHERE staff.UserID = %s', (email,firstname,lastname,phone,address,userid))
                mysql.connection.commit()
                flash('Profile information changed successfully!','success')
                return redirect(url_for('check_profile',userid=userid))
            elif account['Role'] == 1:
                flash('Profile information changed successfully!','success')
                return redirect(url_for('check_profile',userid=userid))
            else:
                return render_template('unauthorized.html', user_role=session['role'])
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        return redirect(url_for('login'))
    

# http://localhost:5000/home/customer_list - admin or staff can view all the customers
@app.route('/home/customer_list')
def customer_list():
    if is_authenticated():
        user_role = get_user_role()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM customer LEFT JOIN user ON customer.UserID = user.UserID WHERE user.Active=1')
        customer_list = cursor.fetchall()
        if user_role in ['admin','staff']:
            return render_template('customer_list.html', customer_list=customer_list, user_role=session['role']) 
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        return redirect(url_for('login'))


# http://localhost:5000/home/staff_list - admin can view the staff list
@app.route('/home/staff_list')
def staff_list():
    if is_authenticated():
        user_role = get_user_role()
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM staff LEFT JOIN user ON staff.UserID = user.UserID WHERE user.Active = 1')
        staff_list = cursor.fetchall()
        if user_role == 'admin':
            return render_template('staff_list.html', staff_list=staff_list, user_role=session['role'])
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        return redirect(url_for('login'))
    

 # http://localhost:5000/update/user - admin can edit customer or staff's information
@app.route('/update/user', methods=['GET', 'POST'])
def update_user():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin']:
            userid = request.form.get('user_id')
            username = request.form.get('username')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')
            password = request.form.get('password')

            account = get_account(userid)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            #if username is changed:
            if username != account['UserName']:
                #check if username already exists in database
                if username_crash(username):
                    flash('Failed. Username already exists. Please choose a different username.','error')
                    if account['Role']== 3:
                        return redirect(url_for('customer_list'))
                    elif account['Role'] == 2:
                        return redirect(url_for('staff_list'))
                    else:
                        return render_template('unauthorized.html', user_role=session['role'])
                else:
                    cursor.execute('UPDATE user SET UserName=%s WHERE UserID=%s',(username, userid))
                    mysql.connection.commit()

            # check if the password is changed by comparing the input password with the password stored in database
            if password != account['Password']:
                # if password is changed, then the new password needs to be encrypted before inserting into databse
                hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
                cursor.execute('UPDATE user SET Password=%s WHERE UserID=%s',(hashed, userid))
                mysql.connection.commit()

            # update the other data to the database
            if account['Role']== 3:
                cursor.execute('UPDATE customer SET Email=%s,FirstName=%s,LastName=%s,PhoneNumber=%s,Address=%s WHERE customer.UserID=%s', (email,firstname,lastname,phone,address,userid))
                mysql.connection.commit()
                flash('Information updated successfully!','success')
                return redirect(url_for('customer_list'))
            elif account['Role'] == 2:
                cursor.execute('UPDATE staff SET Email=%s,FirstName=%s,LastName=%s,PhoneNumber=%s,Address=%s WHERE staff.UserID = %s', (email,firstname,lastname,phone,address,userid))
                mysql.connection.commit()
                flash('Information updated successfully!','success')
                return redirect(url_for('staff_list'))
            else:
                return render_template('unauthorized.html', user_role=session['role'])
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        return redirect(url_for('login'))


 # http://localhost:5000/delete/user/<userid> - admin can delete a customer or staff
@app.route('/delete/user/<userid>')
def delete_user(userid):
    if is_authenticated():
        user_role = get_user_role()
        if user_role == 'admin':
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM user WHERE UserID=%s and Active = 1',(userid,))
            user_to_delete = cursor.fetchone()

            # delete a customer
            if user_to_delete['Role'] == 3:
                # Check if the customer has rented a car, 
                cursor.execute('SELECT * FROM car WHERE Active = 1 and CustomerID in (SELECT CustomerID FROM customer WHERE customer.UserID=%s)',(userid,))
                rented_car = cursor.fetchall()
                if rented_car:
                    flash('Cannot delete customer who has rented a car.','error')
                    return redirect(url_for('customer_list'))
                else:
                    cursor.execute('UPDATE user SET Active=%s WHERE UserID=%s',(0,userid))
                    cursor.execute('UPDATE customer SET Active=%s WHERE UserID=%s',(0,userid))
                    mysql.connection.commit()
                    flash('Delete successfully!','success')
                    return redirect(url_for('customer_list'))
            # delete a staff
            elif user_to_delete['Role'] == 2:
                    cursor.execute('UPDATE user SET Active=%s WHERE UserID=%s',(0,userid,))
                    cursor.execute('UPDATE staff SET Active=%s WHERE UserID=%s',(0,userid))
                    mysql.connection.commit()
                    flash('Delete successfully!','success')
                    return redirect(url_for('staff_list'))
            else:
                return render_template('unauthorized.html', user_role=session['role'])
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        return redirect(url_for('login'))
    

# http://localhost:5000/add/user - admin can add a new customer or staff
@app.route('/add/user', methods=['Get', 'POST'])
def add_user():
    if is_authenticated():
        user_role = get_user_role()
        if user_role == 'admin':
            username = request.form.get('username')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')
            password = request.form.get('password')
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            user_type = int(request.form.get('user_type'))
            if username_crash(username):
                    flash('Failed. Username already exists. Please choose a different username.','error')
                    if user_type == 3:
                        return redirect(url_for('customer_list'))
                    elif user_type == 2:
                        return redirect(url_for('staff_list'))
                    else:
                        return render_template('unauthorized.html', user_role=session['role'])
            # insert the data to the database
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            if user_type == 2:
                cursor.execute('INSERT INTO user (UserName, Password, Role) VALUES (%s, %s, %s)',(username, hashed, 2))
                user_id = cursor.lastrowid
                cursor.execute('INSERT INTO staff (UserID,Email,FirstName,LastName,PhoneNumber,Address) VALUES (%s,%s,%s,%s,%s,%s)',(user_id,email,firstname,lastname,phone,address))
                mysql.connection.commit()
                flash("You have successfully added a staff!",'success')
                return redirect(url_for('staff_list'))
            elif user_type == 3:
                cursor.execute('INSERT INTO user (UserName, Password, Role) VALUES (%s, %s, %s)',(username, hashed, 3))
                user_id = cursor.lastrowid
                cursor.execute('INSERT INTO customer (UserID,Email,FirstName,LastName,PhoneNumber,Address) VALUES (%s,%s,%s,%s,%s,%s)',(user_id,email,firstname,lastname,phone,address))
                mysql.connection.commit()
                flash("You have successfully added a customer!",'success')
                return redirect(url_for('customer_list'))
            else:
                return render_template('unauthorized.html', user_role=session['role'])
        else:
            return render_template('unauthorized.html', user_role=session['role'])
    else:
        return redirect(url_for('login'))

