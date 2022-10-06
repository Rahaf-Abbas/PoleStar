from flask import render_template
import pandas as pd

def index():
    return render_template("home.html")


def login():
    return render_template("login.html")


def register():
    return render_template("home.html")




