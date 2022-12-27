from flask import Flask, render_template, url_for, flash, redirect
from sqlalchemy import create_engine
import redis
import os
import models

app = Flask(__name__)
app.config["SECRET_KEY"] = 'd2707fea9778e085491e2dbbc73ff30e'

db_string = "postgresql://developer:devpassword@127.0.0.1:25000/developer"

engine = create_engine(db_string, echo=True)

@app.route('/')
def home():
    return render_template('layout.html')


@app.route('/user', defaults={'path': ''})
@app.route('/user/<path:path>')
def user(path):
    if path == 'signup':
        print('login')
    elif path == 'login':
        print('sign up')
    elif path == 'logout':
        print('log out')
    return ('heoo', 200)

if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)
    app.run(debug=True)