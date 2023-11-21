from elasticsearch import Elasticsearch
from tools.preprocessing import preprocess
def search(es: Elasticsearch,text: str):
    if(not es.ping()):
        return False
    if not text:
        return False
    text_without_space = text.replace(" ", "")
    text_for_query = preprocess(text)
    query = {
        "bool": {
            "should": [
                {
                    "match": {
                        "serie.keyword": {
                            "query": text_without_space,
                            "operator": "and",
                            "boost":3
                        }
                    }
                },
                {
                    "match":{
                        "episode.keyword": {
                            "query":text_for_query,
                            "operator":"and",
                            "boost":2
                    }
                    }
                },
                {
                    "match": {
                        "subtitles": {
                            "query": text_for_query,
                            "operator": "and"
                        }
                    }
                }
            ]
        }
    }
    source = ["serie"]
    aggs = {
    "series": {
        "terms": {
            "field": "serie.keyword",
            "size": 20,
            "order": {
                "score_sum": "desc"
            }
        },
        "aggs": {
            "score_sum": {
                "sum": {
                    "script": "_score"
                }
            }
        }
    }
    }
    index_name = "testing"
    result = es.search(index=index_name, body={"query": query, "_source": source, "aggs": aggs})
    ranking = {}
    for hit in result['hits']['hits']:
        ranking[hit['_source']['serie']] = hit['_score']
    to_return = {"ranking": ranking, "infos": {
        "took": result['took'],
        "total": result['hits']['total']['value']
    }}
    return to_return