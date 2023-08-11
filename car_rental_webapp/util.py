from car_rental_webapp import app
from flask import session
from flask_mysqldb import MySQL
import MySQLdb.cursors


# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'anystring'

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


UPLOAD_FOLDER = './static/car_images'
# UPLOAD_FOLDER = '/home/2young/COMP639-Rental-Car-Web-App/car-rental-webapp/static/car_images'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.',1)[1].lower() in ALLOWED_EXTENSIONS


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
        return 'guest'
    
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

def username_crash(username):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM user WHERE Active = 1 and UserName = %s', (username,))
    exist_account = cursor.fetchone()
        # If account exists show error and validation checks
    if exist_account:
        return 1
    else:
        return 0