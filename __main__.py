import os
import time
import pandas as pd
from tqdm import tqdm
import sys
import pytest
from tools.unzipper import Unzipper, rmtmp
from tools.cleaner import Cleaner
from tools.loader import get_preprocessed_data
from es_interface.importer import ElasticSearchImports
from es_interface.query import search
from elasticsearch import Elasticsearch
from global_var import ES_ENDPOINT, ES_USER, ES_PASSWORD
from test.score_search import run as test_search

def get_help():
    help_str = """
    Commands:
    unzip: Unzip the data and process it, store it in data/processed
    query: Query the database with a text in parameter
    import: Import the data from data/processed to the database
    run_api: Run the api
    score_search: Run the score search test
    test_api: Run the api tests
    recommand: Run the recommendation test with a static serie list (see __main__.py for the list)
    """
    print(help_str)
def run_tests():
    retcode = pytest.main(["-x", "./test", "--disable-warnings"])
    if retcode != 0:
        print("Error in tests. Tests must pass before running the API.")
        exit()

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
    es = Elasticsearch([ES_ENDPOINT], basic_auth=(ES_USER, ES_PASSWORD) , verify_certs=False, ssl_show_warn=False)
    start = time.time()
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
def launch_api():
    from api.app import create_app
    app = create_app()
    app.run(debug=True, host='')
    exit()
    
def main():
    if len(sys.argv) < 2:
        print("Please specify a command")
        get_help()
        exit()
    elif sys.argv[1] == "help" or sys.argv[1] == "-h" or sys.argv[1] == "--help":
        get_help()
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
    elif sys.argv[1] == "score_search":
        es = Elasticsearch([ES_ENDPOINT], basic_auth=(ES_USER, ES_PASSWORD) , verify_certs=False, ssl_show_warn=False)
        # test_search.run(es)
        test_search(es)
        exit()
    elif sys.argv[1] == "recommand":
        es = Elasticsearch([ES_ENDPOINT], basic_auth=(ES_USER, ES_PASSWORD) , verify_certs=False, ssl_show_warn=False)
        from es_interface.recommendation import recommendate
        print(recommendate(es, ["alias", "ncis", "24", "breakingbad", "prisonbreak",'smallville', 'stargatesg1', 'friends', 'scrubs', 'charmed', 'southpark', 'bones', 'xfiles', 'onetreehill', 'lost','criminalminds', 'entourage', 'buffy', 'coldcase', 'supernatural', 'desperatehousewives', 'greysanatomy', 'doctorwho', 'intreatment', 'theoc','howimetyourmother', 'uglybetty', 'angel', 'ghostwhisperer', 'medium', 'thesopranos', 'niptuck', 'thepretender', 'veronicamars', 'weeds']))
        exit()
    elif sys.argv[1] == "test_api":
        run_tests()
        exit()
    elif sys.argv[1] == "run_api":
        launch_api()
    else:
        print("Unknown command")
        get_help()
        exit()
if __name__ == "__main__":
    main()