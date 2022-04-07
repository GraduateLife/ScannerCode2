#imports C functions into python functions, in order to neated up the code
#hopefully there will be no issues with speed.

#just need function to do setup and motor parameter and then functions to move x and y
from logging import exception
import ctypes as  pyC
import serial
import sys
import glob

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




def MotorStartup(speed):

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
    checkMotors = motordll.motorSetup(speed)
    
    if checkMotors != 1:
        raise Exception ("Motor Failure")
        

        


def moveX(stepsToMove):
    motordll.XAxismoveToPositionN(int(stepsToMove))

def moveY(stepsToMove):
    motordll.YAxismoveToPositionN(int(stepsToMove))


def checkMotorPower():
    motordll.checkMotorPower()