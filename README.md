Here's the modified syntax for your GitHub README:

```markdown
# Data Engineering Challenge

## Dependencies 

### Tools 
1. Python version (3.x) in Visual Studio Code
2. PostgreSQL hosted on Docker acting as database for our operation
3. dbt to build models and test cases   

### Scripts 
1. `DataEngineering.py` script has been used to fetch data from API, build Docker container, access PostgreSQL in Docker to ingest data into database
2. dbt folder in the repo contains dbt virtual environment inside which dbt dependencies have been installed and dbt project folder has been created to create models and perform test cases
3. Github has been used to create repository

## Installation 

### Docker 
1. Install the docker postgres image. And after installation using following commands to initiate the image `docker start postgres-docker`. And use the `docker image ls` command to list all the images that are active
2. Initiate the docker container with docker run command and with necessary variables. For e.g. `docker run --name postgres-docker --env POSTGRES_PASSWORD=pstgres123456 -p 5433:5432 --detach --network=host postgres`
3. Use this command to check if the container is up and running `docker ps`
4. `docker exec -it postgres-docker  bash` to engage with postgressql
5. Once psql initiates `postgres-# psql -h localhost -p 5433  -U postgres -W`
6. Inside psql `psql -U postgres` or `postgres-# psql -h localhost -p 5433  -U postgres -W`
7. psql (16.3 (Debian 16.3-1.pgdg120+1))
8. `postgres=#` within this instance one can execute sql commands for e.g. `CREATE DATABASE mytestdb;`

### dbt 
1. Initialise the virtual environment after installing dbt in VS code. For e.g. `python3 -m venv dbt-env`
2. Activate dbt in your virtual environment using dbt command, `source dbt-env/bin/activate`
3. Install any required dependencies for e.g .in our case dbt core and postgres database are required to be able to create model. So you can use such command `python3 -m pip install dbt-core dbt-postgres`
4. To check dbt version on our system `dbt --version`
5. `dbt debug` can be initiated to perform the connection test
6. `cat profiles.yml` for .dbt file can  be used to get across the yml file containing profile information
7. `dbt init` will run dbt and ask few questions such as project name 
8. Once your connection have passed you can run `dbt run --select my_first_dbt_model` where `my_first_dbt_model.sql` is a sql script that dbt will have within its model directory. And create own custom scripts as per need under model, test 
9. `dbt test` can be used to test out any case while executing the file

### PostgreSQL
(Add PostgreSQL related instructions here)
```
