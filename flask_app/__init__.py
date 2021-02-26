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
db = app.mongo_client.harvard_db

def loadDB():
    collection = db.data

    collection.drop()
    
    # app.elasticsearch.indices.delete('harvard', ignore=[400, 404])

    # Load File
    with open('flask_app/harvard_dataverse.json') as raw_file:
        raw = json.load(raw_file)

    # Loads documents from JSON file into collection called 'data'
    collection.insert_many(raw)

    #Finds all documents, assigns cursor to res
    res = collection.find()

    # Checks how many documents have been loaded into MongoDB
    num_docs = collection.estimated_document_count()

    # # Pull from Mongo and dump into ES w/ bulk indexing
    # actions = []
    # for i in range(num_docs):
    #     doc = res[i]

    #     # Remove ID from MongoDB entry, so no duplicate IDs are given in elastic search index
    #     doc.pop('_id')

    #     action = {
    #         "_index": 'harvard',
    #         "_source": json.dumps(doc)
    #     }
    #     actions.append(action)

    # # Mapping that matches requisites provided by Dr. Wu
    # custom_map = {
    #     "settings": {
    #         "analysis": {
    #             "normalizer": {
    #                 "case_insensitive": {
    #                     "type": "custom",
    #                     "filter": ["lowercase"]
    #                 }
    #             }
    #         }
    #     },
    #     "mappings": {
    #         "properties": {
    #             "funder.name": {
    #                 "type": "keyword",
    #                 "normalizer": "case_insensitive"		    }
                                                
    #         }
    #     }
    # }
    
    # app.elasticsearch.indices.create(index='harvard', body=custom_map)
    # helpers.bulk(app.elasticsearch, actions, request_timeout=30)
        
except:
    print("Unexpected Error: ", sys.exc_info())

if __name__ == '__main__':
    loadDB()
    app.run()
    
# Workaround for the circular import problem
from flask_app import routes
