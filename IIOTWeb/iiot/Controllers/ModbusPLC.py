from pymodbus.client import ModbusTcpClient
from pymodbus.payload import BinaryPayloadDecoder
from pymodbus.payload import BinaryPayloadBuilder
from pymodbus.constants import Endian
import time
import logging


logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

tcp_host = '192.168.200.2'
tcp_port = 503

coil_address = 1
# value_to_write = True

num_to_read = 1

def write_coil(client, address, value):
    result = client.write_coil(address, value, 1)

    if not result.isError():
        print(f"Successfully wrote value {value} to coil address {address}")
    else:
        print(f"Failed to write value to coil address {address}")

def read_coil(client, address, quantity):
    result = client.read_coils(address, quantity)

    if not result.isError():
        print("Successfully read coils: %s" % result.bits)
    else:
        print(f"Failed to read coils from address {address}")

def read_reg(address,count=1,slave=1):
    # result=client.read_holding_registers(address=address,count=quantity,slave=1)
    # read=client.read_holding_registers(address = 31249 ,count =2,unit=1)
    # read.registers

    # address=address-40001
    result = client.read_holding_registers(address=address, count=count,slave=slave)
    # result = client.read_holding_registers(address=530, count=1,slave=1)
    
    # result = client.read_holding_registers(register,count=2,unit=1).registers
    # decoder = BinaryPayloadDecoder.fromRegisters(result,byteorder= Endian.Big, wordorder=Endian.Little)
    # value = decoder.decode_32bit_float()
    # print(value)
    print(result.registers)
    if not result.isError():
        # print("Successfully read function code: %s" % result.function_code)
        print("Result:",result.registers)
        return result.registers
    else:
        logger.error(f"Error reading register from address {address}")

# client = ModbusTcpClient(host=tcp_host, port=tcp_port)

if __name__=='__main__':
    try:
        # while True:
            client = ModbusTcpClient(host='192.168.200.2',port=504)
            connected=client.connect()
            logger.info(connected)
            if connected:
                # write_coil(client, coil_address, value_to_write)
                # value_to_write = not value_to_write

                # read_coil(client, coil_address, num_to_read)
                read_reg(address=530,count=1,slave=1)

                # client.close()
            else:
                print(f"Failed to connect to Modbus TCP on {tcp_host}")
                client.close()

            time.sleep(1)
    except KeyboardInterrupt:
        print(KeyboardInterrupt)