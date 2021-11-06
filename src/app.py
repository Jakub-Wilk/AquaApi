from flask import Flask, request
from flask_pymongo import PyMongo
from . import env

app = Flask(__name__)
app.config["MONGO_URI"] = env.mongo_uri
app.config["SECRET_KEY"] = env.secret_key

mongo = PyMongo(app)

