import os
import time
import pandas as pd
from tqdm import tqdm
import sys
from tools.unzipper import Unzipper, rmtmp
from tools.cleaner import Cleaner
from tools.loader import get_preprocessed_data
from es_interface.importer import ElasticSearchImports
from es_interface.query import search
from elasticsearch import Elasticsearch
from global_var import ES_ENDPOINT, ES_USER, ES_PASSWORD
from test import test_search
def treat_import_command():
    # if not data in ./data/processed, raise error
    if(os.path.exists('./data/processed') and os.listdir('./data/processed') == []):
        print("No data to import, please unzip data first")
        exit()
    print("Load and preprocess data")
    data = get_preprocessed_data()
    print("Connecting to ElasticSearch...")
    es = Elasticsearch([ES_ENDPOINT], basic_auth=(ES_USER, ES_PASSWORD) , verify_certs=False, ssl_show_warn=False)
    print(f'Importing {data.size} subs to database...')
    importer = ElasticSearchImports(data, index_name='testing', es=es)
    importer.delete_index()
    importer.create_index()
    importer.run()
    print("Importing data, Done ! Ready to query !")
def treated_query_command(text:str):
    start = time.time()
    es = Elasticsearch([ES_ENDPOINT], basic_auth=(ES_USER, ES_PASSWORD) , verify_certs=False, ssl_show_warn=False)
    print("Querying...")
    res = search(es, text)
    print("Querying done in " + str(time.time() - start) + " seconds")
    print("Results:")    
    print(res)

def treat_unzip_command(path_to_unzip):
    tqdm.pandas()
    print("Unzipping data...")
    if not os.path.exists(path_to_unzip):
        print("Path does not exist, make sure to go to your root zip containing subs")
        exit()
    if not path_to_unzip.endswith(".zip") and not path_to_unzip.endswith(".7z"):
        print("Path is not a zip file")
        exit()
    # check if ./tmp exists and if it is empty
    rmtmp()
    to_unzip = Unzipper('./data/processed',path_to_unzip)
    to_unzip.u_zip()
    to_unzip.categorise_all_sub()
    print("Processing data, Done !")

# If command is process, get the zip and process it, store it in data/processed
if len(sys.argv) < 2:
    print("Please specify a command")
    print("Commands:")
    print("unzip")
    print("query")
    print("import")
    print("run_api")
    print("test_search")
    exit()

if sys.argv[1] == "unzip":
    print("Called unzip command")
    if len(sys.argv) < 3:
        print("Please specify a path to unzip")
        exit()
    treat_unzip_command(sys.argv[2])
    exit()
elif sys.argv[1] == "import":
    treat_import_command()
    exit()
elif sys.argv[1] == "query":
    #Must have a text to query
    if len(sys.argv) < 3:
        print("Please specify a text to query")
        exit()
    text = sys.argv[2]
    treated_query_command(text)
    exit()
elif sys.argv[1] == "test_search":
    es = Elasticsearch([ES_ENDPOINT], basic_auth=(ES_USER, ES_PASSWORD) , verify_certs=False, ssl_show_warn=False)
    test_search.run(es)
    exit()