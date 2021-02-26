from flask_app import app
import json
import sys
from elasticsearch import Elasticsearch, helpers

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
