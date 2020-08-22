# Importing modules nessary  
from sqlalchemy import Column, String, Integer, Float, DateTime, create_engine
from flask_sqlalchemy import SQLAlchemy
import json
import os
import sys

# setup database path 
database_path = os.environ['DATABASE_URL']

db = SQLAlchemy()

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()

# class Movies with attributes id and title, release date

class Movie(db.Model):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True)
    title = Column(String(50), nullable=True)
    rate = Column(Float)
    release_date = Column(DateTime, nullable=True)

    def __init__(self, title, rate, release_date):
        self.title = title
        self.rate = rate
        self.release_date = release_date
    
    def commit(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def insert(self):
        db.session.add(self)
        self.commit()
    
    def delete(self):
        db.session.delete(self)
        self.commit()

    def update(self):
        self.commit()
    
    
    def format(self):
        return {
            'id':self.id,
            'title':self.title,
            'rate':self.rate,
            'release_date':self.release_date
        }


# class Actors with attributes id, name, age and gender
class Actor(db.Model):
    __tablename__ = 'actors'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=True)
    age = Column(Integer, nullable=True)
    gender = Column(String(1), nullable=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender
    
    def commit(self):
        try:
            db.session.commit()
        except:
            db.session.rollback()
        finally:
            db.session.close()

    def insert(self):
        db.session.add(self)
        self.commit()
    
    def delete(self):
        db.session.delete(self)
        self.commit()

    def update(self):
        self.commit()


    def format(self):
        return {
            'id':self.id,
            'name':self.name,
            'age':self.age,
            'gender':self.gender
        }
# relation act belong to one movie and the movie has many actors
