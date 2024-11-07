import S7PLC
import S7PLCLogo
import ModbusPLC

class PlcProtocol:
    def getData(protocol_name,Address,IPAddress,Port,RackOrTsap,SlotOrTsapLogo):
        try:
            if (protocol_name is not None):
                if protocol_name=='S7Rack':
                    if S7PLC.connectConnection(IPAddress,int(RackOrTsap),int(SlotOrTsapLogo),Port)==True:
                        return S7PLC.readData(Address)
                    else:
                        return None
                elif protocol_name=='S7Tsap':
                    changedTsap=int(RackOrTsap, 16)
                    changedTsapLogo=int(SlotOrTsapLogo, 16)
                    if S7PLCLogo.connectConnection(IPAddress,changedTsap,changedTsapLogo,Port)==True:
                        return S7PLCLogo.readData(Address)
                    else:
                        return None
                elif protocol_name=='Modbus':
                    if ModbusPLC.connectConnection(IPAddress,Port)==True:
                        return ModbusPLC.read_reg(int(Address))
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