from src.api.court_listener_api import tags_ep, dockets_ep
import pandas as pd

from src.api.court_listener_api import query_api

def update_data():
    # Get dockets without federal jurisdictions: curl "https://www.courtlistener.com/api/rest/v4/dockets/?court__jurisdiction!=F"
    # Related Filters: can join filters between APIs
    trump_eo_dockets = query_api(endpoint=tags_ep, parameters={'name': 'trump-executive-authority'})
    docket_ids = trump_eo_dockets['dockets'][0]
    dockets = []
    current_date = str(pd.Timestamp.now())
    date_last_queried = current_date.split(' ')[0]

    for docket_id in docket_ids:
        res = query_api(endpoint=dockets_ep, parameters={"id": docket_id})
        dockets.append(res)
    dockets_df = pd.concat(dockets, ignore_index=True)
    # TODO: get state court case abbreviation, change below to read from clusters column in dockets_df
    courts_df = pd.concat([query_api(endpoint=court) for court in dockets_df['court'].unique()], ignore_index=True)

    # Append date_last_queried to dfs
    dockets_df['date_last_queried'] = date_last_queried
    courts_df['date_last_queried'] = date_last_queried

    # Save dfs to csvs
    dockets_df.to_csv('../data/raw/dockets.csv')
    courts_df.to_csv('../data/raw/courts.csv')

    save_docket_resource_link()

def save_docket_resource_link():
    dockets = pd.read_csv('../../data/raw/dockets.csv')
    docket_entries = dockets[['id', 'absolute_url', 'case_name']]
    docket_entries['absolute_url'] = 'https://www.courtlistener.com' + docket_entries['absolute_url']
    docket_entries = docket_entries.rename(columns={'id': 'docket_id'})
    docket_entries.to_csv('../data/raw/docket_entry_info.csv')



if __name__=='__main__':
    update_data()
