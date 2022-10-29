from flask import Flask, render_template, request , jsonify , session , url_for , redirect
import pandas as pd
import numpy as np

from flask_mysqldb import MySQL
import MySQLdb.cursors
import re


app = Flask(__name__)

app.secret_key = '6e63626d17f55cc6b73d019d'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'polestar'
 
mysql = MySQL(app)

def books():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM books')
    books = cursor.fetchall()

    return render_template('books.html', books = books)

def test():
    ratings = pd.read_csv('data/Books.csv')
    
    #pivot_table function on a DataFrame will construct a user / book rating matrix
    bookRatings = ratings.pivot_table(index=['user_id'],columns=['book_name'],values='ratings')


    #users who rated book & entering input (book to search for similarity):
    input = "OpenVPN Cookbook - Second Edition"
    x = bookRatings[input]

    # corrwith function makes it really easy to compute the pairwise correlation
    # Showing the relation between the books and other books based on rating

    similarBooks = bookRatings.corrwith(x)
    similarBooks = similarBooks.dropna()

    # Getting the Similar Books according to the rating and users
    similarBooks.sort_values(ascending=False)

    # get rid of the unpopluar books who may mess up our results (missing more rating).
    # counts up how many ratings exist for each book and the average rate.

    BookStats = ratings.groupby('book_name').agg({'ratings': [np.size, np.mean]})

    #get rid of any books rated by fewer than 40 people, and check the top-rated ones that are left
    popularBooks = BookStats['ratings']['size'] >= 40
    BookStats[popularBooks].sort_values([('ratings', 'mean')], ascending=False)[:15]

    # Applying the new List of books (has 40 rating at least) to results
    df = BookStats[popularBooks].join(pd.DataFrame(similarBooks, columns=['similarity']))

    # taking Top 3 books based on similarity for our specfied book (input best match) 
    results = df.sort_values(['similarity'], ascending=False)[1:4]

    firstBook = results[:1].index[0]
    SecondBook = results[1:2].index[0]
    ThirdBook = results[2:3].index[0]

    output = [firstBook , SecondBook , ThirdBook]
    return render_template('predict.html', output = output)
 