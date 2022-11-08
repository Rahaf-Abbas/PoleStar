import pandas as pd
from flask import Flask , url_for, session , redirect
from flask_mysqldb import MySQL



#import pages
import home , predict , admin

# Declare a Flask app
app = Flask(__name__)

app.secret_key = '6e63626d17f55cc6b73d019d'
 
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'polestar'
 
mysql = MySQL(app)

# App Routes (pages)

# Start Auth Routes
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

#End Auth Routes


# Start Model Routes

app.add_url_rule('/books', view_func=predict.books , methods=['GET'])
app.add_url_rule('/rate', view_func=predict.rate , methods=['POST'])
app.add_url_rule('/statistics', view_func=predict.statistics , methods=['GET'])

# End Model Routes


## Start Admin Routes (pages)

app.add_url_rule('/admin/login', view_func=admin.Alogin , methods=['GET','POST'])
app.add_url_rule('/admin/logout', view_func=admin.Alogout , methods=['GET'])

app.add_url_rule('/admin/main', view_func=admin.main , methods=['GET'])

app.add_url_rule('/admin/books', view_func=admin.Abooks , methods=['GET','POST'])
app.add_url_rule('/admin/AddBook', view_func=admin.AddBook , methods=['GET','POST'])

app.add_url_rule('/admin/users', view_func=admin.Users , methods=['GET'])

## End Admin Routes (pages)


# Running the app
if __name__ == '__main__':
    app.run(debug = True)