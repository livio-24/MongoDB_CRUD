from flask import Flask
from flask_pymongo import PyMongo

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/hotels_reviews"

# setup mongodb connection
mongodb_client = PyMongo(app)
db = mongodb_client.db

from flask_app import routes
