from elasticsearch import Elasticsearch
def query_id_for_serie(es : Elasticsearch, serie_name: str):
    print()
    query = {
      "query": {
        "match": {
          "serie": serie_name
        }
      }
    }
    result = es.search(index="testing", body=query)
    ids = [hit['_id'] for hit in result['hits']['hits']]
    return ids
def recommendate(es : Elasticsearch, series_regardees_ids: list):
    if len(series_regardees_ids) == 0:
        print("No series to recommendate")
        return
    ids = []
    for serie in series_regardees_ids:
        ids += query_id_for_serie(es, serie)
    query = {
    "_source": ["serie"],
    "size": 0,
    "query": {
        "bool": {
            "must": [
                {
                    "more_like_this": {
                        "fields": ["subtitle"],
                        "like": [{"_index": "testing", "_id": serie_id} for serie_id in ids],
                        "min_term_freq": 1,
                        "max_query_terms": 25,
                        "min_doc_freq": 1
                    }
                }
            ],
            "must_not": [
                { 
                    "terms": {
                        "serie": series_regardees_ids
                    }
                }
            ]
        }
    },
    "aggs": {
        "series": {
            "terms": {
                "field": "serie",
                "size": 10
            }
        }
    }
    
}
    result = es.search(index="testing", body=query)
    return [hit['key'] for hit in result['aggregations']['series']['buckets']]
