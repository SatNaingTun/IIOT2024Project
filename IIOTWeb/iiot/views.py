from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib import messages
# from .Controllers import PlcAllInOne
from .PlcProtocols import PlcProtocol
from .Controllers import S7PLCLogo
from .forms import PLCAddressForm
# Create your views here.
# plc_data = []

def index(request):
    return HttpResponse("Hello, world. You're at the polls index.")

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
        protocol_name=request.POST.get('PlcProtocol')
        # print(protocol_name)
        result=PlcProtocol.getData(protocol_name,AddressMemory)
        
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
         
def list_view(request):
     if request.method=='POST':
          pass
     elif request.method=='GET':
          return render(request,'iiot/list.html')

