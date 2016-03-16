# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from sqlalchemy.orm import sessionmaker
from models import Reviews, db_connect, create_reviews_table

class YelpReviewPipeline(object):
    def __init__(self):
    	""" initialize database connection and sessionmaker. 
    	Creates yelp review table
    	"""
    	engine = db_connect()
    	create_reviews_table(engine)
    	self.Session = sessionmaker(bind=engine)
    
    def process_item(self, item, spider):
    	""" save reviews in db"""

    	session = self.Session()
    	review = Reviews(**item)

    	try:
    		session.add(review)
    		session.commit()
    	except:
    		session.rollback()
    		raise
    	finally:
    		session.close()
    		
        return item
