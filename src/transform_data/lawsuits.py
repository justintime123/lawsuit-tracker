import pandas as pd

def get_dockets():
    return pd.read_csv('../../data/raw/dockets.csv')

def get_courts():
    #full_name = {Type of Court}, {State}
    return pd.read_csv('../../data/raw/courts.csv')

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