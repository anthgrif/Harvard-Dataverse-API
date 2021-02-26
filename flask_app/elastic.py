from flask_app import app
from elasticsearch import helpers
import json
import sys
from elasticsearch import Elasticsearch, helpers

try:
    db = app.mongo_client['harvard_db']
    collection = db['data']

    collection.drop()

    # Load File
    with open('flask_app/harvard_dataverse.json') as raw_file:
        raw = json.load(raw_file)

    # Loads documents from JSON file into collection called 'data'
    if isinstance(raw, list): 
        collection.insert_many(raw)
    else: 
        collection.insert_one(raw) 

    #Finds all documents, assigns cursor to res
    res = collection.find()

    # Checks how many documents have been loaded into MongoDB
    num_docs = collection.estimated_document_count()

    # Pull from Mongo and dump into ES w/ bulk indexing
    actions = []
    for i in range(num_docs):
        doc = res[i]

        # Remove ID from MongoDB entry, so no duplicate IDs are given in elastic search index
        doc.pop('_id')

        action = {
            "_index": 'harvard',
            "_source": json.dumps(doc)
        }
        actions.append(action)

    # Mapping that matches requisites provided by Dr. Wu
    custom_map = {
        "settings": {
            "analysis": {
                "normalizer": {
                    "case_insensitive": {
                        "type": "custom",
                        "filter": ["lowercase"]
                    }
                }
            }
        },
        "mappings": {
            "properties": {
                "funder.name": {
                    "type": "keyword",
                    "normalizer": "case_insensitive"		    }
                                                
            }
        }
    }

    # OPTIONAL: Delete index 'harvard'
    if app.elasticsearch.indices.exists('harvard'):
        app.elasticsearch.indices.delete('harvard')
    
    app.elasticsearch.indices.create(index='harvard', body=custom_map)
    helpers.bulk(app.elasticsearch, actions, request_timeout=30)
        
except:
    print("Unexpected Error: ", sys.exc_info())

def searchByID(idNum, facet="funder.name"):
    # Look for exact match with what the user has submitted    
    search_obj = {
        "query": {
            "match": {
                    "@id.keyword": idNum
                    }
            },
        "aggs": {
            "Funder Name Filter": {
                "terms": {
                        "field": facet
                        }
                }
        }
    }

    res = app.elasticsearch.search(index="harvard", body=json.dumps(search_obj))

    # List to include all 'hits' from query
    mydata = []

    # Append total number of documents found that match specified ID
    mydata.append(res['hits']['total']['value'])

    for hit in res['hits']['hits']:
        mydata.append(hit['_source'] | res['aggregations'])

    return mydata

def searchByField(field, value, facet="funder.name"):
    # Look for exact match with what the user has submitted    
    search_obj = {
        "query": {
            "match": {
                    field+".keyword": value
                    }
            },
        "aggs": {
            "Funder Name Filter": {
                "terms": {
                    "field": facet
                }
            }
        }
    }
    
    res = app.elasticsearch.search(index="harvard", body=search_obj)

    # List to include all 'hits' from query
    mydata = []

    # Append total number of documents found that match specified ID
    mydata.append(res['hits']['total']['value'])

    for hit in res['hits']['hits']:
        mydata.append(hit['_source'] | (res['aggregations']))

    # Return list w/ number of documents in the first index followed by the documents returned by the query
    return mydata
        
def find_all():
    search_obj = {
        "query": {
            "match_all": {}
        }
    }
            
    res = app.elasticsearch.search(index="harvard", body=search_obj, size=100)
    return json.dumps(res['hits']['hits'])
