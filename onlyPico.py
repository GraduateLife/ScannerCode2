from logging import exception

import pico5000withC as pico5000_fuckaround
#pico5000.PicoVal('PicoValues.csv',"PS5000A_DR_16BIT",'PS5000A_1V',1,'PS5000A_US',100,1)
import sys
import glob
import serial
import numpy as np
import threading
import concurrent.futures
import time
import FFTLinePixelsRows as FFTLinePixels
import sys
import glob
import serial
import ctypes as  pyC

motordll = pyC.WinDLL("./firstMotorLib.dll")
thread_local = threading.local()

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
    checkMotors = motordll.motorSetup(100)
    
    if checkMotors != 1:
        return 0
        
    else:
        return 1



    




if __name__ == '__main__':
    PicoTimeBase = ['PS5000A_NS','PS5000A_NS','PS5000A_NS','PS5000A_NS','PS5000A_NS']
    #Key Scanning Parameters
    CoilFrequency = 400e3
    #SamplingInterval = (1/SamplingFrequency)*1e9 #why 1e9
    SamplingInterval = 512
    SamplingFrequency = 1/(SamplingInterval*1e-9)
    print(f'sampling every {SamplingInterval} ns')



    #motorSpeed = 600
    
    
    # motordll.XAxismoveToPositionN(39000)
    # motordll.XAxismoveToPositionN(0)
    #motordll.YAxismoveToPositionN(20000)
    #motordll.YAxismoveToPositionN(0)
    
    
    BufferSize = 10000
    Captures = 1
    #captures, blocks of buffers
     # self,OFileName,BitRes,VoltRange,SampInterval,SampIntUnit,BuffSize,Caps
    #test1 = pico5000.StreamData('PicoValues.csv',"PS5000A_DR_16BIT",'PS5000A_5V',SamplingInterval,'PS5000A_NS',BufferSize,Captures)
    test1 = pico5000_fuckaround.StreamData('PicoValues.csv',"PS5000A_DR_16BIT",'PS5000A_5V',SamplingInterval,'PS5000A_NS',BufferSize,Captures)
 
    #t1 = threading.Thread(target=test1.GetVal)
    # #t2 = threading.Thread(target=motordll.XAxismoveToPositionN,args=(40000,))
    # t2 = threading.Thread(target=motordll.XAxismoveToPositionN,args = (35000,))
    
    callCounter = 0
    # for z in range(1):
    #       t1 = threading.Thread(target=test1.GetVal,args=(BufferSize,))
    #       callCounter += 1
    # #      callCounter += 1
    #       t1.start()
    # #      motordll.XAxismoveToPositionN(19500)
    #       t1.join()

    


    callCounter = 0
    for z in range(10):
          t1 = threading.Thread(target=test1.GetVal,args=(BufferSize,callCounter,))
          callCounter += 1
    #      callCounter += 1
          t1.start()
    #      motordll.XAxismoveToPositionN(19500)
          t1.join()
          #motordll.YAxismoveToPositionN((400*z)+200)
         
          #motordll.XAxismoveToPositionN(0)
          
    #      motordll.YAxismoveToPositionN((400*z)+400)
    #motordll.XAxismoveToPositionN(0)
    SamplesPerPixel = 25600
   
    SensorFrequency = 30000
    
    Gain = 100

    VoltageFile = 'Ctesting.csv'
    FFTOutFile = 'IndexInvertNew.csv'


    fft = FFTLinePixels.FFTLine(VoltageFile,FFTOutFile,SamplesPerPixel,CoilFrequency,SensorFrequency,SamplingFrequency,Gain)
    fft.FFTData()
    # # # t1.start()
    # # # t2.start()
    # # # t2.join()
    # # # t1.join()
    test1.ClosePico()
    
    
    