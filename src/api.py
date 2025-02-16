#Code to interact with CourtListener's API
import pandas as pd
import requests
import json
from pandas import json_normalize
from pandas import concat
from pandas import DataFrame

from api_auth import token

#Options HTTP request
#curl -v   -X OPTIONS   --header 'Authorization: Token ..'   "https://www.courtlistener.com/api/rest/v4/dockets/" | jq '.filters'


#endpoints
root = 'https://www.courtlistener.com/api/rest/v4/'
dockets_ep = root + 'dockets/'
clusters_ep = root + 'clusters/'
courts_ep = root + 'courts/'
parties_ep = root + 'parties/'
opinions_ep =  root + 'opinions/'
tags_ep = root + 'tags/'
people_ep = root + 'people/'

def query_options(endpoint, parameters=None):
    #Info on OPTIONS requests: https://reqbin.com/req/python/jecm0tqu/options-request-example
    #This OPTIONS request does not apply to the search API
    response = requests.request("OPTIONS", url=endpoint, params=parameters)
    response_dict = json.loads(response.text)
    results = response_dict
    #filtered_response = jq  jq_filter response_dict
    return results

def query_api(endpoint, parameters=None) -> pd.DataFrame:
    #parameters is dict object, where key is field and value is condition
    try:
        response = requests.get(endpoint, headers={'Authorization': f"Token {token}"}, params=parameters)
        response_dict = json.loads(response.text)
        if 'results' in response_dict: #multi-object return
            results_df = json_normalize(response_dict['results'])

            next_page_endpoint = response_dict['next']

            while next_page_endpoint:
                response = requests.get(next_page_endpoint, headers={'Authorization': f"Token {token}"})
                response_dict = json.loads(response.text)
                results_df = concat([results_df, json_normalize(response_dict['results'])], ignore_index=True)
                next_page_endpoint = response_dict['next']
        else: #dealing with single instance/object
            results_df = pd.DataFrame.from_dict(response_dict, orient='index').T
    except Exception as e:
        print(e)
        return DataFrame()

    return results_df

