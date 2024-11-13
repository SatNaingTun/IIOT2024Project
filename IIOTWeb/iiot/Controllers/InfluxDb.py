import datetime
from django.shortcuts import redirect, render
# from ..forms import InfluxDBForm
from influxdb import InfluxDBClient
import logging

# InfluxDB client initialization
# INFLUXDB_HOST = '192.168.1.102'
INFLUXDB_HOST = '192.168.1.104'
INFLUXDB_PORT = 8086

# json_payLoad=[]
# data={
#     "measurement":"stocks",
#     "tags":{
#         "ticker":"TSLA"
#     },
#     "time":datetime.now(),
#     "fields":{
#         "open":688.37,
#         "close":667.93
         
#     }
# }

# client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)
# def connectConnection(host='192.168.1.102',port=8086):
def connectConnection(host='192.168.1.104',port=8086):
    global client
    client = InfluxDBClient(host, port)

    return client


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database(db_name):
    """Create a new database in InfluxDB."""
    client.create_database(db_name)
    logger.info("Database created: %s", db_name)

def createRetentionPolicy(db_name,duration):
    client.create_retention_policy(name=db_name,database=db_name,duration=duration,replication=1)

def alterRetentionPolicy(db_name,duration):
    client.alter_retention_policy(name=db_name,database=db_name,duration=duration,replication=1)
    


def create_measurement(name):
    """Create a new table in InfluxDB."""
    
    logger.info("Database created: %s", name)


def delete_database(db_name):
    """Delete a database from InfluxDB."""
    client.drop_database(db_name)
    logger.info("Database deleted: %s", db_name)

def list_databases():
    """List all existing databases in InfluxDB."""
    try:
        databases = client.get_list_database()
        return [db['name'] for db in databases]
    except Exception as e:
        logger.error("Error retrieving databases: %s", str(e))
        return []

def create_measurement(database_name, measurement_name, field_name="value", field_value=1):
    client.switch_database(database_name)
    json_body = [{
        "measurement": measurement_name,
        "fields": {
            field_name: field_value
        }
    }]
    client.write_points(json_body)
    logger.info(f"Measurement {measurement_name} created in database {database_name} with field {field_name}: {field_value}")

def get_list(database_name, measurement_name,query:str):
    client.switch_database(database_name)
    client.query(query)


if __name__=='__main__':
    connectConnection()
    # create_measurement('test5','tst_mes',field_value=5)
    create_measurement('gwiiot','tst_mes',field_value=5)

