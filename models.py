from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, func
Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    # user name
    uid = Column(Integer, Sequence('user_id_seq'), primary_key = True)
    # user's name
    fullname = Column(String(30))
    # user's email
    email = Column(String(50))
    # user's password -> should be private!
    password = Column(String(20))
    
    
    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.password = password
    
    
    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.fullname, self.email, self.password)


class Board:
    __tablename__ = 'boards'
    # board id
    bid = Column(Integer, Sequence('board_id_seq'), primary_key = True)
    # board name
    name = Column(String(30))


class Article:
    __tablename__ = 'articles'
    # article id
    aid = Column(Integer, Sequence('article_id_seq'), primary_key = True)
    # board id (foreign key)
    bid = Column(Integer, ForeignKey('boards.bid'))
    # article contents
    texts = Column(Text)
    # article date (create or edit)
    date = Column(DateTime, default = func.now())