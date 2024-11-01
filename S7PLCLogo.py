import snap7
import logging

logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

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
    dataTypeBits = {'X': 1,'BOOL':1, 'BYTE': 8, 'WORD': 16, 'INT': 16, 'DWORD': 32, 'REAL': 32, 'CHAR': 8, 'STRING': 254}
    return dataTypeBits.get(dataTypeName, None)

def string2Address(Address):
    commaIndex = Address.find(',')
    db_number = Address[2:commaIndex]
    typeNo = Address[commaIndex+1:]
    dataTypes = ['BOOL', 'BYTE', 'DWORD', 'INT', 'WORD', 'REAL', 'CHAR', 'STRING','X']
    dataType = contains_substring(typeNo, dataTypes)
    if dataType is None:
        logger.error("Invalid data type in address: %s", Address)
        return None
    dotIndex = typeNo.find('.')
    print("DotIndex",dotIndex)
    if dotIndex<0:
        addressNumber = typeNo[len(dataType):]
        # print("My address Number1 is",addressNumber)
        lengthData = datatype2BitNumber(dataType)
    else:
        addressNumber = typeNo[len(dataType):dotIndex]
        # print("My address Number2 is",addressNumber)
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
        if dataType == "BOOL" or dataType=="X":
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

def askCommand():
    if connectConnection():
        while True:
            user_address = input("Enter the PLC address to read (e.g., DB1,WORD1122) or 'exit' to quit: ")
            if user_address.lower() == 'exit':
                break
            readData(user_address)
            # string2Address(user_address)
    else:
        logger.error("Could not establish connection to the PLC.")


string2Address('DB1,X1024.0')

# if __name__ == '__main__':
#    askCommand()
