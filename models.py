from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Sequence, Integer, String, DateTime, Boolean, ForeignKey, Text, func
Base = declarative_base()

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
    password = Column('password', String(20))


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
    
    # article contents
    texts = Column('contents', Text)
    
    # article date (create)
    date = Column('date', DateTime, default = func.now())
    
    # article date (recently edit)
    edate = Column('edate', DateTime, default = func.now())
    
    # status -> this system should be "vengeful"
    status = Column('status', Boolean, default = False)
    
    def __init__(self, bid, texts, date, edate, status):
        self.bid = bid
        self.texts = texts
        self.date = date
        self.edate = edate
        self.status = status