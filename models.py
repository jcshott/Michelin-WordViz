"""Models and database functions"""

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSON

import os 

import psycopg2


db = SQLAlchemy()

class Reviews(db.Model):
    """review data from yelp
    """

    __tablename__ = 'reviews'

    review_id = db.Column(db.String(30), primary_key=True)
    restaurant_name = db.Column(db.String(20), nullable=False)
    biz_id = db.Column(db.String(15), db.ForeignKey('restaurants.biz_id'), nullable=False)
    rating = db.Column(db.Float, nullable=False) 
    text = db.Column(db.Text, nullable=False)
    location = db.Column(db.String(50), nullable=True)
    date = db.Column(db.DateTime, nullable=False)
    
    restaurant = db.relationship("Restaurants", backref=db.backref('reviews'))
    

    def __repr__(self):
        return "<Review ID=%s, Restaurant=%s, Rating=%s>" % (self.contrib_id, self.leg_id, self.amount)


##############################################################################
# Helper functions for flask app

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use postgresql database
    DATABASE_URL = os.environ.get("DATABASE_URL", 'postgresql://yelpproject@localhost:5432/yelpreviewviz')

    app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL

    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from runserver import app
    
    connect_to_db(app)
    print "Connected to DB."