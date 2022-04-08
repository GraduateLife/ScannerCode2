#imports
import motorWrapper
import fGenControl
import PicoScopewithFFT as pico
import FFTLinePixels as FFTLinePixels
import scanParams
import threading
import time
from datetime import datetime
import simpleIP
thread_local = threading.local()





class scannerControl:
    def __init__(self,parameterDictionary):
    
    #these variables will need to be moved to the gui code
    
    
        self.parameterDictionary = parameterDictionary
        fGenControl.setFgenParams(self.parameterDictionary["coilFrequency"],self.parameterDictionary["coilAmplitude"],
                                self.parameterDictionary["sensorFrequency"],self.parameterDictionary["sensorAmplitude"])
        fGenControl.turnFgenOn()
        
        self.parameterDictionary["xStepRange"
        ],self.parameterDictionary["bufferSize"
        ],self.parameterDictionary["samplesPerPixel"
        ],self.parameterDictionary["yIncrement"
        ], self.parameterDictionary["nOfRows"] =  scanParams.calculateParameters(self.parameterDictionary["samplingFrequency"],
                                                                                                self.parameterDictionary["mmMovedX"],
                                                                                                self.parameterDictionary["motorSpeed"],
                                                                                                self.parameterDictionary["mmMovedY"],
                                                                                                self.parameterDictionary["yResolutionMm"])

        print(self.parameterDictionary)
        self.parameterDictionary["pixelsPerRow"] = self.parameterDictionary['bufferSize']/self.parameterDictionary['samplesPerPixel']
        print(self.parameterDictionary)
        self.fft = FFTLinePixels.FFTLine(self.parameterDictionary["filename"],
                                    self.parameterDictionary["samplesPerPixel"],
                                    self.parameterDictionary["coilFrequency"],
                                    self.parameterDictionary["sensorFrequency"],
                                    self.parameterDictionary["samplingFrequency"],
                                    self.parameterDictionary["gain"])


        self.picoOb = pico.StreamData(self.parameterDictionary["PicoResolution"],
                                self.parameterDictionary["PicoVoltageRange"],
                                self.parameterDictionary["samplingPeriod"],
                                self.parameterDictionary["PicoTimeBase"],
                                self.parameterDictionary["bufferSize"],
                                self.parameterDictionary["captures"])
    




    
    #simpleIP.showImage(parameterDictionary["filename"])


    def MotorStartup(self):
        motorWrapper.MotorStartup(100)
        motorWrapper.checkMotorPower()


    def endScan(self):
        motorWrapper.moveX(0)
        motorWrapper.moveY(0)
        self.picoOb.ClosePico()
        fGenControl.turnFgenOff()

    def Scan(self):
        motorWrapper.MotorStartup(self.parameterDictionary["motorSpeed"])
        tic = time.perf_counter()
        for row in range(int(self.parameterDictionary["nOfRows"])):
            picoT1 = threading.Thread(target=self.picoOb.GetVal,args=(self.parameterDictionary["bufferSize"],row,self.fft))
            print(f'writing to row {row}')
            picoT1.start()
            if row % 2 == 0:
                motorWrapper.moveX(self.parameterDictionary["xStepRange"])
            else:
                motorWrapper.moveX(0)
            picoT1.join()
            if row > 2:
                simpleIP.showImage(self.parameterDictionary["filename"])
            motorWrapper.moveY((self.parameterDictionary["yIncrement"]*row)+self.parameterDictionary["yIncrement"])
        toc = time.perf_counter()
        print(f'Complete scan took {toc - tic:0.4f} seconds')







            
       
                                
    #new function to input dimension of scan to and completes it, writing data to fft file
    