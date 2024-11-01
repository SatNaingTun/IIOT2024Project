import S7PLC
import S7PLCLogo
import ModbusPLC

user_choice = input("Enter the PLC protocol to read (e.g., S7Rack or S7Tsap or Modbus) or 'exit' to quit: ")
if user_choice=='S7Rack':
    S7PLC.askCommand()
elif user_choice=='S7Tsap':
    S7PLCLogo.askCommand()
elif user_choice=='Modbus':
    ModbusPLC.askCommand()