#Code to interact with CourtListener's API
import requests
from api_auth import token

#endpoints
dockets = 'https://www.courtlistener.com/api/rest/v4/dockets/'

def query_dockets(parameters):
    #parameters is dict object, where key is field and value is condition
    response = requests.get(dockets, headers={'Authorization': f"Token {token}"}, params=parameters)
    return response.text



if __name__=='__main__':
    response = query_dockets({'fields': 'case_name,date_filed', 'date_filed__gte':'2025-01-20'})