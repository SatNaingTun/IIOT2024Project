from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
# from .Controllers import PlcAllInOne
from .PlcProtocols import PlcProtocol
from .Controllers import S7PLCLogo
from .models import InputDevice
from .forms import InputDeviceForm
from .forms import MqttServerForm
from .models import MqttServer

# Create your views here.
plc_data = []

def listInputDevices(request):
    inputDevices=InputDevice.objects.all()
    context={
         'inputDevices':inputDevices
     }
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request,"iiot/listInputDevices.html",context)

def test(request):
    plc_data=[]
    if request.method=='GET':
        return render(request,"iiot/test.html")
    elif request.method=='POST':
        # form = PLCAddressForm(request.POST)
        var_name = request.POST.get('variable_name')
        # print(var_name)
        AddressMemory = request.POST.get('AddressMemory')
        # print(AddressMemory)
        ip=request.POST.get('IPAddressPLC')
        port=request.POST.get('PlcPort')
        protocol_name=request.POST.get('PlcProtocol')
        rack=request.POST.get('Rack')
        slot=request.POST.get('Slot')
        print(protocol_name)
        result=PlcProtocol.getData(protocol_name,AddressMemory,ip,int(port),rack,slot)
        
        if result is not None:
            plc_data.append({'address': AddressMemory, 'data': result, 'variable_name': var_name})
        else:
            messages.error(request,"Check Your Connection")
        return render(request,"iiot/test.html",{'plc_data': plc_data})

        
                 
        # if S7PLCLogo.connectConnection()==True:
        #         data=S7PLCLogo.readData(AddressMemory)
        #         plc_data.update({'address': AddressMemory, 'data': data, 'variable_name': var_name})
        #         print(plc_data)
        # else:
        #         messages.error(request,"Connection Error")
        # return render(request,"iiot/test.html",{'form':form,'plc_data': plc_data})
        # messages.info(request,'You clicked the submit button')
        # return redirect(test)
def testLocal(request):
    plc_data=[]
    
    
    
    if request.method=='GET':
        return render(request,"iiot/test.html")
    elif request.method=='POST':
        # PlcAllInOne.getData(protocol_name)
        var_name = request.POST.get('variable_name')
        # print(var_name)
        AddressMemory = request.POST.get('AddressMemory')

        protocol_name=request.POST.get('PlcProtocol')
        # print(protocol_name)
        plc_data.append({'address': AddressMemory, 'data': 5, 'variable_name': var_name})
        # print(plc_data)
        # print(plc_data.get('variable_name'))
        return render(request,"iiot/test.html",{'plc_data': plc_data})
       
def mqtt_view(request):
     if request.method=='POST':
          pass
     elif request.method=='GET':
          return render(request,'iiot/mqtt.html')
         
def registerInputDevice(request):
   
          
     if request.method=='POST':
        try:
          inputDeviceForm=InputDeviceForm(request.POST)
          if inputDeviceForm.is_valid():
              inputDevice=inputDeviceForm.save()
              messages.info(request,f'{inputDevice.device_name} saved Successfully')
        except Exception as e:
            print(e)
            messages.error(request,'An error occurred while saving InputDevice')
        return redirect(registerInputDevice)

     elif request.method=='GET':
          inputDeviceForm=InputDeviceForm()
          return render(request,'iiot/registerInputDevice.html',{"inputDeviceForm":inputDeviceForm})
     
            
def registerMqtt(request):
   
          
     if request.method=='POST':
        try:
          mqttServerForm=MqttServerForm(request.POST)
          if mqttServerForm.is_valid():
              mqttServer=mqttServerForm.save()
              messages.info(request,f'{mqttServer.device_name} saved Successfully')
        except Exception as e:
            print(e)
            messages.error(request,'An error occurred while saving InputDevice')
        return redirect(registerMqtt)

     elif request.method=='GET':
          mqttServerForm=MqttServerForm()
          return render(request,'iiot/registerMqtt.html',{"mqttServerForm":mqttServerForm})

      

      
def editInputDevice(request,id):
    try:
        inputDevice=InputDevice.objects.get(input_device_id=id)
        # if inputDevice is None:
        #     raise Exception
        if request.method=="POST":
            pass
        else:
            print(id)
        return render(request,'iiot/editInputDevice.html',{})
    except Exception as e:
        messages.error(request,'An error occurred while editing InputDevice')
    redirect(listInputDevices)
