import pandas as pd

def get_executive_orders_by_docket():
    df = pd.read_csv('../../data/raw/executive_orders_by_docket.csv')

    keep_cols = ['docket_id', 'EO Title']
    df = df[keep_cols]

    df = df.rename(columns={'EO Title': 'related_executive_orders'})

    df['related_executive_orders'] = df['related_executive_orders'].str.split("\n")
    df = df.dropna(subset=['related_executive_orders'])
    df['related_executive_orders'] = df['related_executive_orders'].apply(lambda x: [entry.lower().strip() for entry in x])

    df = df.explode('related_executive_orders')

    return df

def get_executive_orders_list():
    df = pd.read_csv('../../data/raw/executive_orders.csv')
    df['title'] = df['title'].str.lower()
    df['title'] = df['title'].str.strip()
    return df