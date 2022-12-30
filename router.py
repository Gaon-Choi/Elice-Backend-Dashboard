from flask import render_template, request, Blueprint
import query

page = Blueprint('app_page', __name__)

@page.route('/')
def home():
    return render_template('layout.html')


@page.route('/user/<path:path>', methods = ['POST'])
def user(path):
    if path == 'signup':
        params = request.get_json()
        name = params['name']
        email = params['email']
        password = params['password']
        return query.signup(name, email, password)
    
    elif path == 'login':
        params = request.get_json()
        email = params['email']
        password = params['password']
        return query.login(email, password)
    
    elif path == 'logout':
        return query.logout()
    
    # invalid path
    return {
        "result": None,
        "status": 400
    }


@page.route('/boardlist', methods=['GET'])
def boardlist():
    page = request.args.get('page', type=int, default=1)
    return query.board_list(page)


@page.route('/board/<board_name>', methods=['PUT', 'PATCH', 'DELETE', 'GET'])
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


@page.route('/article', methods=['POST', 'PUT'])
def article():
    params = request.get_json()
    title = params['title']
    contents = params['contents']
    if (request.method == 'POST'):
        bname = params['board_name']
        return query.create_article(title, contents, bname)
    
    elif (request.method == 'PUT'):
        article_id = params['article_id']
        return query.edit_article(article_id, title, contents)
    
@page.route('/article/<article_id>', methods = ['GET', 'PATCH'])
def article_contents(article_id: int):
    if (request.method == 'GET'):
        return query.read_article(article_id)

    elif (request.method == 'PATCH'):
        return query.delete_article(article_id)


@page.route('/article/delete/<article_id>', methods = ['DELETE'])
def article_delete(article_id: int):
    return query.delete_article_s(article_id)

@page.route('/article/recent/<rpp>', methods = ['GET'])
def article_recent(rpp: int):
    rpp = abs(int(rpp)) # use absolute value if negative
    return query.recent_articles(rpp)