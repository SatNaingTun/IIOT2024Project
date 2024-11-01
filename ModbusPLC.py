from pymodbus.client import ModbusTcpClient # type: ignore

# def connectConnection(address='192.168.200.250')
client=ModbusTcpClient('192.168.200.250')
client.connect()                           # connect to device
# client.write_coil(1, True, slave=1)        # set information in device
result = client.read_coils(530, 3, slave=1)  # get information from device
print(result.bits[0])                      # use information
client.close()                             # Disconnect device

