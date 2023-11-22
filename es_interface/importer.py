from elasticsearch import Elasticsearch
from tqdm import tqdm
from global_var import ES_ENDPOINT, ES_USER, ES_PASSWORD

class ElasticSearchImports(object):
    def __init__(self, df, index_name='testing', es=None):
        ENDPOINT = ES_ENDPOINT
        USERNAME = ES_USER
        PASSWORD = ES_PASSWORD
        self.df = df
        self.index_name = index_name
        self.es = es or Elasticsearch([ENDPOINT], http_auth=(USERNAME, PASSWORD), verify_certs=False)

    def run(self):
        elk_data = self.df.to_dict("records")
        #tqdm the for loop
        for job in tqdm(elk_data):
            try:
                self.es.index(index=self.index_name, document=job)
            except Exception as e:
                pass
            #handle warning

    def delete_index(self):
        self.es.indices.delete(index=self.index_name, ignore=[400, 404])
    
    def create_index(self):
        settings = {"similarity": {
                    "custom_bm25": {
                        "type": "BM25"
                    }
                },
                "index": {
                    "max_result_window": 100000
                }}
        mappings = {"properties": {
                    "serie": {
                        "type": "keyword",
                    },
                    "episode": {
                        "type": "text",
                        "similarity": "custom_bm25"
                    },
                    "subtitle": {
                        "type": "text",
                        "similarity": "custom_bm25"
                    }
                }}
        #If index already exists, say it
        if self.es.indices.exists(index=self.index_name):
            print("Index already exists")
            return False
        self.es.indices.create(index=self.index_name, ignore=400, settings=settings, mappings=mappings)
        self.es.indices.refresh(index=self.index_name)
        return True
