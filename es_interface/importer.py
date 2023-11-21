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
        self.es = es or Elasticsearch([ENDPOINT], http_auth=(USERNAME, PASSWORD))

    def run(self):
        elk_data = self.df.to_dict("records")
        #Add a console tqdm to see the progress
        for job in elk_data:
            try:
                self.es.index(index=self.index_name, document=job)
            except Exception as e:
                pass
    def delete_index(self):
        self.es.indices.delete(index=self.index_name, ignore=[400, 404])
    
    def create_index(self):
        settings = {"similarity": {
                    "default": {
                        "type": "BM25"
                    }
                },
                "index": {
                    "max_result_window": 100000
                }}
        mappings = {"properties": {
                    "serie": {
                        "type": "text"
                    },
                    "episode": {
                        "type": "text"
                    },
                    "subtitles": {
                        "type": "text"
                    }
                }}
        self.es.indices.create(index=self.index_name, ignore=400, settings=settings, mappings=mappings)
        self.es.indices.refresh(index=self.index_name)
        return True
