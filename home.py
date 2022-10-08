from flask import Flask, render_template, request , jsonify , session
import pandas as pd

from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

# Declare a Flask app
app = Flask(__name__)

app.secret_key = '6e63626d17f55cc6b73d019d'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'polestar'
 
mysql = MySQL(app)

def index():
    return render_template("home.html")


def login():
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:                        
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            response = [
            { 't': 'Successfully', 'm': 'you have Logged in' , 'tp': 'success' }
            ]   
            return jsonify(response)
        else:
            response = [
            { 't': 'Sorry', 'm': 'these credentials do not match' , 'tp': 'error' }
            ]   
            return jsonify(response)
    else:
        return render_template('login.html')

def register():
    return render_template("home.html")




