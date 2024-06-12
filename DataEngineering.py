


from docker import DockerClient     #imports dockerclient class to interact with docker engine
import docker.errors                #imports error handling for docker operation
import psycopg2                     #imports psycopg2 library for connecting to postgresql database
import time                         #imports time library to introduce delays 
import requests                     #library to make HTTP request and downaload data from web
from urllib.parse import urljoin    #library to handle urls
import json                         #library to handle json data format

"""1.Setting up the PostgreSQL continer using Docker"""

image = "postgres:latest" #defining docker image for postgres db
client = DockerClient()   #creating docker client instance to interact with docker

"""2.Defining connection details for PostgreSQL database"""

host = "localhost"       
port = 5435
user = "postgres"
database = "postgres_world_bank"
password = 123456

"""3.Defining Docker container configuration"""

container_name = "postgres-docker-worldbank"  #defining docker postgresql container 
environment = {                               #defining environment variables for connection
    "POSTGRES_PASSWORD": password,
    "POSTGRES_DB": database,
}                       
ports = {"5432/tcp": port}                    #port mapping between container port 5432 & host port 5434
detach = True                                 # this allows the container to run in the background
volumes = {"/var/lib/postgresql/data": {"bind": "/var/lib/postgresql/data", "mode": "rw"}}  
# Postgresql data storage directiory is defined in this instance using volumes
# /var/lib/postgresql/data stores database files inside the container
# Binds this directory on the container to the same directory (/var/lib/postgresql/data) on the host machine 
# rw set volume to read-write


"""4. Logic execution to check for exisitng Docker container or creating a new one if doesn't exist"""

def create_or_run_container(client, container_name, image, environment, detach, ports, volumes):
    """
    Checks if a container with the given name exists.
    If it exists, prints a message indicating so.
    Otherwise, creates and runs a new container using the provided parameters.

    Args:
        client (docker.DockerClient): A Docker client object.
        container_name (str): The name of the container.
        image (str): The image to use for the container.
        environment (dict, optional): Environment variables to set for the container. Defaults to None.
        detach (bool, optional): Whether to run the container in detached mode. Defaults to True.
        ports (list, optional): A list of port mappings for the container. Defaults to None.
        volumes (list, optional): A list of volume mounts for the container. Defaults to None.

    Returns:
        docker.models.containers.Container: The created or retrieved container object.
    """

    # try block client.containers.get(client.containers.get(container_name)
    # is chekcing if an existing container with specified name already exist
    # if no existing container is found then except block handles this with client.containers.run()

    try:
        container = client.containers.get(container_name)
        print(f"Container {container_name} already exists.")
        return container
    
    except docker.errors.NotFound:
        print(f"initiating PostgreSQL: {container_name}")
        container = client.containers.run(
            image=image,
            name=container_name,
            environment=environment,
            detach=detach,
            ports=ports,
            volumes=volumes
        )
    return container



# url for world bank api endpoint to access gdp data
worldbank_api_url = "https://api.worldbank.org/v2/country/all/indicator/NY.GDP.MKTP.CD?format=json"

def get_data(worldbank_api_url):
    """fetches data from worldbank api URL using requests.get() 
    and converts repsone texxt to json format using json.loads(worldbank_api_response.text.
     Finally returning parse JSON data """

    worldbank_api_response  = requests.get(worldbank_api_url)
    worldbank_api_list      = json.loads(worldbank_api_response.text)
    return worldbank_api_list
    
    
def postgresqldb_connection(host,port,user,database,password):

    """ Tries to connect to a PostgreSQL database using connection details 
        (host, port, user, password, database) stored in variables.
        If successful, returns a connection object and a cursor object to interact with the database.
        If connection fails, prints an error message and returns None """

    try:
            conn = psycopg2.connect(
                    host = host,
                    port = port,
                    user = user,
                    database = database,
                    password = password)
            
            cursor = conn.cursor()
            return conn, cursor

    except Exception:
            print(f"database connection error: {Exception}")
            return None

def create_table(conn,cursor):

    """Takes a connection and cursor object as arguments.
        Defines a SQL statement to create a table named world_bank in the database. 
        The table stores information about GDP data with columns for indicator ID, indicator 
        name, country ID, country name, country code, date, value, unit, observation status, 
        and number of decimal places.
        
        Executes the SQL statement using the PostgreSQL's cursor and commits 
        the changes to the database.
        
        In case of errors, prints an error message. Closes the cursor and connection objects."""

    try:
        cursor.execute (
            """
            CREATE TABLE world_bank (
            
            indicator_id    VARCHAR NOT NULL,    
            indicator       VARCHAR NOT NULL,
            country_id      VARCHAR NOT NULL,
            country         VARCHAR NOT NULL,
            country_code    VARCHAR NOT NULL,
            date            VARCHAR NOT NULL, 
            value           FLOAT,
            unit            VARCHAR,
            obs_status      VARCHAR,
            decimal         INTEGER

            )
            """
        )

        conn.commit()
        #date if not entered varchar throws error
    except Exception:
        print(f"database connection in error: {Exception}")

    finally:
        cursor.close()
        conn.close()

def insert_table(conn, cursor,worldbank_api_list):

    """ Takes a connection, cursor, and list of data (from World Bank API) as arguments.
        Loops through each data item in the list.
        Extracts details like indicator ID, indicator name, country information, date, GDP value, unit, and other details.
        Uses the cursor to execute an SQL INSERT statement to add each data item as a new row in the world_bank table.
        Commits the changes to the database.
        In case of errors, prints an error message.
        Closes the cursor and connection objects."""
    try:
        for item in worldbank_api_list[1]:
        
            indicator_id    = item["indicator"]["id"]
            indicator       = item["indicator"]["value"]
            country_id      = item["country"]["id"]
            country         = item["country"]["value"]
            country_code    = item["countryiso3code"]
            date            = item["date"]
            value           = item["value"]
            unit            = item["unit"]
            obs_status      = item["obs_status"]
            decimal         = item["decimal"]

            if conn:
                cursor.execute(
                    """
                    INSERT INTO world_bank (
                    
                    indicator_id,    
                    indicator,
                    country_id,
                    country,
                    country_code,
                    date,
                    value,
                    unit,
                    obs_status,
                    decimal
                    )

                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""",
                    
                    (indicator_id,    
                    indicator,
                    country_id,
                    country,
                    country_code,
                    date,
                    value,
                    unit,
                    obs_status,
                    decimal)
                    
                    )
                
                conn.commit()

    except Exception as e:
        print(f"error conneting to database: {e}")

    finally:
        
        cursor.close()
        conn.close()


def main(worldbank_api_url):

    """This is the main function where the program execution starts.
        1.Calls get_data to retrieve data from the World Bank API using the provided URL.
        2.Inititaes Docker client connection to engage with Docker and create container
        3.Establishes a connection to the PostgreSQL database using postgresqldb_connection.
        4.Calls create_table to create the world_bank table (if it doesn't exist already).
        5.Accesses the first item in the retrieved data (worldbank_api_list) to get the current page number (page) and total number of pages (pages).
        6.Loops through all pages of data (from page to pages + 1).

        Inside the forloop:
        1.Establishes a new connection for each page to avoid potential connection issues.
        2.Constructs a new URL with the page number appended for pagination using urljoin.
        3.Calls get_data again to download data for the specific page.
        4.Calls insert_table to insert the data from that page into the database table."""

    worldbank_api_list = get_data(worldbank_api_url)
    client = DockerClient()
    container = create_or_run_container(client, container_name, image, environment, detach, ports, volumes)
    time.sleep(10) # Add a delay of 10 secs before attempting to connect to postgresql db
    conn, cursor = postgresqldb_connection(host,port,user,database,password)
    
    create_table(conn,cursor)
    
    i = worldbank_api_list[0]['page']
    j = worldbank_api_list[0]['pages'] +1


    for pg in range(i, j):
        conn, cursor = postgresqldb_connection(host,port,user,database,password)
        worldbank_api_url_loop = worldbank_api_url + f"&page={pg}"
        worldbank_api_list_loop = get_data(worldbank_api_url_loop)
        insert_table(conn, cursor,worldbank_api_list_loop)

main(worldbank_api_url) # calling the main fucntion




