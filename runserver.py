from flask import Flask
from jinja2 import StrictUndefined
from models import connect_to_db, db #add tables classes here
import os

app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
SECRET_KEY = os.environ.get("FLASK_SECRET_KEY", "ABCDEF")
app.secret_key = SECRET_KEY
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

PORT = int(os.environ.get("PORT", 5000))
#set debug-mode to false for deployed version but true locally
DEBUG = "NO_DEBUG" not in os.environ

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined

#### ROUTES ###

@app.route("/")
def home():
    """This is home page"""

    return "Hello!!"

if __name__ == '__main__':
	
	connect_to_db(app)
	
	port = int(os.environ.get("PORT", 5000))
	
	app.run(debug=DEBUG, host="0.0.0.0", port=PORT)