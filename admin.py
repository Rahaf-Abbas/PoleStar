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

def Alogin():
    if session.get('Admin_loggedin') == True: # if user is logged in don't allow him to enter login page
            return redirect('/admin/main') #redirect to home page

    if request.method == 'POST' and 'email' in request.form and 'password' in request.form: 
                       
        email = request.form['email']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM admins WHERE email = % s AND password = % s', (email, password, ))
        account = cursor.fetchone()
        if account:
            session['Admin_loggedin'] = True
            session['Admin_id'] = account['admin_id']
            session['Admin_username'] = account['username']
            session['Admin_email'] = account['email']

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
        return render_template("admin/login.html")

def main():
    if session.get('Admin_loggedin') != True: # if admin is not logged 
            return redirect('/admin/login') #redirect to login page

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT COUNT(*) as count FROM books')
    countBooks = cursor.fetchone()

    cursor.execute('SELECT COUNT(*) as count FROM users')
    countUsers = cursor.fetchone()

    cursor.execute('SELECT COUNT(*) as count FROM book_rates')
    countRates = cursor.fetchone()

    return render_template("admin/main.html",countBooks=countBooks['count'],countUsers=countUsers['count'],countRates=countRates['count'])


def Alogout():
    # Remove session data, this will log the admin out
   session.pop('Admin_loggedin', None)
   session.pop('Admin_id', None)
   session.pop('Admin_username', None)
   # Redirect to login page
   return redirect('/admin/login')

def Abooks():
    if session.get('Admin_loggedin') != True: # if admin is not logged 
        return redirect('/admin/login') #redirect to login page

    if request.method == 'POST' and 'book_id' in request.form: 
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM books WHERE book_id = %s', (request.form['book_id'],)) #check database for book by id
        book = cursor.fetchone() 
        # check If book exist before moving on
        if book:
            # First Deleting rates for this book by id
            cursor.execute('DELETE FROM book_rates WHERE book_id = %s', (request.form['book_id'],))
            mysql.connection.commit()
            # Deleting the book by id
            cursor.execute('DELETE FROM books WHERE book_id = %s', (request.form['book_id'],))
            mysql.connection.commit()

            response = [
            { 't': 'Successfully', 'm': 'Book Deleted' , 'tp': 'success' }
            ]   
            return jsonify(response)
        else:
            response = [
            { 't': 'Successfully', 'm': 'Book not found' , 'tp': 'error' }
            ]   
            return jsonify(response)


    else:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM books')
        books = cursor.fetchall()

        return render_template('admin/books.html', books = books)

def AddBook():
    if session.get('Admin_loggedin') != True: # if admin is not logged 
        return redirect('/admin/login') #redirect to login page

    if request.method == 'POST' and 'name' in request.form and 'img' in request.form and 'page' in request.form and 'lang' in request.form and 'concept' in request.form and 'tool' in request.form and 'author' in request.form and 'des' in request.form:  
    
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO books VALUES (NULL, %s, %s, %s, %s, %s, %s, %s , %s)', (request.form['name'], request.form['img'], request.form['page'],request.form['lang'],request.form['concept'],request.form['tool'],request.form['author'],request.form['des']))
        mysql.connection.commit()

        response = [
        { 't': 'Successfully', 'm': 'Book Added successfully' , 'tp': 'success' }
        ]   
        return jsonify(response)


    else:
        return render_template('admin/AddBook.html')


def Users():
    if session.get('Admin_loggedin') != True: # if admin is not logged 
        return redirect('/admin/login') #redirect to login page

    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM users')
    users = cursor.fetchall()

    return render_template('admin/Users.html', users = users)
