# plc_app/views.py

from django.shortcuts import render
from .forms import PLCAddressForm
import logging
import snap7
import json  
import paho.mqtt.client as mqtt



logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

plc_data = []  # Initialize plc_data globally
json_data = {}

def publish_to_mqtt(json_data):
    """Publish JSON data to MQTT server."""
    MQTT_BROKER = '192.168.0.121'
    MQTT_PORT = 1883
    MQTT_TOPIC = 'iiot/data'  # Specify your MQTT topic here

    client = mqtt.Client()
    try:
        client.connect(MQTT_BROKER, MQTT_PORT, 60)  # Connect to the broker
        logger.info("Publishing to MQTT: %s", json_data)  # Log the data being published
        client.publish(MQTT_TOPIC, json_data)  # Publish the JSON data
    except Exception as e:
        logger.error("Failed to publish to MQTT: %s", str(e))
    finally:
        client.disconnect()  # Ensure disconnection from the broker

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

def plc_view(request):
    global plc_data  # Use the global plc_data variable
    data = None
    if connectConnection():  # Connect to PLC
        if request.method == 'POST':
            form = PLCAddressForm(request.POST)
            if form.is_valid():
                address = form.cleaned_data['address']
                variable_name = form.cleaned_data['variable_name']  # Capture the variable name
                data = readData(address)

                # Append the address, its data, and the variable name to the plc_data list
                plc_data.append({'address': address, 'data': data, 'variable_name': variable_name})
        else:
            form = PLCAddressForm()
    else:
        logger.error("Could not establish connection to the PLC.")
        form = PLCAddressForm()

    return render(request, 'plc_app/plc_form.html', {'form': form, 'plc_data': plc_data})

def plc_view(request):
    global plc_data  # Use the global plc_data variable
    global json_data  # Use the global json_data variable
    data = None
    if connectConnection():  # Connect to PLC
        if request.method == 'POST':
            form = PLCAddressForm(request.POST)
            if form.is_valid():
                address = form.cleaned_data['address']
                variable_name = form.cleaned_data['variable_name']  # Capture the variable name
                data = readData(address)

                # Append the address, its data, and the variable name to the plc_data list
                plc_data.append({'address': address, 'data': data, 'variable_name': variable_name})

                # Update the json_data dictionary with the new value
                json_data[variable_name] = data

                # Log the updated JSON data
                logger.info("Updated JSON Data: %s", json.dumps(json_data))

                # Send the JSON data to MQTT server
                publish_to_mqtt(json.dumps(json_data))  # Publish the JSON data

        else:
            form = PLCAddressForm()
    else:
        logger.error("Could not establish connection to the PLC.")
        form = PLCAddressForm()

    return render(request, 'plc_app/plc_form.html', {'form': form, 'plc_data': plc_data, 'json_data': json.dumps(json_data)})
