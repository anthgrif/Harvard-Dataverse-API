import os

# Class to assign configuration variables
class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret_password'
    ELASTICSEARCH_URL = os.environ.get('ELASTICSEARCH_URL')
    MONGODB_URI = os.environ.get('MONGODB_URI')
