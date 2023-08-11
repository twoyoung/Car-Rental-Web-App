from car_rental_webapp import app, mysql
from flask import flash, render_template, request, redirect, url_for, session
import MySQLdb.cursors
import os
from werkzeug.utils import secure_filename
from util import is_authenticated, get_user_role, allowed_file

   


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
    

