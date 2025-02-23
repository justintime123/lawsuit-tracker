import pandas as pd
from src.api.federal_register_api import query_api, documents_req_url


def update_data():
    executive_orders_df = query_api(documents_req_url)
    current_date = str(pd.Timestamp.now())
    date_last_queried = current_date.split(' ')[0]

    executive_orders_df['date_last_queried'] = date_last_queried
    executive_orders_df.to_csv('../data/raw/executive_orders.csv')

if __name__=='__main__':
    update_data()

