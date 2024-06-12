Here's the modified syntax for your GitHub README:

```markdown
# Data Engineering Challenge

## Dependencies

### Operating System: Mac OS 

### Tools 
1. Python version python 3.11.2 in Visual Studio Code
2. PostgreSQL hosted on Docker acting as database for our operation. pgAdmin4 application is used to connect Postgres (postgresql 16.3) on my local system to server of Docker container containing Postgres.
3. dbt to build models and test cases
4. Github for version control
5. Tableau Public for visualisation  

### Scripts 
1. `DataEngineering.py` script has been used to fetch data from API, build Docker container, access PostgreSQL in Docker to ingest data into database
2. dbt folder in the repo contains dbt virtual environment inside which dbt dependencies have been installed and dbt project folder has been created to create models and perform test cases
3. Github has been used to create repository

## Installation 

### Docker (performed thes steps inside bash terminal)
1. Install the docker postgres image. And after installation using following commands to initiate the image `docker start postgres-docker`. And use the `docker image ls` command to list all the images that are active
2. Initiate the docker container with docker run command and with necessary variables. For e.g. `docker run --name postgres-docker-worldbank --env POSTGRES_PASSWORD= 123456 -p 5435:5432 --detach --network=host postgres`
3. Use this command to check if the container is up and running `docker ps`
4. `docker exec -it postgres-docker  bash` to engage with postgressql
5. Once psql initiates `psql -h localhost -p 5435  -U postgres -W` or `psql -U postgres` or `psql -h localhost -p 5435  -U postgres -W`
8. After this instance one can execute sql commands for e.g. "CREATE DATABASE mytestdb;" to execute interaction with database.

### dbt 
1. Initialise the virtual environment after installing dbt in VS code. For e.g. `python3 -m venv dbt-env`
2. Activate dbt in your virtual environment using dbt command, `source dbt-env/bin/activate`
3. Install any required dependencies for e.g .in our case dbt core and postgres database are required to be able to create model. So you can use such command `python3 -m pip install dbt-core dbt-postgres`
4. To check dbt version on our system `dbt --version`
5. `dbt debug` can be initiated to perform the connection test
6. `cat profiles.yml` for .dbt file can  be used to get across the yml file containing profile information
7. `dbt init` will run dbt and ask few questions such as project name - `dbt_worldbank_project`
8. `Enter a number: 1`
   `host (hostname for the instance): localhost`
   `port [5432]: 5435`
   `user (dev username): postgres`
   `pass (dev password): 123456`
   `dbname (default database that dbt will build objects in): postgres_world_bank`
   `schema (default schema that dbt will build objects in): postgres_world_bank_dbt`
   `threads (1 or more) [1]: 5` 
9. Once your connection have passed you can run `dbt run --select my_first_dbt_model` where `my_first_dbt_model.sql` is a sample sql script that dbt will have within its model directory. And create own custom scripts as per our need under model &     
   test 
10. `dbt test` can be used to test out any case while executing the file

### PostgreSQL
1. Inititiated postgres installation by following EDB installer
2. Set the password, port during the installation for PostgresSQL
3. Set the correct connection setting for host, port, username and password to connect to the server from initiated on the Docker instance.

### Approach to complete Task 1 and Task 2

#### Task1 Data ingestion and database setup

1. Prior to performing task made sure all my tools such as VS studio, Docker, pgAdmin4, dbt and Github were connected with my user settings and accessible to perform the task
2. Firstly, for task 1 I tried to establish a working connection bewtween my python script fetching information from API, creating a table inside the PostgreSQL application and ingesting into the table undergoing a loop based on api pages as identified from the api's JSON data structure. The database server from my local machine was connected with Docker container containing image of PostgreSQL. I used a python script to handle "DataEngineering.py" to define Docker setting's and initiate Docker engine for building container with postgres image. Following on this the databse connection details have been specified within the script.
3. Upon executing the DataEngineering.py script the following occurs:
     1.get_data function to retrieve data from the World Bank API using the provided URL.
     2.Inititaes Docker client connection to engage with Docker and create container using postgres image.
     3.Establishes a connection to the PostgreSQL database using postgresqldb_connection.
     4.Calls create_table function conatining SQL query to create the world_bank table. The table schema was defined in this section
     5.Accesses the first item in the retrieved data (worldbank api) to get the current page number (page) and total number of pages (pages).
     6.Loops through all pages of data.

     Inside the loop:
     1.Establishes a new database connection for each page to avoid potential connection issues.
     2.Constructed a new URL with the page number appended for pagination using urljoin.
     3.Function get_data again was used to download data for the specific page.
     4.Function insert_table was used to insert the data from that page into the database table.

     Errors handled during execution:
     1. While insatlling libraries to perform task module installation errors were handled 
     2. Incorrect server setting being mapped for local Postgres server to Docker's Postgres instance. To handle this after initialising Docker container time delay was added to script before attempting to connect to PostgreSQL server.
     3. While using PostgresSQL connection the connection timeout using create table statements posed a problem to not execute insert values into tables SQL quiery. I handlded this of the query by re initiating the connection before ingestion into
        respective database table occurs.
     4. During table creation the schema of data posed a problem for values that were being ingested. For e.g. date field contained year but upon defining it as date in schema posed an ingestion problem. To handle this case i defined the schema as             varchar for date so that ingestion occurs and later using dbt I can control the data type of the columns
     5. While converting the entire script into resuable code my making functions and using inheritance the sequential execution of task posed a problem. Hence, I arranged the steps sequentially such as : 1.api call function, 2. Docker client,   
        function, 3. Docker container creation fucntion, 4.time delay before initiating database connection, 5.PostgreSQL connection function, 6.Creating the database table fucntion, 7.Performing the loop exectuion taking care of pagination for                fetching data from api and 8. calling the main function to execute all of the above.
     6.While defining unique within table schema for coulms faced the following errors during ingestion:
       #error conneting to database: duplicate key value violates unique constraint "world_bank_pkey"
       #DETAIL:  Key (indicator_id)=(NY.GDP.MKTP.CD) already exists.
       #error conneting to database: null value in column "value" of relation "world_bank" violates not-null constraint
       #DETAIL:  Failing row contains (NY.GDP.MKTP.CD, GDP (current US$), ZH, Africa Eastern and Southern, AFE, 2023, null, , , 0).
       I handled them by removing such constraints in the schema as I can later control these situations while defining in dbt.


     Output:
     1. Ingested all historic GDP (in US$) data for all countries using the World Bank API and imported the data into a PostgreSQL database. Handled the API is pagination
     2. Before loading the raw data into a local PostgreSQL database, hosted postgres on Docker and mapped server connection. Defined a table schema in python script create table, and imported the data from the API into the database using insert               statement.

  
#### Task2 Data transformation
1. As we have already established dbt connection to perform data transformation "world_bank_gdp.sql" for model creation and produce output as table is utitlised. And "world_bank_gdp_test.sql" for handling test case has been utilised.
2. "world_bank_gdp.sql":
    Defined mulitple CTE's:
    1. to handle source_data by selecting data from the world_bank table and renames columns for to align with Output:
    2. country is renamed to Country
    3. Year is extracted from the date column using to_date and extract functions (assuming the date format is YYYY) and named Year
    4. value is renamed to Gdp
    5. ranking of columns for each country ordered by year
    6. calculating the GDP growth for each country and year
    7. calculating the minimum and maximum GDP growth for each country since the year 2000 to the current year the row represents (not to the latest year)
    8. ensuring gdp value is not null and year range initates from 2000 onwards
    9. used SQL queries to cast data type of each column as hihglighted in the output
    10.finally executed the queries and fetched the output. The output csv file "world_bank_gdp.csv" stores the model's output to be referenced further.
    11.under schema.yml file within dnt project's model defined the model and column data type
     
3. "world_bank_gdp_test.sql":
    1. Wrote one test case to find count of instances where either country is null or year is null or Gdp is null
4. Errors handled during execution:
    2. execution of CTE's to obtain desired logic for transformations such as GDP growth, minimum and maximum GDP growth since the year 2000 to the current year the row represents (not to the latest year) were challenging, I handled this my         
       implementing first building the logic and then getting the syntac for SQL query correct to get the desrired outcome. And performing a one on one comparision for the same with the output specified.
5. Output:
    1.Performed an ELT (Extract, Load, Transform) process on the ingested data in Postgres databse table to create a table that aligns with the provided format. The table contains information about countries' GDPs recorded every year since 2000. 
    2. Wrote 1 test case in dbt.
    3. Implemented CI/CD using GitHub. Performed one Pull Request (PR) to demonstrate your integration of CI/CD principles in my workflow. 
    4. The table columns were aligned as per below 
      a. Country 
      b. Year 
      c. Gdp 
      d. gdp_growth = calculated as ( gdp - previous year gdp ) / previous year gdp 
      e. min_gdp_growth_since_2000: (minimum GDP growth from year 2000 to the current year the row represents (not to the latest year) 
      f. max_gdp_growth_since_2000: (maximum GDP growth from year 2000 to the current year the row represents (not to the latest year). 
       

   



        
        
```
