from .Controllers import S7PLC

from .Controllers import S7PLCLogo
from .Controllers import ModbusPLC

class PlcProtocol:
    def getData(protocol_name,Address,IPAddress,Port,RackOrTsap,SlotOrTsapLogo):
        try:
            if (protocol_name is not None):
                if protocol_name=='S7Rack':
                    if S7PLC.connectConnection(IPAddress,RackOrTsap,SlotOrTsapLogo,Port)==True:
                        return S7PLC.readData(Address)
                    else:
                        return None
                elif protocol_name=='S7Tsap':
                    if S7PLCLogo.connectConnection(IPAddress,RackOrTsap,SlotOrTsapLogo,Port)==True:
                        return S7PLCLogo.readData(Address)
                    else:
                        return None
                elif protocol_name=='Modbus':
                    if ModbusPLC.connectConnection()==True:
                        return ModbusPLC.read_reg(Address)
                    else:
                        return None
        except Exception as e:
            print(e)
            return None


if __name__=='__main__':
    user_choice = input("Enter the PLC protocol to read (e.g., S7Rack or S7Tsap or Modbus) or 'exit' to quit: ")
    if user_choice=='S7Rack':
        S7PLC.askCommand()
    elif user_choice=='S7Tsap':
        S7PLCLogo.askCommand()
    elif user_choice=='Modbus':
        ModbusPLC.askCommand()
