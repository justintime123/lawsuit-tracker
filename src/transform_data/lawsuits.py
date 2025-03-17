import pandas as pd

def get_dockets():
    df = pd.read_csv('../../data/raw/dockets.csv')

    df['absolute_url'] = 'https://www.courtlistener.com' + df['absolute_url']

    keep_cols = ['id', 'court_id',  'case_name', 'absolute_url', 'date_filed', 'date_modified', 'date_last_queried']

    return df[keep_cols]

def get_courts():
    #full_name = {Type of Court}, {State}
    df = pd.read_csv('../../data/raw/courts.csv')

    df['court_type'] = df['full_name'].apply(lambda x: x.split(',')[0])
    df['court_name'] = df['full_name'].apply(lambda x: x.split(',')[1])

    keep_cols = ['id', 'court_type', 'court_name']
    df = df[keep_cols]

    return df