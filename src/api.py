#Code to interact with CourtListener's API
import pandas as pd
import requests
import json
from pandas import json_normalize
from pandas import concat
from pandas.core.interchange.dataframe_protocol import DataFrame

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

def query_options(endpoint, parameters=None):
    #Info on OPTIONS requests: https://reqbin.com/req/python/jecm0tqu/options-request-example
    #This OPTIONS request does not apply to the search API
    response = requests.request("OPTIONS", url=endpoint, params=parameters)
    response_dict = json.loads(response.text)
    results = response_dict
    #filtered_response = jq  jq_filter response_dict
    return results

def query_api(endpoint, parameters) -> pd.DataFrame:
    #parameters is dict object, where key is field and value is condition
    try:
        response = requests.get(endpoint, headers={'Authorization': f"Token {token}"}, params=parameters)
        response_dict = json.loads(response.text)
        results_df = json_normalize(response_dict['results'])

        next_page_endpoint = response_dict['next']

        while next_page_endpoint:
            response = requests.get(next_page_endpoint, headers={'Authorization': f"Token {token}"})
            response_dict = json.loads(response.text)
            results_df = concat([results_df, json_normalize(response_dict['results'])], ignore_index=True)
            next_page_endpoint = response_dict['next']
    except Exception as e:
        print(e)
        return DataFrame()

    return results_df



if __name__=='__main__':
    #Get dockets without federal jurisdictions: curl "https://www.courtlistener.com/api/rest/v4/dockets/?court__jurisdiction!=F"
    #Related Filters: can join filters between APIs
    trump_eo_dockets = query_api(endpoint=tags_ep, parameters={'name':'trump-executive-authority'})
    docket_ids = trump_eo_dockets['dockets'][0]
    dockets = []
    for docket_id in docket_ids:
        res = query_api(endpoint=dockets_ep, parameters={"id": docket_id})
        dockets.append(res)
    dockets_df = concat(dockets, ignore_index=True)
    #TODO: get state court case abbreviation, change below to read from clusters column in dockets_df
    #clusters = [query_api(endpoint=cluster_ep, parameters={'docket__docket_number': f"{docket_num}"}) for docket_num in dockets_df['docket_number']]
    #dockets = [query_api(dockets, {"id": f"{docket_id}"}) for docket_id in docket_ids]
    query_options(opinions_ep)