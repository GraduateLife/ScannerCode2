#imports
import motorWrapper
import fGenControl
import PicoScopewithFFT as pico
import FFTLinePixels as FFTLinePixels
import scanParams
import threading
import time
import json
from datetime import datetime
import simpleIP
#import contour
thread_local = threading.local()





class scannerControl:
    def startMotors(self):
        motorWrapper.MotorStartup(100)
        motorStatus = motorWrapper.checkMotorPower()
        return motorStatus
    def setScanParams(self,parameterDictionary):
    
    #these variables will need to be moved to the gui code
    
        self.parameterDictionary = parameterDictionary
        scanInput = input('details of this scan: ')
        self.parameterDictionary["scanNotes"] = scanInput

        with open(f'./Results/{self.parameterDictionary["filename"]}.json','w') as fp:
            json.dump(self.parameterDictionary,fp)

        print(parameterDictionary)
        fGenControl.setFgenParams(self.parameterDictionary["coilFrequency"],self.parameterDictionary["coilAmplitude"],
                                self.parameterDictionary["sensorFrequency"],self.parameterDictionary["sensorAmplitude"])
        fGenControl.turnFgenOn()
        motorWrapper.setXspeed(parameterDictionary["motorSpeed"])
        
        self.parameterDictionary["xStepRange"
        ],self.parameterDictionary["bufferSize"
        ],self.parameterDictionary["samplesPerPixel"
        ],self.parameterDictionary["yIncrement"
        ], self.parameterDictionary["nOfRows"
        ], self.parameterDictionary["samplingFrequency"] =  scanParams.calculateParameters(self.parameterDictionary)

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



        


    def endScan(self):
        motorWrapper.setXspeed(500)
        motorWrapper.moveX(0)
        motorWrapper.moveY(0)
        self.picoOb.ClosePico()
        fGenControl.turnFgenOff()

    def scanPercentage(self):
        return (self.Row/self.parameterDictionary["nOfRows"])*100

    def scanStatus(self):
        if self.Row <= self.parameterDictionary["nOfRows"]:
            return 0
        else:
            return 1
        
    

    def Scan(self):
        self.Row = 0
        tic = time.perf_counter()
        for row in range(int(self.parameterDictionary["nOfRows"])):
            self.Row == row
            picoT1 = threading.Thread(target=self.picoOb.GetVal,args=(self.parameterDictionary["bufferSize"],row,self.fft))
            print(f'writing to row {row}')
            
            if row % 2 == 0:
                motorWrapper.moveY((self.parameterDictionary["yIncrement"]*row)+self.parameterDictionary["yIncrement"])
                motorWrapper.setXspeed(self.parameterDictionary["motorSpeed"])
                picoT1.start()
                motorWrapper.moveX(self.parameterDictionary["xStepRange"])
            else:
                motorWrapper.setXspeed(1000)
                motorWrapper.moveX(0)
            if row % 2 == 0:
                picoT1.join()
        
            if row > 5:
                simpleIP.showImage(self.parameterDictionary["filename"])
            #if row % 2 == 0:
        toc = time.perf_counter()
        print(f'Complete scan took {toc - tic:0.4f} seconds')







            
       
                                
    #new function to input dimension of scan to and completes it, writing data to fft file
    