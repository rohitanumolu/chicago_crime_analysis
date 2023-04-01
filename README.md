# End-to-End Chicago Crime Analysis

Created an End-to-end crime analysis of Chicago city. Streamlined the deployment process utilizing Docker by containerizing PostgreSQL and PgAdmin removing the hassle of installing and setting up each service. 

Gathered the data from [Chicago Data portal](https://data.cityofchicago.org/Public-Safety/Crimes-2022/9hwr-2zxp/data) and [Visual Crossing](https://www.visualcrossing.com/weather-history/Chicago%2CUnited+States). 

Docker compose allows us to run multi-container docker applications, by specifying a number of services that must be run together in a single YAML file. For more information, see [docker docs](https://docs.docker.com/compose/). Having both Dockerfile and docker-compose.yaml ready we can run 

```
docker build t image_name . 
```
in the command line from the directory of the files. Once this is successful we can run the Dockerfile which has the data ingestion script to be loaded as image is run. 

```
docker run -it image_name --user=root --password=root --host=pgdatabase --port=5432 --db=chicago_crimes
```
This provides python script, arguments needed to make the connected to the postgreSQL using SQL Alchemy. Make sure the information matches with the information of postgres image provided in the Dockerfile. 

This should successfully insert the data into the chicago_crimes database of Postgres server. 

As the connection is made to pgadmin in same network, an initial analysis was performed in pgAdmin answering various questions in the data. PgAdmin can be opened by >http://localhost:8080/browser/ (Port number provided in the image). 

A connection to the database was set in Power BI for easy dataflow in which the analysis report was made. 