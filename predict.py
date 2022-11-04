from flask import Flask, render_template, request , jsonify , session , url_for , redirect, flash

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

    # Set the pagination configuration
    page = request.args.get('page', 1, type=int)
    perpage=100
    startat=page*perpage


    cursor.execute('SELECT * FROM books limit %s, %s;', (startat,perpage))
    books = cursor.fetchall()

    cursor.execute('SELECT COUNT(*) as count FROM books')
    countBooks = cursor.fetchone()
    No_pages = int(round((countBooks['count'] / perpage)))

    return render_template('books.html', books = books,page=page,No_pages=No_pages)


def rate():
    if session.get('loggedin') != True: # if user is not logged 
        return redirect('/login') #redirect to login page

    if request.method == 'POST' and 'bookRate' in request.form and 'book_id' in request.form: 
        if 1 <= int(request.form['bookRate']) <= 5 : # Check Rate ( Allow only from 1 to 5)
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('SELECT * FROM books WHERE book_id = %s', (request.form['book_id'],)) #check database for book by id
            book = cursor.fetchone() 
            # check If book exist before moving on
            if book:
                # defining variables for user and book and rate
                userID = session.get('id')
                bookID = book['book_id']
                rate = request.form['bookRate']
                
                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
                # check if user rated this book by book id and user id
                cursor.execute('SELECT id FROM book_rates WHERE user_id = % s AND book_id = % s', (userID, bookID, ))
                checkRate = cursor.fetchone() 
                if checkRate: # check if user already rated this book
                    flash('You have Already rated this book, Thank you !')
                    return redirect('/books')

                #Insert the new rate in the database of the user
                cursor.execute('INSERT INTO book_rates VALUES (NULL, %s, %s, %s)', (userID, bookID, rate))
                mysql.connection.commit()

                ############## Starting model operations ##############
                ratings = pd.read_csv('data/Books.csv')
                
                #pivot_table function on a DataFrame will construct a user / book rating matrix
                bookRatings = ratings.pivot_table(index=['user_id'],columns=['book_name'],values='ratings')


                #users who rated book & entering input (book to search for similarity):
                try:
                    input = book['book_name']
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

                    recommendations = [firstBook , SecondBook , ThirdBook]
                except KeyError:
                    return render_template('notTrained.html')

                ############## End model operations ##############

                cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            # Get recommended books information from the Database
                cursor.execute('SELECT * FROM books WHERE book_name IN % s', (recommendations, ))
                recommendedBooks = cursor.fetchall()



                return render_template('result.html',recommendations = recommendedBooks,bookConcept = book['concept'])
            else:
                flash('This book does not exist , please try again')
                return redirect('/books')
    else:
        flash('an error occurred , please try again')
        return redirect('/books')

def statistics():
    ratings = pd.read_csv('data/Books.csv')
    BookStats = ratings.groupby('book_name').agg({'ratings': [np.size, np.mean]})
    df = BookStats.reset_index()  # make sure indexes pair with number of rows
    books_rates = df.to_numpy() # convert DataFrame to Array , So we can use it easily with our template
    books_count = len(books_rates)
    return render_template('statistics.html',books_rates=books_rates,books_count=books_count)
