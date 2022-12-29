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
    query = select(Board.bid, Board.name).select_from(Board).order_by(Board.bid).offset(page).limit(RECORDS_PER_PAGE)
    result = session.execute(query).fetchall()

    def tuple_to_dict(tuple_: tuple) -> dict:
        a, b = tuple_
        return {"bid": a, "name": b}
    
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
