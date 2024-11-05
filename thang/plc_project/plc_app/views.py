from django.shortcuts import render, redirect
from .forms import PLCAddressForm, InfluxDBForm
import logging
import snap7
import json
import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# InfluxDB client initialization
INFLUXDB_HOST = '192.168.1.102'
INFLUXDB_PORT = 8086
client = InfluxDBClient(host=INFLUXDB_HOST, port=INFLUXDB_PORT)

plc_data = []  # Initialize plc_data globally
json_data = {}

def publish_to_mqtt(json_data):
    """Publish JSON data to MQTT server."""
    MQTT_BROKER = '192.168.1.102'
    MQTT_PORT = 1883
    MQTT_TOPIC = 'iiot/data' 
    MQTT_USERNAME = 'thang'    
    MQTT_PASSWORD = 'raspberry'  

    client = mqtt.Client()
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD) 
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)
        logger.info("Publishing to MQTT: %s", json_data)
        client.publish(MQTT_TOPIC, json_data)
    except Exception as e:
        logger.error("Failed to publish to MQTT: %s", str(e))
    finally:
        client.disconnect()

def connectConnection(address='192.168.200.2', tsap=0x0100, tsaplogo=0x0100, Port=102):
    global plc
    plc = snap7.logo.Logo()
    try:
        plc.connect(address, tsap, tsaplogo, tcp_port=Port)
        logger.info("Connected to PLC at %s", address)
        return True
    except Exception as e:
        logger.error("Failed to connect to PLC: %s", str(e))
        return False

def contains_substring(string, substrings):
    for substring in substrings:
        if substring in string:
            return substring
    return False

def datatype2BitNumber(dataTypeName):
    dataTypeBits = {'X': 1, 'BOOL': 1, 'BYTE': 8, 'WORD': 16, 'INT': 16, 'DWORD': 32, 'REAL': 32, 'CHAR': 8, 'STRING': 254}
    return dataTypeBits.get(dataTypeName, None)

def string2Address(Address):
    commaIndex = Address.find(',')
    db_number = Address[2:commaIndex]
    typeNo = Address[commaIndex + 1:]
    dataTypes = ['BOOL', 'BYTE', 'DWORD', 'INT', 'WORD', 'REAL', 'CHAR', 'STRING', 'X']
    dataType = contains_substring(typeNo, dataTypes)
    if dataType is None:
        logger.error("Invalid data type in address: %s", Address)
        return None
    dotIndex = typeNo.find('.')
    if dotIndex < 0:
        addressNumber = typeNo[len(dataType):]
        lengthData = datatype2BitNumber(dataType)
    else:
        addressNumber = typeNo[len(dataType):dotIndex]
        lengthData = datatype2BitNumber(dataType)
    return (db_number, dataType, addressNumber, lengthData)

def readData(Address):
    parsedAddress = string2Address(Address)
    if not parsedAddress:
        return None
    dbNumber, dataType, addressNumber, lengthData = parsedAddress
    try:
        DB_bytearray = plc.db_read(int(dbNumber), int(addressNumber), int(lengthData))
        data = None
        if dataType == "BOOL" or dataType == "X":
            data = snap7.util.get_bool(DB_bytearray, 0, int(addressNumber))
        elif dataType == "DWORD":
            data = snap7.util.get_dword(DB_bytearray, 0)
        elif dataType == "WORD":
            data = snap7.util.get_word(DB_bytearray, 0)
        elif dataType == "REAL":
            data = snap7.util.get_real(DB_bytearray, 0)
        elif dataType == "INT":
            data = snap7.util.get_int(DB_bytearray, 0)
        elif dataType == "CHAR":
            data = snap7.util.get_char(DB_bytearray, 0)
        elif dataType == "STRING":
            data = snap7.util.get_string(DB_bytearray, 0)

        logger.info("Read data from PLC: %s", data)
        return data
    except Exception as e:
        logger.error("Error reading data: %s", str(e))
        return None

def save_to_influxdb(variable_name, address, data):
    """Save PLC data to InfluxDB."""
    json_body = [
        {
            "measurement": "plc_data",
            "tags": {
                "variable_name": variable_name,
                "address": address
            },
            "fields": {
                "value": data
            }
        }
    ]
    try:
        client.write_points(json_body)
        logger.info("Data written to InfluxDB: %s", json_body)
    except Exception as e:
        logger.error("Error writing to InfluxDB: %s", str(e))

def plc_view(request):
    global plc_data  # Use the global plc_data variable
    global json_data  # Use the global json_data variable

    if connectConnection():  # Connect to PLC
        if request.method == 'POST':
            form = PLCAddressForm(request.POST)

            # Check if the delete action is requested
            if 'delete' in request.POST:
                selected_entries = request.POST.getlist('selected_entries')  # Get selected entries to delete
                plc_data = [entry for entry in plc_data if entry['address'] not in selected_entries]  # Remove selected entries
                json_data = {entry['variable_name']: entry['data'] for entry in plc_data}  # Update JSON data
            else:
                # Normal form handling to read PLC data
                if form.is_valid():
                    address = form.cleaned_data['address']
                    variable_name = form.cleaned_data['variable_name']
                    if not address:  # Ensure address is not empty
                        logger.error("Address cannot be empty.")
                        form.add_error('address', 'Address cannot be empty.')
                        return render(request, 'plc_app/plc_form.html', {'form': form, 'plc_data': plc_data, 'json_data': json.dumps(json_data)})

                    data = readData(address)
                    
                    # Append new data if not already in plc_data
                    if data is not None and not any(entry['address'] == address for entry in plc_data):
                        plc_data.append({'address': address, 'data': data, 'variable_name': variable_name})
                    
                    # Update JSON data
                    if data is not None:
                        json_data[variable_name] = data
                        publish_to_mqtt(json.dumps(json_data))  # Publish JSON data to MQTT server
                        save_to_influxdb(variable_name, address, data)  # Save to InfluxDB
                    else:
                        logger.error("Failed to read data from PLC for address: %s", address)

        else:
            form = PLCAddressForm()
    else:
        logger.error("Could not establish connection to the PLC.")
        form = PLCAddressForm()

    # Retrieve stored data from InfluxDB for display
    try:
        influx_data = client.query('SELECT * FROM plc_data')
        influx_data_list = list(influx_data.get_points())
    except Exception as e:
        logger.error("Error retrieving data from InfluxDB: %s", str(e))
        influx_data_list = []

    return render(request, 'plc_app/plc_form.html', {
        'form': form, 
        'plc_data': plc_data, 
        'json_data': json.dumps(json_data),
        'influx_data': influx_data_list  # Pass InfluxDB data to template
    })

def create_database(db_name):
    """Create a new database in InfluxDB."""
    client.create_database(db_name)
    logger.info("Database created: %s", db_name)

def create_database_view(request):
    """View to handle database creation, deletion, and listing."""
    form = InfluxDBForm()  # Instantiate the form
    if request.method == 'POST':
        if 'create' in request.POST:
            form = InfluxDBForm(request.POST)
            if form.is_valid():
                db_name = form.cleaned_data['db_name']
                create_database(db_name)
                return redirect('plc_view')  # Redirect to PLC view after creating database
        elif 'delete' in request.POST:
            db_name = request.POST.get('database_name')
            if db_name:
                delete_database(db_name)
                return redirect('plc_view')  # Redirect to PLC view after deleting database

    databases = list_databases()  # List all databases
    return render(request, 'plc_app/create_database.html', {'form': form, 'databases': databases})

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