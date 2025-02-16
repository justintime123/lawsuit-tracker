from api import tags_ep, dockets_ep
import pandas as pd

from src.api import query_api

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
    dockets_df.to_csv('../data/dockets.csv')
    courts_df.to_csv('../data/courts.csv')

def get_dockets():
    return pd.read_csv('../data/dockets.csv')

def get_courts():
    #full_name = {Type of Court}, {State}
    return pd.read_csv('../data/courts.csv')

def get_data():
    dockets = get_dockets()
    courts = get_courts()

    #Join dockets with courts
    #court_id in dockets = id in courts
    #More info on .concat() vs .merge(): https://stackoverflow.com/questions/38256104/differences-between-merge-and-concat-in-pandas
    #.concat() is recommended for joining homogenous dfs, while merge() is good for joining complementary dfs
    combined_data = dockets.merge(courts, left_on='court_id', right_on='id', suffixes=('_docket', '_court'))

    return combined_data

#TODO: add keep_cols section to get_dockets() and get_courts()
#TODO: Add latest_status and executive_order_referenced columns to combined_data
# #Downloading docket resources to get (1) latest update/status (info within latest docket entry) and (2) Executive order referenced in initial Complaint document
    #Examples of statuses: Appeal
    #Using PACER Data API
    #https://www.courtlistener.com/help/api/rest/pacer/
    #https://judiciallearningcenter.org/state-courts-vs-federal-courts/
    #PACER applies to federal courts only (US District Courts, US Court of Appeals, and U.S. Supreme Court)
    #State Courts (e.g.) - Missouri Circuit Courts, Missouri Court of Appeals, Missouri Supreme Court


if __name__=='__main__':
    data = get_data()
