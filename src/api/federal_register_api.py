#Code to interact with Federal Register's API
import pandas as pd
import requests
import json
from pandas import json_normalize
from pandas import concat
from pandas import DataFrame

documents_req_url = "https://www.federalregister.gov/api/v1/documents.json?per_page=20&order=newest&conditions[publication_date][year]=2025&conditions[agencies][]=&conditions[presidential_document_type][]=executive_order&conditions[president][]=donald-trump"

def query_api(req_url) -> pd.DataFrame:
    #parameters is dict object, where key is field and value is condition
    try:
        response = requests.get(req_url)
        response_dict = json.loads(response.text)
        if 'results' in response_dict: #multi-object return
            results_df = json_normalize(response_dict['results'])

            next_page_url = response_dict['next_page_url']

            while next_page_url:
                response = requests.get(next_page_url)
                response_dict = json.loads(response.text)
                results_df = concat([results_df, json_normalize(response_dict['results'])], ignore_index=True)
                next_page_url = response_dict['next_page_url'] if 'next_page_url' in response_dict else None
        else: #dealing with single instance/object
            results_df = pd.DataFrame.from_dict(response_dict, orient='index').T
    except Exception as e:
        print(e)
        return DataFrame()

    return results_df

if __name__=='__main__':
    res = query_api(documents_req_url)
