#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from pyarrow.parquet import ParquetFile
import pyarrow as pa 
from time import time
import argparse
import os

def main(params):
    user = params.user
    password = params.password
    host = params.host
    port = params.port
    db = params.db
    table_name = params.table_name
    url = params.url
    pq_name = 'output_pq.parquet'
    zones_url = params.zones_url
    zones_csv = 'taxi_zones.csv'
    
    os.system(f"wget {url} -O {pq_name}")
    os.system(f"wget {zones_url} -O {zones_csv}")
        
    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')
    engine.connect()

    zones_df = pd.read_csv(zones_csv)
    zones_df.to_sql(name='zones', con=engine, if_exists='replace')
    
    pf = ParquetFile(pq_name)
    raw_df = pd.read_parquet(pq_name, engine='pyarrow')
    df = raw_df.head(2)

    df.tpep_pickup_datetime = pd.to_datetime(df.tpep_pickup_datetime)
    df.tpep_dropoff_datetime = pd.to_datetime(df.tpep_dropoff_datetime)
    df.head(n=0).to_sql(name=table_name, con=engine, if_exists='replace')

    def write_data_to_postgres(pf, table_name, batch_size):
        for chunk in pf.iter_batches(batch_size=batch_size):
            start = time()
            if not isinstance(chunk, pd.DataFrame):
                chunk = chunk.to_pandas()
            chunk.tpep_pickup_datetime = pd.to_datetime(chunk.tpep_pickup_datetime)
            chunk.tpep_dropoff_datetime = pd.to_datetime(chunk.tpep_dropoff_datetime)
            chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
            print(f'Chunk written in {(time()-start):.3f} seconds')
        print('All data written to Postgres!')

    write_data_to_postgres(pf, table_name=table_name, batch_size=100000)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Parquet data into Postgres')
    parser.add_argument('--user', required= True, help= 'user name for postgres')
    parser.add_argument('--password', required= True, help= 'password for postgres')
    parser.add_argument('--host', required= True, help= 'host for postgres')
    parser.add_argument('--port', required= True, help= 'port for postgres')
    parser.add_argument('--db', required= True, help= 'database name for postgres')
    parser.add_argument('--table_name', required= True, help= 'table name for postgres')
    parser.add_argument('--url', required= True, help= 'url for parquet file')
    parser.add_argument('--zones_url', required= True, help= 'url for zones csv file')

    args = parser.parse_args()
    main(args)