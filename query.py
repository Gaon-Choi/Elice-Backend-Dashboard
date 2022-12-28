from sqlalchemy import *
from models import User, Board, Article

from app import session

import datetime


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
    pass

def login(email: str, password: str):
    pass

def logout():
    pass

def board_list():
    pass

