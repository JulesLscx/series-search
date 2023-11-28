import json
from elasticsearch import Elasticsearch
from es_interface.query import search as es_search
def load_json_test():
    path = "./test/series_keywords.json"
    with open(path, 'r') as f:
        data = json.load(f)
    return data

def test_for_a_serie(es : Elasticsearch, keywords: list, serie: str):
    score = 0
    for keyword in keywords:
        query = keyword
        result = es_search(es,query)
        if result == None or result == {} or result == False :
            continue
        if serie in result.values():
            score +=1
    if score == 0:
        percentage = 0
    else:
        percentage = score/len(keywords)
    # print(f"Score for {serie}: {score}/{len(keywords)}")
    return percentage
def run(es: Elasticsearch):
    data = load_json_test()
    score = 0
    total = len(data)
    for serie, keywords in data.items():
        print(f"Testing {serie}")
        score += test_for_a_serie(es, keywords, serie)
    print(f"Total score: {score/total}")
    
    
def with_different_bm25_params(es: Elasticsearch):
    bm25_configurations = [
    {"k1": 1.2, "b": 0.75, "discount_overlaps": True},
    {"k1": 1.5, "b": 0.6, "discount_overlaps": False},
    {"k1": 1.0, "b": 0.8, "discount_overlaps": True},
    {"k1": 1.8, "b": 0.5, "discount_overlaps": False},
    {"k1": 1.3, "b": 0.7, "discount_overlaps": True},
    {"k1": 1.6, "b": 0.6, "discount_overlaps": False},
    {"k1": 1.1, "b": 0.8, "discount_overlaps": True},
    {"k1": 1.7, "b": 0.5, "discount_overlaps": False},
    {"k1": 1.4, "b": 0.7, "discount_overlaps": True},
    {"k1": 1.9, "b": 0.4, "discount_overlaps": False},
    {"k1": 1.5, "b": 0.8, "discount_overlaps": True},
    {"k1": 1.8, "b": 0.3, "discount_overlaps": False},
    ]
    data = load_json_test()
    for conf in bm25_configurations:
        es.indices.close(index="testing")
        es.indices.put_settings(index="testing", body={"index": {"similarity": {"custom_bm25": {"type": "BM25", "k1": conf["k1"], "b": conf["b"], "discount_overlaps": conf["discount_overlaps"]}}}}) 
        es.indices.put_mapping(index="testing", body={"properties": {"subtitle": {"type": "text", "similarity": "custom_bm25"}}})
        es.indices.open(index="testing")
        print(f"Testing with k1: {conf['k1']}, b: {conf['b']}, discount_overlaps: {conf['discount_overlaps']}")
        score = 0
        for serie, keywords in data.items():
            score += test_for_a_serie(es, keywords, serie)
        print(f"Total score: {score}")