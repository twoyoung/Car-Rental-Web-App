from car_rental_webapp import app

from flask import flash, render_template, request, redirect, url_for, session
import MySQLdb.cursors
import os
import bcrypt
from werkzeug.utils import secure_filename
from util import is_authenticated, get_user_role, allowed_file
from util import get_account, mysql,username_crash

   


@app.route('/home/car_list')
def car_list():
    if is_authenticated():
        user_role = get_user_role()
        # if  user_role == 'customer':
        #     cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #     cursor.execute('SELECT * FROM car WHERE CustomerID is NULL and Active=1')
        #     car_list = cursor.fetchall()
        #     return render_template('car_list_customer.html', car_list=car_list, user_role=user_role )
        if user_role in ['staff','admin']:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM car WHERE Active=1')
            car_list = cursor.fetchall()
            return render_template('car_list.html', car_list=car_list, user_role=session['role'])
        else:
            return render_template('unauthorized.html')
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))


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
            return "404"
    else:
    # User is not loggedin redirect to login page
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
            return render_template('unauthorized.html')
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
            if not customer_id:
                customer_id = None
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * from car WHERE CarID=%s',(carid,))
            car=cursor.fetchone()
            print(car)
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
            return render_template('unauthorized.html')
    else:
        return redirect(url_for('login'))

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
            return render_template('unauthorized.html')
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
    
@app.route('/profile/<userid>')
def check_profile(userid):
    # Check if user is loggedin
    if is_authenticated():
        account = get_account(userid)
        userid = int(userid)
        if account:
            user_role = get_user_role()
            if user_role == 'admin':
                # We need all the account info for the user so we can display it on the profile page
                # Show the profile page with account info
                return render_template('profile.html', account=account,user_role=session['role'])
            elif user_role == 'staff':
                if account['Role'] == 3 or userid == session['id']:
                    return render_template('profile.html', account=account,user_role=session['role'])
                else:
                    return render_template('unauthorized.html')
            elif user_role == 'customer':
                if session['id'] == userid:
                    return render_template('profile.html', account=account,user_role=session['role'])
                else:
                    return render_template('unauthorized.html')
            else:
                return render_template('unauthorized.html')
        else:
            return "404"
    else:
    # User is not loggedin redirect to login page
        return redirect(url_for('login'))
    
    
@app.route('/edit/profile/<userid>')
def change_password(userid):
    account=get_account(userid)
    userid = int(userid)
    if is_authenticated():
        if session['id'] == 1:
            user_role = get_user_role()
            account = get_account(userid)
            return render_template('change_password.html',account=account,user_role=session['role']) 
        else:
            return render_template('unauthorized.html')
    else:
        # User is not loggedin redirect to login page
        return redirect(url_for('login'))

    
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
                return render_template('unauthorized.html')
        else:
            return render_template('unauthorized.html')
    else:
        return redirect(url_for('login'))
    

    
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
            return render_template('unauthorized.html')
    else:
        return redirect(url_for('login'))

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
            return render_template('unauthorized.html')
    else:
        return redirect(url_for('login'))
    
@app.route('/update/user', methods=['GET', 'POST'])
def update_user():
    if is_authenticated():
        user_role = get_user_role()
        if user_role in ['admin']:
            userid = request.form.get('user_id')
            print(userid)
            username = request.form.get('username')
            firstname = request.form.get('firstname')
            lastname = request.form.get('lastname')
            phone = request.form.get('phone')
            email = request.form.get('email')
            address = request.form.get('address')
            password = request.form.get('password')

            account = get_account(userid)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            print(account)
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
                        return render_template('unauthorized.html')
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
                return render_template('unauthorized.html')
        else:
            return render_template('unauthorized.html')
    else:
        return redirect(url_for('login'))

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
                return render_template('unauthorized.html')
        else:
            return render_template('unauthorized.html')
    else:
        return redirect(url_for('login'))
     
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
                        return render_template('unauthorized.html')
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
                return render_template('unauthorized.html')
        else:
            return render_template('unauthorized.html')
    else:
        return redirect(url_for('login'))

