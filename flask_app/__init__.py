from flask import Flask
from config import Config
from elasticsearch import Elasticsearch, helpers
from pymongo import MongoClient
import sys
import json

# Initialize Flask application
app = Flask(__name__)
app.config.from_object(Config)

app.elasticsearch = Elasticsearch([app.config['ELASTICSEARCH_URL']]) \
    if app.config['ELASTICSEARCH_URL'] else None

app.mongo_client = MongoClient(app.config['MONGODB_URI'])

# Workaround for the circular import problem
from flask_app import routes
