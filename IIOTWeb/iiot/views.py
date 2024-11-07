from django.shortcuts import get_object_or_404, render,redirect
from django.http import HttpResponse
from django.contrib import messages
# from .Controllers import PlcAllInOne
from .PlcProtocols import PlcProtocol
from .Controllers import S7PLCLogo

# from .forms import InputDeviceForm
# from .forms import InputAddressForm
# from .forms import MqttServerForm
# from .models import MqttServers
# from .models import InputDevice
# from .models import InputAddress
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import InputAddressForm,InputDeviceForm,MqttServerForm
from .models import InputDevices, InputAddresses,MqttServers
from .DataCollector import getCollect

# Create your views here.
plc_data = []

def listDevices(request):
    inputDevices=InputDevices.objects.all()
    mqttServers=MqttServers.objects.all()
    context={
         'inputDevices':inputDevices,
         'mqttServers':mqttServers
     }
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request,"iiot/listDevices.html",context)

def listInputAddresses(request):
    inputAddresses=InputAddresses.objects.all()
    context={
         'inputAddresses':inputAddresses
     }
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request,"iiot/listInputAddresses.html",context)


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
        return redirect(listDevices)

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
        return redirect(listDevices)

     elif request.method=='GET':
          mqttServerForm=MqttServerForm()
          return render(request,'iiot/registerMqtt.html',{"mqttServerForm":mqttServerForm})

      

      
def editInputDevice(request,device_id):
    try:
        inputDevice=InputDevices.objects.get(device_id=device_id)
        if inputDevice is None:
            raise Exception
        if request.method=="POST":
            inputDeviceForm=InputDeviceForm(request.POST,instance=inputDevice)
            if inputDeviceForm.is_valid:
                inputDevice=inputDeviceForm.save()
                messages.info(request,f'{inputDevice.device_name} updated Successfully')
            return redirect(listDevices)
        else:
            inputDeviceForm=InputDeviceForm(instance=inputDevice)
            return render(request,'iiot/editInputDevice.html',{"inputDeviceForm":inputDeviceForm})
    except Exception as e:
        messages.error(request,'An error occurred while editing InputDevice')
    return redirect(listDevices)

      
def editMqtt(request,id):
    try:
        mqttServer=MqttServers.objects.get(id=id)
        if mqttServer is None:
            raise Exception
        if request.method=="POST":
            mqttServerForm=MqttServerForm(request.POST,instance=mqttServer)
            if mqttServerForm.is_valid():
                mqttServerForm=mqttServerForm.save()
                messages.info(request,f'{mqttServerForm.device_name} updated Successfully')
            return redirect(listDevices)
        else:
            mqttServerForm=MqttServerForm(instance=mqttServer)
            return render(request,'iiot/registerMqtt.html',{"mqttServerForm":mqttServerForm})
    except Exception as e:
        messages.error(request,'An error occurred while editing Mqtt Server')
    return redirect(listDevices)

      
def removeMqtt(request,id):
    try:
        mqttServer=MqttServers.objects.get(id=id)
        print(id)
        if mqttServer is None:
            raise Exception
        
        mqttServer.delete()
        return redirect(listDevices)
        
    except Exception as e:
        messages.error(request,'An error occurred while removing Mqtt Server')
    return redirect(listDevices)

    
def removeInputAddress(request,address_id):
    try:
        inputAddress=InputAddresses.objects.get(address_id=address_id)
        
        if inputAddress is None:
            raise Exception
        
        inputAddress.delete()
        return redirect(listInputAddresses)
        
    except Exception as e:
        messages.error(request,'An error occurred while removing Mqtt Server')
    return redirect(listInputAddresses)


def removeInputDevice(request,device_id):
    try:
        inputDevice=InputDevices.objects.get(device_id=device_id)
        
        if inputDevice is None:
            raise Exception
        
        inputDevice.delete()
        return redirect(listDevices)
        
    except Exception as e:
        messages.error(request,'An error occurred while removing Mqtt Server')
    return redirect(listDevices)



# def addInputAddress(request,device_id):
#     try:
#         # inputDevice=get_object_or_404(InputDevice, device=device_id)
#         inputDevice=InputDevice.objects.get(device_id=device_id)
#         if inputDevice is None:
#             raise Exception
#         if request.method=="POST":
#             inputAddressForm=InputAddressForm(request.POST,instance=inputDevice)
#             if inputAddressForm.is_valid():
#                 inputAddress=InputAddressForm.save(commit=False)
#                 inputAddress.device=inputDevice
#                 inputAddress.save()
                
#                 # messages.info(request,f'{inputAddress.variable_name} updated Successfully')
#             return redirect(listDevices)
#         else:
#             inputAddressForm=InputAddressForm()
#             return render(request,'iiot/editInputAddress.html',{"inputAddressForm":inputAddressForm})
#     except Exception as e:
#         messages.error(request,'An error occurred while editing Input Address')
#     return redirect(listDevices)



def addInputAddress(request, device_id):
    # Attempt to fetch the input device; return 404 if not found
    inputDevice = InputDevices.objects.get(device_id=device_id)
    
    if request.method == 'POST':
        inputAddressForm = InputAddressForm(request.POST)
        
        if inputAddressForm.is_valid():
            # Create a new InputAddress instance, but don't save it to the database yet
            inputAddress = inputAddressForm.save(commit=False)
            # Assign the device to the InputAddress instance
            if inputDevice is not None:
                inputAddress.device = inputDevice
            # Save the InputAddress to the database
            inputAddress.save()
            
            # Show success message and redirect
            messages.success(request, f'{inputAddress.variable_name} added successfully to {inputDevice.device_name}.')
            return redirect('ListInput')  # Adjust this to the correct view name or path for listing devices
        
        else:
            # If the form is invalid, show an error message
            messages.error(request, 'Failed to save Input Address. Please check the form data.')
    else:
        # If GET request, initialize an empty form
        inputAddressForm = InputAddressForm()

    # Render the form with context
    return render(request, 'iiot/editInputAddress.html', {
        'inputAddressForm': inputAddressForm,
        'inputDevice': inputDevice
    })


def editInputAddress(request, address_id):
    # Attempt to fetch the input device; return 404 if not found
    try:
        inputAddress = get_object_or_404(InputAddresses, address_id=address_id)
    
        if request.method == 'POST':
            inputAddressForm = InputAddressForm(request.POST,instance=inputAddress)
        
            if inputAddressForm.is_valid():
                inputAddress=inputAddressForm.save()
                messages.info(request,f'{inputAddress.address_id} updated Successfully')
                return redirect(listInputAddresses)
        else:
            inputAddressForm = InputAddressForm(instance=inputAddress)
            return render(request,'iiot/editInputAddress.html',{"inputAddressForm":inputAddressForm})
        
    except Exception as e:
        messages.error(request,'An error occurred while editing InputDevice')
        return redirect(listInputAddresses)

      
def testRun(request):
     if request.method=='POST':
          timeSchedule = request.POST.get('TimeSchedule')
          data=getCollect()
          print(data)
          return render(request,'iiot/testrun.html')
     elif request.method=='GET':
          return render(request,'iiot/testrun.html')
