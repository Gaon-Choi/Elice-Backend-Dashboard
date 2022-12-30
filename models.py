from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Sequence, Integer, String, DateTime, Boolean, ForeignKey, Text, func
Base = declarative_base()
import datetime

'''
USER_ID_SEQ = Sequence('user_id_seq')
BOARD_ID_SEQ = Sequence('board_id_seq')
ARTICLE_ID_SEQ = Sequence('article_id_seq')
'''

class User(Base):
    __tablename__ = 'users'
    # user name
    uid = Column('id', Integer, primary_key = True)
    
    # user's name
    fullname = Column('name', String(30))
    
    # user's email
    email = Column('email', String(50))
    
    # user's password -> should be private!
    password = Column('password', String(80))


    def __init__(self, fullname, email, password):
        self.fullname = fullname
        self.email = email
        self.password = password
    
    
    def __repr__(self):
        return "<User('%s', '%s', '%s')>" % (self.fullname, self.email, self.password)

class Board(Base):
    __tablename__ = 'boards'
    # board id
    bid = Column('id', Integer, primary_key = True)
    
    # board name
    name = Column('name', String(30))

    def __init__(self, name):
        self.name = name


class Article(Base):
    __tablename__ = 'articles'
    # article id
    aid = Column('id', Integer, primary_key = True)
    
    # board id (foreign key)
    bid = Column('board_id', Integer, ForeignKey('boards.id'))
    
    # article title
    title = Column('title', String(100))
    
    # article contents
    texts = Column('contents', Text)
    
    # writer (User id)
    writer = Column('writer', Integer, ForeignKey('users.id'))
    
    # article date (create)
    date = Column('date', DateTime(timezone=True), server_default=func.now())
    
    # article date (recently edit)
    edate = Column('edate', DateTime(timezone=True), server_default = func.now(), onupdate=func.now())
    
    # status -> this system should be "vengeful"
    status = Column('status', Boolean, default = False)
    
    def __init__(self, bid, title, texts, writer):
        self.bid = bid
        self.title = title
        self.texts = texts
        self.writer = writer
        self.date = datetime.datetime.utcnow()
        self.edate = datetime.datetime.utcnow()
        self.status = False
    
    def __dict__(self):
        return {
            "aid": self.aid,
            "bid": self.bid,
            "title": self.title,
            "texts": self.texts,
            "writer": self.writer,
            "date": self.date,
            "edate": self.edate,
            "status": self.status
        }
