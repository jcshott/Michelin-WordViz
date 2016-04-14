"""Models and database functions"""

import os 
import re
import nltk
import psycopg2
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON
from nltk.tokenize import RegexpTokenizer, word_tokenize, WordPunctTokenizer

db = SQLAlchemy()

class Reviews(db.Model):
    """review data from yelp
    """

    __tablename__ = 'reviews'

    review_id = db.Column(db.String(30), primary_key=True)
    restaurant_name = db.Column(db.String(50), nullable=False)
    biz_id = db.Column(db.String(30), db.ForeignKey('restaurants.biz_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False) 
    text = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    restaurant = db.relationship("Restaurants", backref=db.backref('reviews'))
    

    def __repr__(self):
        return "<Review ID=%s, Restaurant=%s, Rating=%s>" % (self.review_id, self.restaurant_name, self.rating)


class Restaurants(db.Model):
    """ basic data for restaurants"""

    # def __init__(self, biz_id=None, common_name=None, yelp_name=None, location=None, avg_yelp_rating=None, michelin_stars=3):
    #     self.biz_id = biz_id
    #     self.common_name=common_name
    #     self.yelp_name=yelp_name
    #     self.location=location
    #     self.avg_yelp_rating=avg_yelp_rating
    #     self.michelin_stars=michelin_stars

    __tablename__ = 'restaurants'

    biz_id = db.Column(db.String(30), primary_key=True)
    common_name = db.Column(db.String(50))
    yelp_name = db.Column(db.String(80))
    location = db.Column(db.String(100))
    avg_yelp_rating = db.Column(db.Float)
    michelin_stars = db.Column(db.Integer)

    def __repr__(self):
        return "<Biz ID=%s, Restaurant=%s, Avg. Rating=%s>" % (self.biz_id, self.common_name, self.avg_yelp_rating)
    
    @staticmethod
    def from_biz_id(target_biz_id):
        restaurant = db.session.query(Restaurants).filter_by(biz_id=target_biz_id).one()
        if restaurant:
            return restaurant
        else:
            print "No such biz id"
            return None

    def collect_words(self):
        # given a retaurant, query the reviews table for review text
        all_reviews = db.session.query(Reviews.text).filter_by(biz_id=self.biz_id).all()
        # all_reviews is list of tuples so need to unpack just the review text
        all_reviews_text = []
        for tup in all_reviews:
            all_reviews_text.append(tup[0])
        return all_reviews_text

    def determine_pos(self):
        all_reviews_list = self.collect_words()
        all_reviews_list = all_reviews_list
        pos_dict = {}
        for review in all_reviews_list:
            tokens = re.split('[\s\W]', review)
            tokens = [token.lower() for token in tokens if token]
            tagged = nltk.pos_tag(tokens)
            for tup in tagged:
                word, pos = tup[0], tup[1]
                pos_dict.setdefault(pos, set())
                pos_dict[pos].add(word)
        for entry in pos_dict:
            pos_dict[entry] = list(pos_dict[entry])

        #print pos_dict
        return pos_dict
        
        
##############################################################################
# Helper functions for flask app

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use postgresql database
    DATABASE_URL = os.environ.get("DATABASE_URL", 'postgresql://yelpproject@localhost:5432/yelpreviewviz')

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from runserver import app
    
    connect_to_db(app)
    print "Connected to DB."