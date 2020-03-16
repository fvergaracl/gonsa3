import requests
from googlesearch import search

def googlesearch(query):
    my_results_list = []
    for i in search(query,  # The query you want to run
                    tld='com',  # The top level domain
                    lang='es',  # The language
                    num=10,  # Number of results per page
                    start=0,  # First result to retrieve
                    stop=50,  # Last result to retrieve
                    pause=2.0,  # Lapse between HTTP requests
                    ):
        my_results_list.append(i)
        print(i)

def duckduckgo(query):
    query_ = 'http://api.duckduckgo.com/?q=%s&format=json' % query
    response = requests.get(query_)
    if response.status_code == 200:
        return True, response.text
    elif response.status_code == 404:
        return False, ''
