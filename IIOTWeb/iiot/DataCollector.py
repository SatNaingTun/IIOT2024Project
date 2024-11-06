from .models import InputDevices, InputAddresses
from PlcProtocols import PlcProtocol
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
            result=PlcProtocol.getData(inputDevice.device_protocol,inputDevice.ip_address,inputDevice.port,inputDevice.rack,inputDevice.slot)
            dataDict[adr.variable_name]=result

    print(dataDict)
    return dataDict


getCollect()


        
        
