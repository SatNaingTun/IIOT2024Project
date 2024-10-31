import snap7

plc = snap7.client.Client()

def connectConnection(address='192.168.200.250',rack=0,slot=1):
    plc.connect(address, rack, slot)

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
        return 32//4
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

def readAddress(Address):
    (dbNumber,dataType,addressNumber,lengthData)=string2Address(Address)
    # print("dbnumber"+str(dbNumber)+"datatype"+str(dataType)+"AddressNumber"+str(addressNumber)+"Length"+str(lengthData))
    # DB_bytearray = plc.db_read(dbNumber,0,lengthData)
    DB_bytearray = plc.db_read(int(dbNumber),0,int(lengthData))
    # total_prod = snap7.util.get_int(DB_bytearray,0)
    if(DB_bytearray is not None):
        if(dataType=="DWORD"):
            data = snap7.util.get_dword(DB_bytearray,0)

        if(dataType=="WORD"):
            data = snap7.util.get_word(DB_bytearray,0)
    
        if(dataType=="REAL"):
            data = snap7.util.get_real(DB_bytearray,0)
    
        if(dataType=="INT"):
            data = snap7.util.get_dint(DB_bytearray,0)

        if(dataType=="CHAR"):
            data = snap7.util.get_char(DB_bytearray,0)
    
        if(dataType=="STRING"):
            data = snap7.util.get_string(DB_bytearray,0)

        print(data)
    return data
# print(prod_rate)
# print(message)
# string2Address("DB5,DWORD0")
# plc.connect('192.168.200.250',0,1)

connectConnection()
readAddress("DB5,DWORD588")

# (db_number,dataType,addressNumber,lengthData)=string2Address("DB5,DWORD0")
# print("dbnumber"+str(db_number)+"datatype"+str(dataType)+"AddressNumber"+str(addressNumber)+"Length"+str(lengthData))
# changeConnection()