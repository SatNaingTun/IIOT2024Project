import snap7
import sys
import logging
# import snap7.type as t
from snap7.type import *


logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

def connectConnection(address='192.168.200.250',rack=0,slot=1,Port=102):
    global plc
    plc = snap7.client.Client()
    return plc.connect(address, rack, slot,Port)
        

def contains_substring(string, substrings):
    for substring in substrings:
        if substring in string:
            return substring
    return False

def datatype2BitNumber(dataTypeName):
    if(dataTypeName=='BOOL'):
        return 1
    if(dataTypeName=='BYTE'):
        return 8//4
    if(dataTypeName=='WORD'):
        return 16//4
    if(dataTypeName=='INT'):
        return 16//4
    if(dataTypeName=='DWORD'):
        return 32//4
    if(dataTypeName=='REAL'):
        # return 32//4
        return 4
    if(dataTypeName=='Char'):
        return 8//4
    if(dataTypeName=='STRING'):
        return 254//4

def string2Address(Address):
    commaIndex=Address.find(',')
    db_number=Address[2:commaIndex]
    # print(db_number)
    typeNo=Address[commaIndex+1:]
    # print(typeNo)
    dataTypes=['BOOL','BYTE','DWORD','INT','WORD','REAL','CHAR','STRING']
    dataType=contains_substring(typeNo,dataTypes)
    # print(cmdDataType)
    addressNumber=typeNo[len(dataType):]
    # print(addressNumber)
    lengthData=datatype2BitNumber(dataType)
    return (db_number,dataType,addressNumber,lengthData)
    # return db_number

def readData(Address):
    (dbNumber,dataType,addressNumber,lengthData)=string2Address(Address)
    # print("dbnumber"+str(dbNumber)+"datatype"+str(dataType)+"AddressNumber"+str(addressNumber)+"Length"+str(lengthData))
    # DB_bytearray = plc.db_read(dbNumber,0,lengthData)
    DB_bytearray = plc.db_read(int(dbNumber),0,int(lengthData))
    print(DB_bytearray)
    # logger.debug(f"Raw data read from PLC DB: {DB_bytearray.hex()}")
    # total_prod = snap7.util.get_int(DB_bytearray,0)
    if(DB_bytearray is not None):
        if(dataType=="BOOL"):
            data = snap7.util.get_bool(DB_bytearray,0)

        if(dataType=="DWORD"):
            data = snap7.util.get_dword(DB_bytearray,0)

        if(dataType=="WORD"):
            data = snap7.util.get_word(DB_bytearray,0)
    
        if(dataType=="REAL"):
            data = snap7.util.get_real(DB_bytearray,0)
            # data = struct.unpack('!f', DB_bytearray)[0]
    
        if(dataType=="INT"):
            data = snap7.util.get_dint(DB_bytearray,0)

        if(dataType=="CHAR"):
            data = snap7.util.get_char(DB_bytearray,0)
    
        if(dataType=="STRING"):
            data = snap7.util.get_fstring(DB_bytearray,0)

        print(data)
    return data

def writeData(Address):
    (dbNumber,dataType,addressNumber,lengthData)=string2Address(Address)
    # print("dbnumber"+str(dbNumber)+"datatype"+str(dataType)+"AddressNumber"+str(addressNumber)+"Length"+str(lengthData))
    # DB_bytearray = plc.db_read(dbNumber,0,lengthData)
    DB_bytearray = plc.db_fill(int(dbNumber),int(lengthData))
    plc.db_write(dbNumber,0,DB_bytearray)

# print(prod_rate)
# print(message)
# string2Address("DB5,DWORD0")
# plc.connect('192.168.200.250',0,1)

def ReadMemory(byte,dataType):
    result=plc.read_area(Areas['MK'],0,byte,dataType)
    if(dataType=="BOOL"):
        data = snap7.util.get_bool(byte,0)

    if(dataType=="DWORD"):
        data = snap7.util.get_dword(byte,0)

    if(dataType=="WORD"):
        data = snap7.util.get_word(byte,0)
    
    if(dataType=="REAL"):
        data = snap7.util.get_real(byte,0)
            # data = struct.unpack('!f', byte)[0]
    
    if(dataType=="INT"):
            data = snap7.util.get_dint(byte,0)

    if(dataType=="CHAR"):
        data = snap7.util.get_char(byte,0)
    
        if(dataType=="STRING"):
            data = snap7.util.get_fstring(byte,0)

        print(data)

if __name__=='__main__':
    # connected=connectConnection(address='192.168.200.250',rack=0,slot=1,Port=102)
    connected=connectConnection(address='192.168.200.250',rack=0,slot=1,Port=102)

    if(connected):
        logger.info("Connected")
        # readData("DB5,DWORD588")
        # readData("DB5,WORD604")
        # readData("DB5,REAL878")
        # readData("DB1,WORD1122")
        while True:
            user_address = input("Enter the PLC address to read (e.g., DB5,DWORD0) or 'exit' to quit: ")
            if user_address.lower() == 'exit':
                break
            readData(user_address)
       
        # while(1):
        #     cmd=input("Enter Address Cmd to read PLC address\n")
        #     readData(cmd)

    else:
        logger.error("Disconnected")


# (db_number,dataType,addressNumber,lengthData)=string2Address("DB5,DWORD0")
# print("dbnumber"+str(db_number)+"datatype"+str(dataType)+"AddressNumber"+str(addressNumber)+"Length"+str(lengthData))
# changeConnection()