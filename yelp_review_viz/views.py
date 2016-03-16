from yelp_review_viz import app

from flask import Flask, render_template, request, redirect, flash, session, jsonify, g
from jinja2 import StrictUndefined


@app.route("/")
def home():
    """This is home page"""

    return "Hello!!"