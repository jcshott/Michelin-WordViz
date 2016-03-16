from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.engine.url import URL

import settings

DeclarativeBase = declarative_base()

def db_connect():
	return create_engine(URL(**settings.DATABASE))

def create_reviews_table(engine):

	DeclarativeBase.metadata.create_all(engine)

class Reviews(DeclarativeBase):
	"""Sqlalchemy reviews model"""
	__tablename__ = "reviews"

	id = Column(Integer, primary_key=True)
	yelp_review_id = Column('yelp_review_id', String)
	text = Column('text', String)
	rating = Column('rating', String)
	date = Column('date', DateTime)
	reviewer_location = Column('reviewer_location', String, nullable=True)
	# restraunt_id = Column('restraunt_id', String)