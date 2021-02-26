from flask_app import app
import json

# Behavior for Elasticsearch queries based on '@id' data identifier
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

# Behavior for Elasticsearch queries based on user-inputted field and value
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

# Return all documents in index 'harvard'
# Primarily for debugging purposes 
def find_all():
    search_obj = {
        "query": {
            "match_all": {}
        }
    }
            
    res = app.elasticsearch.search(index="harvard", body=search_obj, size=100)
    return json.dumps(res['hits']['hits'])
