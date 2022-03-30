from logging import exception
import pico5000 as pico5000
#pico5000.PicoVal('PicoValues.csv',"PS5000A_DR_16BIT",'PS5000A_1V',1,'PS5000A_US',100,1)
import sys
import glob
import serial
import numpy as np
import threading
import concurrent.futures
import time
import FFTLinePixels as FFTLinePixels
import sys
import glob
import serial
import ctypes as  pyC

motordll = pyC.WinDLL("./firstMotorLib.dll")

def serial_ports():
    """ Lists serial port names

        :raises EnvironmentError:
            On unsupported or unknown platforms
        :returns:
            A list of the serial ports available on the system
    """
    if sys.platform.startswith('win'):
        ports = ['COM%s' % (i + 1) for i in range(256)]
    elif sys.platform.startswith('linux') or sys.platform.startswith('cygwin'):
        # this excludes your current terminal "/dev/tty"
        ports = glob.glob('/dev/tty[A-Za-z]*')
    elif sys.platform.startswith('darwin'):
        ports = glob.glob('/dev/tty.*')
    else:
        raise EnvironmentError('Unsupported platform')

    result = []
    for port in ports:
        try:
            s = serial.Serial(port)
            s.close()
            result.append(port)
        except (OSError, serial.SerialException):
            pass
    return result






    
def MotorStartup():

    SerialPortsList = serial_ports()
    print(SerialPortsList)
    print(f"\\\\\\\.\\\{SerialPortsList[0]}")
    #motordll.openSerialPorts(f"\\\\\\\.\\\{SerialPortsList[0]}",f"\\\\\\\.\\\{SerialPortsList[1]}",f"\\\\\\\.\\\{SerialPortsList[2]}")
    firstCom = f"\\\\.\\{SerialPortsList[0]}"
    secondCom = f"\\\\.\\{SerialPortsList[1]}"
    thirdCom =  f"\\\\.\\{SerialPortsList[2]}"

    string1 : pyC.Array[pyC.c_char] = pyC.create_string_buffer(bytes(firstCom,'utf-8'))
    string2 : pyC.Array[pyC.c_char] = pyC.create_string_buffer(bytes(secondCom,'utf-8'))
    string3 : pyC.Array[pyC.c_char] = pyC.create_string_buffer(bytes(thirdCom,'utf-8'))
    
    motordll.openSerialPorts(string1,string2,string3)

    motordll.checkMotorAssignment()
    checkMotors = motordll.motorSetup(500)
    
    if checkMotors != 1:
        return 0
        
    else:
        return 1


if __name__ == '__main__':
    motorCheck = MotorStartup()
    if motorCheck == 0:
        raise Exception ("Motor Failure")
    motordll.XAxismoveToPositionN(0)
    # while(1):
    #     motordll.XAxismoveToPositionN(0)
    #     motordll.XAxismoveToPositionN(19500)
        
   

