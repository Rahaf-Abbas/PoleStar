from flask import Flask, render_template, request , jsonify , session , url_for , redirect
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
    if session.get('loggedin') == True: # if user is logged in don't allow him to enter login page
            return redirect('/') #redirect to home page

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form: 
                       
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['loggedin'] = True
            session['id'] = account['id']
            session['username'] = account['username']
            session['email'] = account['email']

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
    if session.get('loggedin') == True: # if user is logged in don't allow him to enter login page
            return redirect('/') #redirect to home page
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:

        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
         # Check if account exists using MySQL
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM users WHERE email = %s', (email,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            response = [
            { 't': 'Sorry', 'm': 'Account already exists!' , 'tp': 'error' }
            ]   
            return jsonify(response)
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            response = [
            { 't': 'Sorry', 'm': 'Invalid email address!' , 'tp': 'error' }
            ]   
            return jsonify(response)

        elif not re.match(r'[A-Za-z0-9]+', username):
            response = [
            { 't': 'Sorry', 'm': 'Username must contain only characters and numbers!' , 'tp': 'error' }
            ]   
            return jsonify(response)

        elif not username or not password or not email:
            response = [
            { 't': 'Sorry', 'm': 'Please fill out the form' , 'tp': 'error' }
            ]   
            return jsonify(response)
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO users VALUES (NULL, %s, %s, %s)', (username, email, password))
            mysql.connection.commit()
            response = [
            { 't': 'Successfully', 'm': 'You have successfully registered!' , 'tp': 'success' }
            ]   
            return jsonify(response)

    elif request.method == 'POST':
        # Form is empty... (no POST data)
        response = [
            { 't': 'Sorry', 'm': 'Please fill out the form' , 'tp': 'error' }
            ]   
        return jsonify(response)

    else:
        return render_template('register.html')
    






