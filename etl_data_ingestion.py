import os
import argparse
from time import time
import pandas as pd
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date, Numeric, Float, DateTime, Boolean, ForeignKey

def main(params):
    user = params.user
    password = params.password
    host = params.host 
    port = params.port 
    db = params.db

    print("Before connecting")

    engine = create_engine(f'postgresql://{user}:{password}@{host}:{port}/{db}')

    print("After connecting")
    
    df_crime = pd.read_csv('datasets/Crimes_Chicago_2022.csv')
    df_area = pd.read_csv('datasets/chicago_areas.csv')
    df_temp = pd.read_csv('datasets/chicago_temp_2022.csv')

    df_crime.columns = [x.replace(' ','_') for x in df_crime.columns]
    df_area.columns = [x.replace(' ','_') for x in df_area.columns]
    df_temp.columns = [x.replace(' ','_') for x in df_temp.columns]

    df_crime.Date = pd.to_datetime(df_crime.Date)
    df_temp.datetime = pd.to_datetime(df_temp.datetime)

    df_crime = df_crime[['ID', 'Case_Number', 'Date', 'Block','Primary_Type',
                        'Description', 'Location_Description', 'Arrest', 
                        'Domestic','Community_Area', 'Latitude', 'Longitude']]
    df_crime.columns = ["crime_id", "case_number", "crime_date", "street_name", 
                        "crime_type", "crime_description", "location_description", 
                        "arrest", "domestic", "community_area_id", "latitude", "longitude"]

    df_area = df_area[['community_area_id', 'name', 'population', 'area_sq_mi', 'density']]
    df_area.columns = ['area_id', 'area_name', 'population', 'area_size', 'population_density']

    df_temp = df_temp[['datetime','tempmax', 'tempmin','precip']]
    df_temp.columns = ['Weather_Date','Temp_max','Temp_low','Precipitation']

    meta = MetaData()

    areas = Table(
    'areas', meta, 
        Column('area_id',Date, primary_key = True), 
        Column('area_name', String(100)), 
        Column('population', Integer),
        Column('area_size', Float),
        Column('population_density', Float)
    )


    crimes = Table(
    'crimes', meta, 
        Column('crime_id', Integer, primary_key = True), 
        Column('case_number', String(50)), 
        Column('crime_date', DateTime),
        Column('street_name', String(50)),
        Column('crime_type', String(50)),
        Column('crime_description', String(50)),
        Column('location_description', String(50)),
        Column('arrest', Boolean),
        Column('domestic', Boolean),
        Column('community_area_id', Integer),
        Column('latitude', Float),
        Column('longitude', Float)
    )


    weather = Table(
    'weather', meta, 
        Column('weather_date',Date, primary_key = True), 
        Column('temp_max', Float), 
        Column('temp_low', Float),
        Column('precipitation', Float)
    )

    meta.create_all(engine)

    df_area.to_sql(name='areas', con=engine, if_exists='append',index=False)
    df_crime.to_sql(name='crimes', con=engine, if_exists='append',index=False)
    df_temp.to_sql(name='weather', con=engine, if_exists='append',index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingesting CSV data to Postgres')

    parser.add_argument('--user', required=True, help='user name for postgres')
    parser.add_argument('--password', required=True, help='password for postgres')
    parser.add_argument('--host', required=True, help='host for postgres')
    parser.add_argument('--port', required=True, help='port for postgres')
    parser.add_argument('--db', required=True, help='database name for postgres')

    args = parser.parse_args()

    main(args)