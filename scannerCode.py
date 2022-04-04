from logging import exception

import pico5000withMadness as pico5000_fuckaround
#pico5000.PicoVal('PicoValues.csv',"PS5000A_DR_16BIT",'PS5000A_1V',1,'PS5000A_US',100,1)
import sys
import glob
import serial
import numpy as np
import threading
import concurrent.futures
import time
import FFTLinePixelsVariableVersion as FFTLinePixels
import sys
import glob
import serial
import ctypes as  pyC

import psuedo as psuedo

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
    checkMotors = motordll.motorSetup(400)
    
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
    motorCheck = MotorStartup()
    if motorCheck == 0:
        raise Exception ("Motor Failure")
    
    # motordll.XAxismoveToPositionN(39000)
    # motordll.XAxismoveToPositionN(0)
    #motordll.YAxismoveToPositionN(20000)
    #motordll.YAxismoveToPositionN(0)
    mmoved = 170
    nosteps,BufferSize,SamplesPerPixel = psuedo.param(SamplingFrequency,mmoved) 

    Captures = 1
    #captures, blocks of buffers
     # self,OFileName,BitRes,VoltRange,SampInterval,SampIntUnit,BuffSize,Caps
    #test1 = pico5000.StreamData('PicoValues.csv',"PS5000A_DR_16BIT",'PS5000A_5V',SamplingInterval,'PS5000A_NS',BufferSize,Captures)
    motordll.XAxismoveToPositionN(0)
    
   
    SensorFrequency = 30000
    
    Gain = 100

    
    FFTOutFile = 'FFTOutput.csv'
    fft = FFTLinePixels.FFTLine(FFTOutFile,SamplesPerPixel,CoilFrequency,SensorFrequency,SamplingFrequency,Gain)
    test1 = pico5000_fuckaround.StreamData('PicoValues.csv',"PS5000A_DR_16BIT",'PS5000A_5V',SamplingInterval,'PS5000A_NS',BufferSize,Captures)
 
    #t1 = threading.Thread(target=test1.GetVal)
    # #t2 = threading.Thread(target=motordll.XAxismoveToPositionN,args=(40000,))
    # t2 = threading.Thread(target=motordll.XAxismoveToPositionN,args = (35000,))
    
    # t1 = threading.Thread(target=test1.GetVal,args=(BufferSize,))
        # #t2 = threading.Thread(target=test1.GetVal,args=(2323641,))
    # t1.start()
    # motordll.XAxismoveToPositionN(19500)
    # t1.join()

    
    rowCounter = 0
    totalRows = 90
    for z in range(int(totalRows/2)):
        if rowCounter == 0: 
            picoT1 = threading.Thread(target=test1.GetVal,args=(BufferSize,rowCounter,fft))
            print(f'writing to row {rowCounter}')
            #fftT1 = threading.Thread(target=fft.FFTData,args=(rowCounter,))
            print(f'fft of row {rowCounter}')
            rowCounter += 1
            picoT2 = threading.Thread(target=test1.GetVal,args=(BufferSize,rowCounter,fft))
            print(f'writing to row {rowCounter}')
            rowCounter += 1
            picoT1.start()
            motordll.XAxismoveToPositionN(nosteps)
            picoT1.join()
            motordll.YAxismoveToPositionN((400*z)+200)
            picoT2.start()
            #fftT1.start()
            motordll.XAxismoveToPositionN(0)
            picoT2.join()
            #fftT1.join()
            motordll.YAxismoveToPositionN((400*z)+400)
            
        else:
            picoT1 = threading.Thread(target=test1.GetVal,args=(BufferSize,rowCounter,fft))
            print(f'writing to row {rowCounter}')
            #fftT1 = threading.Thread(target=fft.FFTData,args=((rowCounter-1),))
            print(f'fft of row {rowCounter -1}')

            rowCounter += 1
            picoT2 = threading.Thread(target=test1.GetVal,args=(BufferSize,rowCounter,fft))
            print(f'writing to row {rowCounter}')
            fftT2 = threading.Thread(target=fft.FFTData,args=((rowCounter -1),))
            print(f'fft of row {rowCounter -1}')
            rowCounter += 1
            picoT1.start()
            #fftT1.start()
            motordll.XAxismoveToPositionN(nosteps)
            picoT1.join()
            #fftT1.join()
    
            motordll.YAxismoveToPositionN((400*z)+200)
            picoT2.start()
            #fftT2.start()
            motordll.XAxismoveToPositionN(0)
            picoT2.join()
            #fftT2.join()
            motordll.YAxismoveToPositionN((400*z)+400)
            


        


    
    # # t1.start()
    # # t2.start()
    # # t2.join()
    # # t1.join()
    test1.ClosePico()
    
    
    motordll.YAxismoveToPositionN(0)
    motordll.XAxismoveToPositionN(0)
    motordll.closeSerialPorts()
  




    
    










# test1 = pico5000.Pico5000('PicoValues.csv',"PS5000A_DR_16BIT",'PS5000A_1V',1,'PS5000A_US',10000,10)
# test1.GetVal()
# test1.GetVal()

