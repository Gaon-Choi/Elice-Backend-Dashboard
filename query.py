from sqlalchemy import *
from models import User, Board, Article

from app import sql_session, session

import datetime
import hashlib
from SessionStore import SessionStore


RECORDS_PER_PAGE = 10

IP = '127.0.0.1'    # localhost
PORT = 6379
REDIS_URL = 'redis://{ip}:{port}'.format(ip=IP, port=PORT)


##### Helper Method #####

def check_duplicate_email(email: str):
    return sql_session.execute(
        select(func.count()).select_from(User).filter_by(email = email)
    )

def check_exist_board(board_name: str):
    return sql_session.execute(
        select(Board.bid).select_from(Board).filter_by(name = board_name)
    )

def check_exist_article(article_id: int):
    return sql_session.execute(
        select(Article.bid, Article.writer).select_from(Article).filter_by(aid = article_id)
    )

def organize_articles(articles: list):
    result = list()
    for article in articles:
        aid, title, content = article
        result.append({ "id": aid, "title": title, "contents": content })
    return result

def isValidEmail(email: str) -> bool:
    import re
    # regular expression for e-mail address form
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    
    if re.fullmatch(regex, email):
      return True
    
    return False

#########################

def signup(name: str, email: str, password: str):
    # check email format validity
    if (isValidEmail(email) is False):
        return {
            "result": 'invalid email address',
            "status": 400
        }
    
    # check whether email address is duplicated
    [duplicate_check] = check_duplicate_email(email).fetchone()
    if (duplicate_check > 0):
        return {
            "result": 'duplicate email detected',
            "status": 400
        }
    
    # SHA encryption
    password_ = hashlib.sha256(password.encode()).hexdigest()
    
    user = User(fullname = name, email = email, password = password_)
    sql_session.add(user)
    sql_session.commit()
    
    store = SessionStore(email, REDIS_URL)
    store.set('userEmail', email)
    store.set('userName', name)
    
    return {
        "result": {
            "fullname": name,
            "email": email
        },
        "status": 201   # 201 Created
    }


def login(email: str, password: str):
    # check if already logged-in
    if 'userId' in session:
        return {
            "result": 'A user already logged in.',
            "status": 200
        }
    
    # check email format validity
    if (isValidEmail(email) is False):
        return {
            "result": 'email address has invalid form.',
            "status": 400
        }
    
    query = select(User.uid, User.email, User.password).select_from(User).where(User.email == email)
    result = sql_session.execute(query).fetchone()
    
    if (result is None):
        # account with given email does not exist
        return {
            "result": 'User does not exist with given e-mail address',
            "status": 200
        }
    
    # account exists
    [user_id, user_email, user_password] = result

    if (user_password != password):
        return {
            "result": "Wrong password!",
            "status": 401
        }
    
    session['userId'] = user_id
    session['userEmail'] = user_email
    
    return {
        "result": {
            "userId": user_id,
            "userEmail": user_email
        },
        "status": 200
    }
    

def logout():
    if 'userId' not in session:
        return {
            "result": 'No user logged in',
            "status": 200
        }
    
    # drop "userId", "userEmail" keys from session
    session.pop('userId', None)
    session.pop('userEmail', None)
    
    return {
        "result": "Logged out successfully",
        "status": 200
    }


def board_list(page: int):
    query = select(Board.bid, Board.name).select_from(Board).order_by(Board.bid).offset(page * RECORDS_PER_PAGE).limit(RECORDS_PER_PAGE)
    result = sql_session.execute(query).fetchall()

    def tuple_to_dict(tuple_: tuple) -> dict:
        board_id, board_name = tuple_
        return { "bid": board_id, "name": board_name }
    
    result = list(map(tuple_to_dict, result))
    
    return {
        "result": result,
        "status": 200
    }


def create_board(board_name: str):
    if 'userId' not in session:
        return {
            "result": 'No user logged in',
            "status": 401
        }
        
    # check whether email address is duplicated
    duplicate_check = check_exist_board(board_name).fetchone()
    if (duplicate_check != None):
        return {
            "result": 'duplicate board name detected',
            "status": 400
        }
    
    board = Board(name = board_name)
    sql_session.add(board)
    sql_session.commit()
    
    return {
        "result": None,
        "status": 201   # 201 Created
    }
    
    
def rename_board(board_name: str, target_name: str):
    if 'userId' not in session:
        return {
            "result": 'No user logged in',
            "status": 401
        }
        
    # check whether the board exists with given name
    exist_check = check_exist_board(board_name).fetchone()
    if (exist_check == None):
        return {
            "result": 'no board detected with given name',
            "status": 400
        }
    
    # if the target name is equal to the board name, it is not efficient
    elif (board_name == target_name):
        return {
            "result": 'target name is the same with present name',
            "status": 400
        }
    
    query = update(Board).where(Board.name == board_name).values(name = target_name).execution_options(synchronize_session="fetch")
    sql_session.execute(query)
    sql_session.commit()

    return {
        "result": None,
        "status": 200
    }


def remove_board(board_name: str):
    if 'userId' not in session:
        return {
            "result": 'No user logged in',
            "status": 401
        }
        
    # check whether the board exists with given name
    exist_check = check_exist_board(board_name).fetchone()
    if (exist_check == None):
        return {
            "result": 'no board detected with given name',
            "status": 400
        }
    
    query = delete(Board).where(Board.name == board_name).execution_options(synchronize_session="fetch")
    sql_session.execute(query)
    sql_session.commit()
    
    return {
        "result": None,
        "status": 200
    }


def read_articles(board_name: str, page: int):
    # check whether the board exists with given name
    exist_bid = check_exist_board(board_name).fetchone()

    if (exist_bid == None):
        return {
            "result": 'no board detected with given name',
            "status": 400
        }
    
    [ exist_bid ] = exist_bid
    
    query = select(Article.aid, Article.title, Article.texts).select_from(Article).where(Article.bid == exist_bid).order_by(Article.aid).offset(page * RECORDS_PER_PAGE).limit(RECORDS_PER_PAGE)
    result = sql_session.execute(query).fetchall()
    result = organize_articles(result)
    
    return {
        "result": result,
        "status": 200
    }


def create_article(title: str, contents: str, bname: str):
    # check login user
    if 'userId' not in session:
        return {
            "result": 'No user logged in',
            "status": 401
        }
    
    # check whether the board exists with given name
    exist_bid = check_exist_board(bname).fetchone()
    if (exist_bid is None):
        return {
            "result": 'no board detected with given name',
            "status": 400
        }
    [exist_bid] = exist_bid
    
    query = insert(Article).values(
        board_id = exist_bid,
        title = title,
        contents = contents,
        writer = session['userId'],
        status = False
    )
    sql_session.execute(query)
    sql_session.commit()
    
    return {
        "result": {
            "title": title,
            "contents": contents
        },
        "status": 200
    }


def edit_article(article_id: int, title: str, contents: str):
    # check login user
    if 'userId' not in session:
        return {
            "result": 'No user logged in',
            "status": 401
        }
    
    # whether the article exists with given article id
    exist_aid, writer_id = check_exist_article(article_id).fetchone()
    if (exist_aid is None):
        return {
            "result": 'no article detected with given id',
            "status": 400
        }
    
    # check user's authority for editing article
    if (session['userId'] != writer_id):    # unauthorized
        return {
            "result": 'Unauthorized User.',
            "status": 401
        }
    
    # edit title and contents (PUT)
    query = update(Article).where(Article.aid == article_id).values(title = title, texts = contents)
    sql_session.execute(query)
    sql_session.commit()
    
    return {
        "result": {
            "title": title,
            "contents": contents
        },
        "status": 200
    }


def read_article(article_id: int):
    # check whether article exists with given article id
    exist_aid, writer_id = check_exist_article(article_id).fetchone()
    if (exist_aid is None):
        return {
            "result": 'no article detected with given id',
            "status": 400
        }
    
    query = select(Article.title, Article.texts, Article.date).select_from(Article).where(Article.aid == article_id, Article.status == False)
    title, contents, date = sql_session.execute(query).fetchone()
    
    return {
        "result": {
            "title": title,
            "contents": contents,
            "date": date
        },
        "status": 200
    }


def delete_article(article_id: int):
    # check login user
    if 'userId' not in session:
        return {
            "result": 'No user logged in',
            "status": 401
        }
        
    # check whether article exists with given article id
    exist_aid, writer_id = check_exist_article(article_id).fetchone()
    if (exist_aid is None):
        return {
            "result": 'no article detected with given id',
            "status": 400
        }
    
    # check user's authority for editing article
    if (session['userId'] != writer_id):    # unauthorized
        return {
            "result": 'Unauthorized User.',
            "status": 200
        }
        
    # mark as "deleted"
    query = update(Article).where(Article.aid == article_id).values(status = True)
    result = sql_session.execute(query)
    sql_session.commit()
    
    return {
        "result": None,
        "status": 200
    }

'''
    This method is intended to be used by the Administrator.
'''
def delete_article_s(article_id: int):
    # check whether article exists with given article id
    exist_aid = check_exist_article(article_id).fetchone()
    if (exist_aid is None):
        return {
            "result": 'no article detected with given id',
            "status": 400
        }
    
    query = delete(Article).where(Article.aid == article_id)
    result = sql_session.execute(query)
    sql_session.commit()
    
    return {
        "result": None,
        "status": 200
    }


def recent_articles(rpp: int):
    query = select(Board.bid).select_from(Board)
    board_ids = sql_session.execute(query).fetchall()
    
    result = dict()
    
    for [ board_id ] in board_ids:
        subquery = select(Article.title).select_from(Article).where(Article.bid == board_id, Article.status == False).order_by(desc(Article.date)).limit(rpp)
        sub_result = sql_session.execute(subquery).fetchall()
        
        # extract elements in tuple to form a complete list
        sub_result = [item for t in sub_result for item in t]
        
        # apend a title list to the dictionary
        result[board_id] = sub_result
    
    return {
        "result": result,
        "status": 200
    }
