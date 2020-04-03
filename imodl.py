import serial
import serial.tools.list_ports_windows as port_list
import time

if __name__ == '__main__':
    ser = serial.Serial('COM3', baudrate=115200, timeout=2)
    # ports = list(port_list.comports())
    # for p in ports:
    #     print(p)
    
    # detect mode
    # waiting for 'ff' or 'ad' ?
    ans = ser.read()
    print(ans.hex(' '))
    
    # check communication
    msg = b'\x7e\x13\x7e\x13'
    ser.write(msg)
    ans = ser.read(4)
    print(ans.hex(' '))

    # change to bootloader mode (SBSL)
    msg = b'\x7e\x02\x80\x31\x51\x81\x10\xfa\xf8\x7e\x87'
    ser.write(msg)
    ans = ser.read()
    print(ans.hex(' '))
    time.sleep(.500)

    # connect and do autobaudrate
    msg = b'\x00\x6c'
    ser.write(msg)
    ans = ser.read()
    print(ans.hex(' '))

    # read SBSL status (Flash erase)
    msg = b'\xa0\x10\x00\x00\x27'
    ser.write(msg)
    ans = ser.read(42)
    print(ans.hex(' '))
