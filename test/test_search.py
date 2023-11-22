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
    print(f"Score for {serie}: {score}/{len(keywords)}")
    return percentage
def run(es: Elasticsearch):
    data = load_json_test()
    score = 0
    total = len(data)
    for serie, keywords in data.items():
        print(f"Testing {serie}")
        score += test_for_a_serie(es, keywords, serie)
    print(f"Total score: {score/total}")
    