import serial
import serial.tools.list_ports_windows as port_list
ser = serial.Serial('COM3', 115200)
ports = list(port_list.comports())
for p in ports:
    print(p)
s = ser.read()
print(s)
