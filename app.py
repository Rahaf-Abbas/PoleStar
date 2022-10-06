import pandas as pd
from flask import Flask, request


#import pages
import home

# Declare a Flask app
app = Flask(__name__)

# App Routes (pages)
app.add_url_rule('/', view_func=home.index , methods=['GET'])
app.add_url_rule('/login', view_func=home.login , methods=['GET', 'POST'])
app.add_url_rule('/register', view_func=home.register , methods=['GET', 'POST'])

app.add_url_rule('/rate', view_func=home.index , methods=['GET', 'POST'])
app.add_url_rule('/show', view_func=home.index , methods=['GET', 'POST'])
app.add_url_rule('/test', view_func=home.index , methods=['GET', 'POST'])


# Running the app
if __name__ == '__main__':
    app.run(debug = True)