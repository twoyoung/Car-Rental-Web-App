from flask import Flask

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'anystring'

# Enter your database connection details below
app.config['MYSQL_HOST'] = '2young.mysql.pythonanywhere-services.com'
app.config['MYSQL_USER'] = '2young'
app.config['MYSQL_PASSWORD'] = 'YouCantGuessIt'
app.config['MYSQL_DB'] = '2young$COMP639'
app.config['MYSQL_PORT'] = 3306

# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = ''
# app.config['MYSQL_DB'] = 'rental'
# app.config['MYSQL_PORT'] = 3306

from . import views


