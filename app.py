from flask import Flask, render_template, session
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
import redis
import models
import SessionStore

db_string = "postgresql://developer:devpassword@127.0.0.1:25000/developer"

engine = create_engine(db_string, echo=True)
sql_session = Session(bind=engine)

if __name__ == '__main__':
    app = Flask(__name__)
    app.config["SECRET_KEY"] = 'd2707fea9778e085491e2dbbc73ff30e'
    
    # use blueprint to connect routing information from router.py
    from router import page
    app.register_blueprint(page)
    
    models.Base.metadata.create_all(bind=engine)
    
    app.run(debug=True)
