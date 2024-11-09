from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
import time
import logging


logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

# tcp_host = '192.168.200.2'
# tcp_port = 503

coil_address = 1
# value_to_write = True

num_to_read = 1


def connectConnection(host='192.168.200.2',port=102):
    global client
    client = ModbusTcpClient(host=host,port=port)
    connected=client.connect()
    return connected

def write_coil(address, value):
    result = client.write_coil(address, value, 1)

    if not result.isError():
        print(f"Successfully wrote value {value} to coil address {address}")
    else:
        print(f"Failed to write value to coil address {address}")

def read_coil(address, count=1,slave=1):
    result = client.read_coils(address, count)

    if not result.isError():
        print("Successfully read coils: %s" % result.bits)
        return result.registers[0]
    else:
        print(f"Failed to read coils from address {address}")

def read_reg(address,count=1,slave=1):
    result = client.read_holding_registers(address=address, count=count,slave=slave)
    print(result.registers)
    if not result.isError():
        print("Result:",result.registers[0])
        return result.registers[0]
    else:
        logger.error(f"Error reading register from address {address}")
        return None
    
def readData(address,count=1,slave=1):
    print(f"Reading Data from address {address}")
    if(0<address<10000):
        address=address
        result=client.read_coils(address, count)
    elif(10000<address<20000):
        address=address-10000
        result=client.read_discrete_inputs(address=address, count=count,slave=slave)
    elif(30000<address<40000):
        address=address-30000
        result=client.read_input_registers(address=address, count=count,slave=slave)
    elif(40000<address<50000):
        address=address-40000
        result=client.read_holding_registers(address=address, count=count,slave=slave)
    
    if not result.isError():
        # if count==1:
            print("Result:",result.registers[0])
            client.close()
            return result.registers[0]
        # else:
        #     print("Result:",result.registers)
        #     client.close()
        #     return result.registers
    else:
        logger.error(f"Error reading register from address {address}")
        return None
    
                 

# client = ModbusTcpClient(host=tcp_host, port=tcp_port)

if __name__=='__main__':
    try:
        # while True:
            # client = ModbusTcpClient(host='192.168.200.2',port=504)
            # connected=client.connect()
            connected=connectConnection(host='192.168.200.2',port=504)
            logger.info("Conntected:"+str(connected))
            if connected:
                
                # read_reg(address=530,count=1,slave=1)
                readData(address=40530,count=1,slave=1)

                client.close()
            else:
                print(f"Failed to connect to Modbus TCP on ")
                client.close()

            time.sleep(1)
    except KeyboardInterrupt:
        print(KeyboardInterrupt)