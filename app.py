import pandas as pd
from flask import Flask, request , url_for, session , redirect
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


#import pages
import home , predict

# Declare a Flask app
app = Flask(__name__)

app.secret_key = '6e63626d17f55cc6b73d019d'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'polestar'
 
mysql = MySQL(app)

# App Routes (pages)
app.add_url_rule('/', view_func=home.index , methods=['GET'])
app.add_url_rule('/login', view_func=home.login , methods=['GET', 'POST'])
app.add_url_rule('/register', view_func=home.register , methods=['GET', 'POST'])

    
@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('login'))

app.add_url_rule('/books', view_func=predict.books , methods=['GET'])
app.add_url_rule('/rate', view_func=predict.rate , methods=['POST'])


# Running the app
if __name__ == '__main__':
    app.run(debug = True)