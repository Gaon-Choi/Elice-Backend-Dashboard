from flask import Flask, render_template, url_for, flash, redirect, request
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import redis
import os
import models
import query


app = Flask(__name__)
app.config["SECRET_KEY"] = 'd2707fea9778e085491e2dbbc73ff30e'

db_string = "postgresql://developer:devpassword@127.0.0.1:25000/developer"

engine = create_engine(db_string, echo=True)
session = Session(bind=engine)

@app.route('/')
def home():
    return render_template('layout.html')


@app.route('/user', defaults={'path': ''})
@app.route('/user/<path:path>', methods = ['PUT', 'GET', 'PATCH'])
def user(path):
    params = request.get_json()
    if path == 'signup':
        name = params['name']
        email = params['email']
        password = params['password']
        return query.signup(name, email, password)
    
    elif path == 'login':
        email = params['name']
        password = params['password']
        return query.login(email, password)
    
    elif path == 'logout':
        return query.logout()
    
    # invalid path
    return {
        "result": None,
        "status": 400
    }


@app.route('/boardlist', methods=['GET'])
def boardlist():
    page = request.args.get('page', type=int, default=1)
    return query.board_list(page)


@app.route('/board/<board_name>', methods=['PUT', 'PATCH', 'DELETE', 'GET'])
def board(board_name):
    # create new board
    if (request.method == 'PUT'):
        return query.create_board(board_name)
    
    # rename board with given name
    elif (request.method == 'PATCH'):
        params = request.get_json()
        target_name = params['target_name']
        return query.rename_board(board_name, target_name)
    
    # delete a board with given name
    elif (request.method == 'DELETE'):
        return query.remove_board(board_name)
    
    # read articles from a board with given name (paginated)
    elif (request.method == 'GET'):
        page = request.args.get('page', type=int, default=1)
        return query.read_articles(board_name, page)
    
    # invalid path
    return {
        "result": None,
        "status": 400
    }


@app.route('/article', methods=['POST', 'PATCH'])
def article():
    params = request.get_json()
    title = params['title']
    contents = params['contents']
    if (request.method == 'POST'):
        bname = params['board_name']
        return query.create_article(title, contents, bname)
    
    elif (request.method == 'PATCH'):
        article_id = params['article_id']
        return query.edit_article(article_id, title, contents)
    
@app.route('/article/<article_id>', methods = ['GET', 'PATCH'])
def article_contents(article_id: int):
    if (request.method == 'GET'):
        return query.read_article(article_id)

    elif (request.method == 'PATCH'):
        return query.delete_article(article_id)


@app.route('/article/delete/<article_id>', methods = ['DELETE'])
def article_delete(article_id: int):
    return query.delete_article_s(article_id)

if __name__ == '__main__':
    models.Base.metadata.create_all(bind=engine)
    app.run(debug=True)