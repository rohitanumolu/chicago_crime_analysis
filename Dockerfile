FROM python:3.11.2

RUN pip install pandas sqlalchemy psycopg2

WORKDIR /app
COPY etl_data_ingestion.py etl_data_ingestion.py
COPY chicago_areas.csv chicago_areas.csv 
COPY Crimes_Chicago_2022.csv Crimes_Chicago_2022.csv 
COPY chicago_temp_2022.csv chicago_temp_2022.csv 

ENTRYPOINT [ "python", "etl_data_ingestion.py" ]
