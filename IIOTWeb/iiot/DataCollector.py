from .models import InputDevices, InputAddresses,MqttServers
from .PlcProtocols import PlcProtocol
from .PlcProtocols import S7PLCLogo
from .Controllers import RepeatedTimer, MyMqtt

 
# from PlcAllInOne import *

def getCollect():
    dataDict={}
    # dataDict[Topic]=data
    # print(dataDict)
    inputDevices=InputDevices.objects.all()
    mqttServers=MqttServers.objects.all()
    
    for inputDevice in inputDevices:
        dataDict2={}
        inputAddresses=InputAddresses.objects.filter(device=inputDevice)
        for adr in inputAddresses:
            
            result=PlcProtocol.getData(inputDevice.device_protocol,adr.address,str(inputDevice.ip_address),inputDevice.port,inputDevice.rack,inputDevice.slot)
            dataDict2[adr.variable_name]=result
            adr.data=str(result)
            adr.save(update_fields=['data'])
        dataDict[inputDevice]=dataDict2
            
    for mqttServer in mqttServers :
        client=MyMqtt.connect_mqtt(mqttServer.ip_address,mqttServer.port,mqttServer.mqtt_user_name,mqttServer.mqtt_password)
        client.publish("iiot/data", str(dataDict))       
    # print(dataDict)
    return dataDict

def getCollectByInputDevice(device_id):
    dataDict={}
    # dataDict[Topic]=data
    # print(dataDict)
    inputDevices=InputDevices.objects.all()
    for inputDevice in inputDevices:
        inputAddresses=InputAddresses.objects.filter(device=inputDevice)
        for adr in inputAddresses:
        # adr.address getData(protocol_name,Address,IPAddress,Port,RackOrTsap,SlotOrTsapLogo)
            # print(inputDevice.device_protocol)
            # print("",adr.address)
            # print("",inputDevice.ip_address)
            # print(inputDevice.port)
            # print(inputDevice.rack)
            # print(inputDevice.slot)

            result=PlcProtocol.getData(inputDevice.device_protocol,adr.address,str(inputDevice.ip_address),inputDevice.port,inputDevice.rack,inputDevice.slot)
            # result=PlcProtocol.getData(inputDevice.device_protocol,adr.address,'192.168.200.2',102,0x0100,0x0100)
            adr.data=result
            adr.save(update_fields=['data'])
            print(result)
            # print(inputDevice.port)
            dataDict[adr.variable_name]=result
            
    print(dataDict)
    return dataDict

def getCollectBySchedule(myTime,status):
    dataDict = RepeatedTimer.RepeatedTimer(myTime, getCollect)
    # print(dataDict)
    # RepeatedTimer.RepeatedTimer(10, print, 'Hello world')




        
        
