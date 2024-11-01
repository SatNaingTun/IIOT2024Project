from pymodbus.client import ModbusTcpClient
import time
import logging


logging.basicConfig(level=logging.INFO) 
logger = logging.getLogger(__name__)

tcp_host = '192.168.200.2'
tcp_port = 502

coil_address = 10001
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

client = ModbusTcpClient(host=tcp_host, port=tcp_port)

if __name__=='__main__':
    try:
        # while True:
            connected=client.connect()
            logger.info(connected)
            if connected:
                # write_coil(client, coil_address, value_to_write)
                # value_to_write = not value_to_write

                read_coil(client, coil_address, num_to_read)

                client.close()
            else:
                print(f"Failed to connect to Modbus TCP on {tcp_host}")

            time.sleep(1)
    except KeyboardInterrupt:
        pass