from .models import InputDevices, InputAddresses,MqttServers
from .PlcProtocols import PlcProtocol
from .PlcProtocols import S7PLCLogo
from .Controllers import RepeatedTimer, MyMqtt
import json

 
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
        client.publish(mqttServer.topic, str(dataDict))
        client.disconnect()
            #json.dumps(myDict)   
    # print(dataDict)
    return dataDict

def getCollectByInputDevice(device_id):
    dataDict={}
    # dataDict[Topic]=data
    # print(dataDict)
   
    mqttServers=MqttServers.objects.all()
    inputDevice=InputDevices.objects.get(device_id=device_id)
   
    inputAddresses=InputAddresses.objects.filter(device=inputDevice)
    for adr in inputAddresses:
            
        result=PlcProtocol.getData(inputDevice.device_protocol,adr.address,str(inputDevice.ip_address),inputDevice.port,inputDevice.rack,inputDevice.slot)
        dataDict[adr.variable_name]=result
        adr.data=str(result)
        adr.save(update_fields=['data'])
        
            
    for mqttServer in mqttServers :
        client=MyMqtt.connect_mqtt(mqttServer.ip_address,mqttServer.port,mqttServer.mqtt_user_name,mqttServer.mqtt_password)
        client.publish(mqttServer.topic, str(dataDict))       
    # print(dataDict)
    return dataDict

def getCollectBySchedule(myTime):
    # dataDict = RepeatedTimer.RepeatedTimer(myTime, getCollect)
    # print(dataDict)
    
    RepeatedTimer.RepeatedTimer(1, getCollect)




        
        
