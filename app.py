from flask import Flask, render_template, url_for, flash, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import redis
import os
import models

app = Flask(__name__)
app.config["SECRET_KEY"] = 'd2707fea9778e085491e2dbbc73ff30e'

db_string = "postgresql://developer:devpassword@127.0.0.1:25000/developer"

engine = create_engine(db_string, echo=True)
session = Session(bind=engine)

@app.route('/')
def home():
    return render_template('layout.html')


@app.route('/user', defaults={'path': ''})
@app.route('/user/<path:path>')
def user(path):
    print(params['name'])
    params = request.get_json()
    if path == 'signup':
        name = params['name']
        email = params['email']
        password = params['password']
        return signup(name, email, password)
    elif path == 'login':
        email = params['name']
        password = params['password']
        return login(email, password)
    elif path == 'logout':
        return logout()
    return ('heoo', 200)

def signup(name: str, email: str, password: str):
    pass

def login(email: str, password: str):
    pass

def logout():
    pass

if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)
    app.run(debug=True)