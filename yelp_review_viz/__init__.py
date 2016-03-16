from flask import Flask


app = Flask(__name__)
app.secret_key = 'abc123'


import yelp_review_viz.views


