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
    return render_template("AdminLogin.html")
