# view.py
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponse
from django.contrib import messages
# from .Controllers import PlcAllInOne
from .PlcProtocols import PlcProtocol
from .Controllers import S7PLCLogo, InfluxDb

from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .forms import CreateMeasurementForm, InfluxDBForm, InputAddressForm, InputDeviceForm, MqttServerForm, InfluxServerForm, InfluxMeasurementForm, PiInfoForm, PiWifiForm
from .models import InputDevices, InputAddresses, MqttServers, InfluxDatabases, InfluxMeasurement
from .DataCollector import getCollect
from .filters import InputAddressFilter, InfluxMeasurementFilter
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required

try:
    from .Controllers import PiProfile
except Exception as e:
    print("PiProfile import error", e)
# from  .Views import InputDeviceView


# Create your views here.
plc_data = []

def login_view(request):
    if request.method=='POST':
        login_form=AuthenticationForm(request=request,data=request.POST)
        if login_form.is_valid():
            username=login_form.cleaned_data.get('username')
            password=login_form.cleaned_data.get('password')
            user=authenticate(username=username,password=password)
            if user is not None:
                login(request,user)
                return redirect(listDevices)
            else:
                pass
    elif request.method=='GET':
        login_form=AuthenticationForm()
    return render(request,'iiot/login.html',{'myform':login_form})

@login_required
def logout_view(request):
    logout(request)
    return redirect(listDevices)
                

@login_required
def listDevices(request):
    inputDevices = InputDevices.objects.all()
    mqttServers = MqttServers.objects.all()
    influxDatabases = InfluxDatabases.objects.all()

    context = {
        'inputDevices': inputDevices,
        'mqttServers': mqttServers,
        'influxDatabases': influxDatabases
    }
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, "iiot/listDevices.html", context)

@login_required
def listInputAddresses(request):
    inputAddresses = InputAddresses.objects.all()
    inputAddressFilter = InputAddressFilter(
        request.GET, queryset=inputAddresses)
    context = {
        # 'inputAddresses': inputAddresses,
        'inputAddressFilter': inputAddressFilter
    }
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, "iiot/listInputAddresses.html", context)

@login_required
def listMeasurements(request):
    influxMeasurements = InfluxMeasurement.objects.all()
    influxMeasurementFilter = InfluxMeasurementFilter(
        request.GET, queryset=influxMeasurements)
    context = {
        # 'influxMeasurements': influxMeasurements,
        'influxMeasurementFilter': influxMeasurementFilter
    }
    # return HttpResponse("Hello, world. You're at the polls index.")
    return render(request, "iiot/listInfluxMeasurement.html", context)

@login_required
def test(request):
    plc_data = []
    if request.method == 'GET':
        return render(request, "iiot/test.html")
    elif request.method == 'POST':
        # form = PLCAddressForm(request.POST)
        var_name = request.POST.get('variable_name')
        # print(var_name)
        AddressMemory = request.POST.get('AddressMemory')
        # print(AddressMemory)
        ip = request.POST.get('IPAddressPLC')
        port = request.POST.get('PlcPort')
        protocol_name = request.POST.get('PlcProtocol')
        rack = request.POST.get('Rack')
        slot = request.POST.get('Slot')
        print(protocol_name)
        result = PlcProtocol.getData(
            protocol_name, AddressMemory, ip, int(port), rack, slot)

        if result is not None:
            plc_data.append({'address': AddressMemory,
                            'data': result, 'variable_name': var_name})
        else:
            messages.error(request, "Check Your Connection")
        return render(request, "iiot/test.html", {'plc_data': plc_data})

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
    plc_data = []

    if request.method == 'GET':
        return render(request, "iiot/test.html")
    elif request.method == 'POST':
        # PlcAllInOne.getData(protocol_name)
        var_name = request.POST.get('variable_name')
        # print(var_name)
        AddressMemory = request.POST.get('AddressMemory')

        protocol_name = request.POST.get('PlcProtocol')
        # print(protocol_name)
        plc_data.append({'address': AddressMemory, 'data': 5,
                        'variable_name': var_name})
        # print(plc_data)
        # print(plc_data.get('variable_name'))
        return render(request, "iiot/test.html", {'plc_data': plc_data})

@login_required
def registerInputDevice(request):

    if request.method == 'POST':
        try:
            inputDeviceForm = InputDeviceForm(request.POST)
            if inputDeviceForm.is_valid():
                inputDevice = inputDeviceForm.save()
                messages.info(
                    request, f'{inputDevice.device_name} saved Successfully')
        except Exception as e:
            print(e)
            messages.error(
                request, 'An error occurred while saving InputDevice')
        return redirect(listDevices)

    elif request.method == 'GET':
        inputDeviceForm = InputDeviceForm()
        return render(request, 'iiot/registerInputDevice.html', {"inputDeviceForm": inputDeviceForm})

@login_required
def registerMqtt(request):

    if request.method == 'POST':
        try:
            mqttServerForm = MqttServerForm(request.POST)
            if mqttServerForm.is_valid():
                mqttServer = mqttServerForm.save()
                messages.info(
                    request, f'{mqttServer.device_name} saved Successfully')
        except Exception as e:
            print(e)
            messages.error(
                request, 'An error occurred while saving InputDevice')
        return redirect(listDevices)

    elif request.method == 'GET':
        mqttServerForm = MqttServerForm()
        return render(request, 'iiot/registerMqtt.html', {"mqttServerForm": mqttServerForm})

@login_required
def editInputDevice(request, device_id):
    try:
        inputDevice = InputDevices.objects.get(device_id=device_id)
        if inputDevice is None:
            raise Exception
        if request.method == "POST":
            inputDeviceForm = InputDeviceForm(
                request.POST, instance=inputDevice)
            if inputDeviceForm.is_valid:
                inputDevice = inputDeviceForm.save()
                messages.info(
                    request, f'{inputDevice.device_name} updated Successfully')
            return redirect(listDevices)
        else:
            inputDeviceForm = InputDeviceForm(instance=inputDevice)
            return render(request, 'iiot/editInputDevice.html', {"inputDeviceForm": inputDeviceForm})
    except Exception as e:
        messages.error(request, 'An error occurred while editing InputDevice')
    return redirect(listDevices)

@login_required
def editMeasurement(request, id):
    try:
        influxMeasurement = InfluxMeasurement.objects.get(id=id)
        if influxMeasurement is None:
            raise Exception
        if request.method == "POST":
            influxMeasurementForm = InfluxMeasurementForm(
                request.POST, instance=influxMeasurement)
            if influxMeasurementForm.is_valid:
                influxMeasurement = influxMeasurementForm.save()
                messages.info(
                    request, f'{influxMeasurement.measurement_name} updated Successfully')
            return redirect(listDevices)
        else:
            influxMeasurementForm = InfluxMeasurementForm(
                instance=influxMeasurement)
            return render(request, 'iiot/form.html', {"myform": influxMeasurementForm})
    except Exception as e:
        messages.error(request, 'An error occurred while editing InputDevice')
    return redirect(listDevices)

@login_required
def editMqtt(request, id):
    try:
        mqttServer = MqttServers.objects.get(id=id)
        if mqttServer is None:
            raise Exception
        if request.method == "POST":
            mqttServerForm = MqttServerForm(request.POST, instance=mqttServer)
            if mqttServerForm.is_valid():
                mqttServerForm = mqttServerForm.save()
                messages.info(
                    request, f'{mqttServerForm.device_name} updated Successfully')
            return redirect(listDevices)
        else:
            mqttServerForm = MqttServerForm(instance=mqttServer)
            return render(request, 'iiot/registerMqtt.html', {"mqttServerForm": mqttServerForm})
    except Exception as e:
        messages.error(request, 'An error occurred while editing Mqtt Server')
    return redirect(listDevices)

@login_required
def removeMqtt(request, id):
    try:
        mqttServer = MqttServers.objects.get(id=id)
        print(id)
        if mqttServer is None:
            raise Exception

        mqttServer.delete()
        return redirect(listDevices)

    except Exception as e:
        messages.error(request, 'An error occurred while removing Mqtt Server')
    return redirect(listDevices)

@login_required
def removeMeasurement(request, id):
    try:
        influxMeasurement = InfluxMeasurement.objects.get(id=id)
        print(id)
        if influxMeasurement is None:
            raise Exception

        influxMeasurement.delete()
        return redirect(listMeasurements)

    except Exception as e:
        messages.error(request, 'An error occurred while removing Mqtt Server')
    return redirect(listMeasurements)

@login_required
def removeInputAddress(request, address_id):
    try:
        inputAddress = InputAddresses.objects.get(address_id=address_id)

        if inputAddress is None:
            raise Exception

        inputAddress.delete()
        return redirect(listInputAddresses)

    except Exception as e:
        messages.error(request, 'An error occurred while removing Mqtt Server')
    return redirect(listInputAddresses)

@login_required
def removeInputDevice(request, device_id):
    try:
        inputDevice = InputDevices.objects.get(device_id=device_id)

        if inputDevice is None:
            raise Exception

        inputDevice.delete()
        return redirect(listDevices)

    except Exception as e:
        messages.error(request, 'An error occurred while removing Mqtt Server')
    return redirect(listDevices)

@login_required
def removeInfluxDB(request, device_id):
    try:
        influxServer = InfluxDatabases.objects.get(device_id=device_id)

        if influxServer is None:
            raise Exception

        influxServer.delete()
        return redirect(listDevices)

    except Exception as e:
        messages.error(request, 'An error occurred while removing Mqtt Server')
    return redirect(listDevices)

@login_required
def addInputAddress(request):
    # Attempt to fetch the input device; return 404 if not found
    # inputDevice = InputDevices.objects.get(device_id=device_id)

    if request.method == 'POST':
        inputAddressForm = InputAddressForm(request.POST)

        if inputAddressForm.is_valid():
            # Create a new InputAddress instance, but don't save it to the database yet
            inputAddress = inputAddressForm.save(commit=False)
            # Assign the device to the InputAddress instance
            # if inputDevice is not None:
            #     inputAddress.device = inputDevice
            # Save the InputAddress to the database
            inputAddress.save()

            # Show success message and redirect
            messages.success(request, f'{inputAddress.variable_name} added successfully to {
                             inputAddress.device.device_name}.')
            # Adjust this to the correct view name or path for listing devices
            return redirect('ListInputAddress')

        else:
            # If the form is invalid, show an error message
            messages.error(
                request, 'Failed to save Input Address. Please check the form data.')
    else:
        # If GET request, initialize an empty form
        inputAddressForm = InputAddressForm()

    # Render the form with context
    return render(request, 'iiot/editInputAddress.html', {
        'inputAddressForm': inputAddressForm,
        # 'inputDevice': inputDevice
    })

@login_required
def addInfluxMeasurement(request):
    # Attempt to fetch the input device; return 404 if not found
    # influxDatabase = InfluxDatabases.objects.get(device_id=device_id)

    if request.method == 'POST':
        influxMeasurementForm = InfluxMeasurementForm(request.POST)

        if influxMeasurementForm.is_valid():

            database = influxMeasurementForm.cleaned_data['database']
            # if InfluxDb.connectConnection(database.device_name,database.port)
            influxMeasurement = influxMeasurementForm.save()

            messages.success(request, f'{influxMeasurement.measurement_name} added successfully to {
                             influxMeasurement.database}.')
            # Adjust this to the correct view name or path for listing devices
            return redirect(listDevices)

        else:
            # If the form is invalid, show an error message
            messages.error(
                request, 'Failed to save Measurement. Please check the form data.')
    else:
        # If GET request, initialize an empty form
        influxMeasurementForm = InfluxMeasurementForm()

    # Render the form with context
    return render(request, 'iiot/form.html', {
        'myform': influxMeasurementForm

    })

@login_required
def addInfluxDB(request):
    # Attempt to fetch the input device; return 404 if not found
    # inputDevice = InputDevices.objects.get(device_id=device_id)

    if request.method == 'POST':
        influxServerForm = InfluxServerForm(request.POST)

        if influxServerForm.is_valid():
            # Create a new InputAddress instance, but don't save it to the database yet
            influxServer = influxServerForm.save()
            try:

                

                InfluxDb.connectConnection(
                    influxServer.ip_address, influxServer.port)
                InfluxDb.create_database(influxServer.database)

                db_name = influxServerForm.cleaned_data['database']
                duration = influxServerForm.cleaned_data['duration']
                databases = InfluxDb.list_databases()
                if duration is not None and duration != "" and databases is not None:
                    InfluxDb.createRetentionPolicy(
                        db_name=db_name, duration=duration)

            # Show success message and redirect
                messages.success(request, f' {influxServer.device_name} save successfully to {
                    influxServer.device_name}.')

                return redirect(listDevices)
            except:
                messages.error(
                    request, 'Failed to create Influxdb name. Please check the connection to Influx')
                influxServer.delete()
                return redirect(listDevices)
    else:
        # If GET request, initialize an empty form
        influxServerForm = InfluxServerForm()

    # Render the form with context
        return render(request, 'iiot/form.html', {
            'myform': influxServerForm,
            # 'inputDevice': inputDevice
        })

@login_required
def editInfluxDB(request, device_id):
    # Attempt to fetch the input device; return 404 if not found
    influxServer = InfluxDatabases.objects.get(device_id=device_id)

    if request.method == 'POST':
        influxServerForm = InfluxServerForm(
            request.POST, instance=influxServer)

        if influxServerForm.is_valid():
            try:
                influxServer = influxServerForm.save()
                influxDb = InfluxDb.connectConnection(
                    influxServer.ip_address, influxServer.port)
                InfluxDb.create_database(influxServer.database)

                db_name = influxServerForm.cleaned_data['database']
                duration = influxServerForm.cleaned_data['duration']
                databases = InfluxDb.list_databases()
                if duration is not None and duration != "" and databases is not None:
                    InfluxDb.createRetentionPolicy(
                        db_name=db_name, duration=duration)

                messages.success(request, f' {influxServer.device_name} updated successfully to {
                    influxServer.device_name}.')
            # Adjust this to the correct view name or path for listing devices
                return redirect(listDevices)
            except:
                messages.error(request, 'Failed to update Influx Database')

        else:
            # If the form is invalid, show an error message
            messages.error(
                request, 'Failed to update Influx Database. Please check the form data.')
    else:
        # If GET request, initialize an empty form
        influxServerForm = InfluxServerForm(instance=influxServer)

    # Render the form with context
    return render(request, 'iiot/form.html', {
        'myform': influxServerForm,
        # 'inputDevice': inputDevice
    })

@login_required
def editInputAddress(request, address_id):
    # Attempt to fetch the input device; return 404 if not found
    try:
        inputAddress = get_object_or_404(InputAddresses, address_id=address_id)

        if request.method == 'POST':
            inputAddressForm = InputAddressForm(
                request.POST, instance=inputAddress)

            if inputAddressForm.is_valid():
                inputAddress = inputAddressForm.save()
                messages.info(
                    request, f'{inputAddress.address_id} updated Successfully')
                return redirect(listInputAddresses)
        else:
            inputAddressForm = InputAddressForm(instance=inputAddress)
            return render(request, 'iiot/editInputAddress.html', {"inputAddressForm": inputAddressForm})

    except Exception as e:
        messages.error(request, 'An error occurred while editing InputDevice')
        return redirect(listInputAddresses)

@login_required
def pi_profile_view(request):
    networks = PiProfile.get_unique_networks()
    wifiNames = PiProfile.get_ssid_list(networks)
    # wifiNames=PiProfile.get_ssid_list(networks)

    print(wifiNames)

    initial_data = {
        'pi_name': PiProfile.get_hostname(),
        'pi_ip_address': PiProfile.get_ip_address(),


    }
    form = PiInfoForm(initial=initial_data)
    # form=PiInfoForm()
    if request.method == 'POST':
        form = PiInfoForm(request.POST)
        if form.is_valid():
            # hostname=request.POST.get('pi_name')
            # wifi_name=request.POST.get('wifi_name')
            # wifi_password=request.POST.get('wifi_password')
            hostname = form.cleaned_data['pi_name']

            PiProfile.set_hostname(hostname)

            form = PiInfoForm(initial=initial_data)

    return render(request, 'iiot/form.html', {'myform': form})

@login_required
def pi_wifi_view(request):
    networks = PiProfile.get_unique_networks()
    wifiNames = PiProfile.get_ssid_list(networks)

    if request.method == 'POST':
        form = PiWifiForm(request.POST, wifiNames=wifiNames)
        if form.is_valid():
            wifi_name = form.cleaned_data['wifi_name']
            wifi_password = form.cleaned_data['wifi_password']
            PiProfile.connect_to_wifi(wifi_name, wifi_password)
            messages.success(request, "Connected to Wi-Fi successfully")
            return redirect('pi_wifi_view')  # Replace with actual success view
        else:
            messages.error(request, "Failed to connect to Wi-Fi")
    else:
        form = PiWifiForm(wifiNames=wifiNames)

    return render(request, 'iiot/form.html', {'myform': form})

@login_required
def influx_database_view(request):
    """View to handle database creation, deletion, and listing."""
    form = InfluxDBForm()  # Instantiate the form
    InfluxDb.connectConnection()
    if request.method == 'POST':
        if 'create' in request.POST:
            form = InfluxDBForm(request.POST)
            if form.is_valid():
                db_name = form.cleaned_data['db_name']
                InfluxDb.create_database(db_name)
                messages.info(request, f"Influx database {db_name} is created")
                # Redirect to PLC view after creating database
                return redirect(listDevices)
        elif 'delete' in request.POST:
            db_name = request.POST.get('database_name')
            if db_name:
                InfluxDb.delete_database(db_name)
                messages.info(request, f"Influx database {db_name} is deleted")
                # Redirect to PLC view after deleting database
                return redirect(listDevices)

    databases = InfluxDb.list_databases()  # List all databases
    return render(request, 'iiot/influx_database.html', {'form': form, 'databases': databases})

@login_required
def create_measurement_view(request):
    # Fetch the list of databases created from InfluxDB
    InfluxDb.connectConnection()
    databases = InfluxDb.list_databases()

    if request.method == 'POST':
        # Pass databases to the form
        form = CreateMeasurementForm(request.POST, databases=databases)
        if form.is_valid():
            database_name = form.cleaned_data['database_name']
            measurement_name = form.cleaned_data['measurement_name']
            field_name = form.cleaned_data['field_name'] or "value"
            field_value = form.cleaned_data['field_value'] or 1

            try:
                # Assuming create_measurement interacts with InfluxDB
                InfluxDb.create_measurement(
                    database_name, measurement_name, field_name, field_value)
                messages.success(request, f"Measurement '{measurement_name}' created in '{
                                 database_name}' with field '{field_name}'={field_value}")
            except Exception as e:
                messages.error(
                    request, f"Error creating measurement: {str(e)}")
            # Redirect to the same page after creation
            return redirect('RegInfluxMeasurement')
    else:
        # Pass databases to the form when rendering
        form = CreateMeasurementForm(databases=databases)

    # Render the form template
    return render(request, 'iiot/influx_measurement.html', {'form': form, 'databases': databases})


def testRun(request):
    if request.method == 'POST':
        timeSchedule = request.POST.get('TimeSchedule')
        data = getCollect()
        print(data)
        return render(request, 'iiot/testrun.html')
    elif request.method == 'GET':
        return render(request, 'iiot/testrun.html')
