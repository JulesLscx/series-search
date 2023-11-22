from elasticsearch import Elasticsearch
from tools.preprocessing import preprocess

def search(es: Elasticsearch, text: str):
    if not es.ping():
        return False

    if not text:
        return False

    text_without_space = text.replace(" ", "")
    text_for_query = preprocess(text)
    print(text_without_space)
    search_query = {
    "_source": [ "serie" ],
    "size": 0,
    "query": {
        "bool": {
            "should": [
                { "match": { "serie": { "query": text_without_space, "boost": 4 } } },
                { "match": { "subtitle": { "query": text_for_query , "operator":"and"} } }
            ]
        }
    },
    "aggs": {
        "series": {
            "terms": { "field": "serie" },
            "aggs": { "total_score": { "avg": { "script": "_score" } } }
        }
    }
}

    result = es.search(index="testing", body=search_query)
    from pprint import pprint
    ranking = {}
    i=1
    for serie in result['aggregations']['series']["buckets"]:
        ranking[str(i)] = serie['key']
        i+=1
    pprint(ranking)
