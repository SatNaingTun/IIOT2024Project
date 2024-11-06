from .models import InputDevices, InputAddresses
from .PlcProtocols import PlcProtocol
from .PlcProtocols import S7PLCLogo
# from PlcAllInOne import *

def getCollect():
    dataDict={}
    # dataDict[Topic]=data
    # print(dataDict)
    inputDevices=InputDevices.objects.all()
    for inputDevice in inputDevices:
        inputAddresses=InputAddresses.objects.filter(device=inputDevice)
        for adr in inputAddresses:
        # adr.address getData(protocol_name,Address,IPAddress,Port,RackOrTsap,SlotOrTsapLogo)
            print(inputDevice.device_protocol)
            result=PlcProtocol.getData(inputDevice.device_protocol,adr.address,str(inputDevice.ip_address),inputDevice.port,inputDevice.rack,inputDevice.slot)
            # result=PlcProtocol.getData(inputDevice.device_protocol,adr.address,'192.168.200.2',102,0x0100,0x0100)
            
            print(result)
            # print(inputDevice.port)
            dataDict[adr.variable_name]=result
            
    print(dataDict)
    return dataDict



        
        
