from django.shortcuts import redirect, render
from iiot.forms import InfluxDBForm
from influxdb import InfluxDBClient
import logging

# InfluxDB client initialization
INFLUXDB_HOST = '192.168.1.102'
INFLUXDB_PORT = 8086
client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_database(db_name):
    """Create a new database in InfluxDB."""
    client.create_database(db_name)
    logger.info("Database created: %s", db_name)


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
