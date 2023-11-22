from elasticsearch import Elasticsearch
from tools.preprocessing import preprocess

def search(es: Elasticsearch, text: str):
    if not es.ping():
        return False

    if not text:
        return False

    text_without_space = text.replace(" ", "")
    text_for_query = preprocess(text)

    search_body ={
        "_source": ["serie"],
        "size": 0,
        "query": {
            "bool": {
            "should": [
                {
                "match": {
                    "serie.keyword": {
                    "query": text_without_space,  
                    "operator": "and",
                    "boost": 2
                    }
                }
                },
                {
                "match": {
                    "subtitle": {
                    "query": text_for_query,  
                    "operator": "and"
                    }
                }
                }
            ]
            }
        },
        "aggs": {
            "series": {
            "terms": {
                "field": "serie.keyword",
                "size": 20,
                "order": {
                "_key": "desc"
                }
            }
            }
        }
        }


    index_name = "testing"
    result = es.search(index=index_name, body=search_body)

    ranking = {}


    to_return = {
        # "ranking": ranking,
        # "infos": {
        #     "took": result['took'],
        #     "total": result['hits']['total']['value']
        # }
    }
    from pprint import pprint
    pprint(result)
    return to_return
