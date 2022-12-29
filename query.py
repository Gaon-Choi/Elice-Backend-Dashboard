from sqlalchemy import *
from models import User, Board, Article

from app import session

import datetime
import hashlib

RECORDS_PER_PAGE = 10

##### Helper Method #####

def check_duplicate_email(email: str):
    return session.execute(
        select(func.count()).select_from(User).filter_by(email = email)
    )

def check_exist_board(board_name: str):
    return session.execute(
        select(Board.bid).select_from(Board).filter_by(name = board_name)
    )

def check_exist_article(article_id: int):
    return session.execute(
        select(Article.bid).select_from(Article).filter_by(aid = article_id)
    )

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
    session.add(user)
    session.commit()
    
    return {
        "result": None,
        "status": 201   # 201 Created
    }


def login(email: str, password: str):
    # check email format validity
    if (isValidEmail(email) is False):
        return {
            "result": None,
            "status": 400
        }
    pass


def logout():
    pass


def board_list(page: int):
    query = select(Board.bid, Board.name).select_from(Board).order_by(Board.bid).offset(page * RECORDS_PER_PAGE).limit(RECORDS_PER_PAGE)
    result = session.execute(query).fetchall()

    def tuple_to_dict(tuple_: tuple) -> dict:
        board_id, board_name = tuple_
        return { "bid": board_id, "name": board_name }
    
    result = list(map(tuple_to_dict, result))
    
    return {
        "result": result,
        "status": 200
    }


def isValidEmail(email: str) -> bool:
    import re
    # regular expression for e-mail address form
    regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
    
    if re.fullmatch(regex, email):
      return True
    
    return False


def create_board(board_name: str):
    # check whether email address is duplicated
    [duplicate_check] = check_exist_board(board_name).fetchone()
    if (duplicate_check != None):
        return {
            "result": 'duplicate board name detected',
            "status": 400
        }
    
    board = Board(name = board_name)
    session.add(board)
    session.commit()
    
    return {
        "result": None,
        "status": 201   # 201 Created
    }
    
    
def rename_board(board_name: str, target_name: str):
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
    session.execute(query)
    session.commit()

    return {
        "result": None,
        "status": 200
    }


def remove_board(board_name: str):
    # check whether the board exists with given name
    exist_check = check_exist_board(board_name).fetchone()
    if (exist_check == None):
        return {
            "result": 'no board detected with given name',
            "status": 400
        }
    
    query = delete(Board).where(Board.name == board_name).execution_options(synchronize_session="fetch")
    session.execute(query)
    session.commit()
    
    return {
        "result": None,
        "status": 200
    }


def create_article(title: str, contents: str, bname: str):
    # check whether the board exists with given name
    [exist_bid] = check_exist_board(bname).fetchone()
    if (exist_bid is None):
        return {
            "result": 'no board detected with given name',
            "status": 400
        }
    
    query = insert(Article).values(
        board_id = exist_bid,
        title = title,
        contents = contents,
        status = False
    )
    session.execute(query)
    session.commit()
    
    return {
        "result": None,
        "status": 200
    }


def edit_article(article_id: int, title: str, contents: str):
    # whether the article exists with given article id
    [exist_aid] = check_exist_article(article_id).fetchone()
    if (exist_aid is None):
        return {
            "result": 'no article detected with given id',
            "status": 400
        }
    
    if (title is None and contents is None):
        return {
            "result": "Bad Request",
            "status": 400
        }
    
    # edit title
    if (title is not None):
        query = update(Article).where(Article.aid == article_id).values(title = title)
        session.execute(query)
        session.commit()
    
    # edit contents
    if (contents is not None):
        query = update(Article).where(Article.aid == article_id).values(texts = contents)
        session.execute(query)
        session.commit()
    
    return {
        "result": None,
        "status": 200
    }


def read_article(article_id: int):
    # check whether article exists with given article id
    exist_aid = check_exist_article(article_id).fetchone()
    if (exist_aid is None):
        return {
            "result": 'no article detected with given id',
            "status": 400
        }
    
    query = select(Article.title, Article.texts, Article.date).select_from(Article).where(Article.aid == article_id, Article.status == False)
    title, contents, date = session.execute(query).fetchone()
    
    return {
        "result": {
            "title": title,
            "contents": contents,
            "date": date
        },
        "status": 200
    }


def delete_article(article_id: int):
    # check whether article exists with given article id
    exist_aid = check_exist_article(article_id).fetchone()
    if (exist_aid is None):
        return {
            "result": 'no article detected with given id',
            "status": 400
        }
    
    # mark as "deleted"
    query = update(Article).where(Article.aid == article_id).values(status = True)
    result = session.execute(query)
    session.commit()
    
    return {
        "result": None,
        "status": 200
    }


def delete_article_s(article_id: int):
    # check whether article exists with given article id
    exist_aid = check_exist_article(article_id).fetchone()
    if (exist_aid is None):
        return {
            "result": 'no article detected with given id',
            "status": 400
        }
    
    query = delete(Article).where(Article.aid == article_id)
    result = session.execute(query)
    session.commit()
    
    return {
        "result": None,
        "status": 200
    }

