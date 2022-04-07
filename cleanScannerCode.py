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



def Scan(nOfRows,BufferSize,xRange,yIncrement,fft,picoOb,pixelsPerRow,filename):
    for row in range(nOfRows)):
        picoT1 = threading.Thread(target=picoOb.GetVal,args=(BufferSize,row,fft))
        print(f'writing to row {row}')
        picoT1.start()
        if z % 2 == 0:
            motorWrapper.moveX(xRange)
        else:
            motorWrapper.moveX(0)
        picoT1.join()
        if row > 2:
            simpleIP.showImage(filename)
        motorWrapper.moveY((yIncrement*row)+yIncrement)


if __name__ == "__main__":
    tic = time.perf_counter()
    #first, set scanning parameters
    #a dictionary of scanning parameters is absolutely necessary
    picoSamplingPeriod = 256
    picoTimebase = 1e-9
    now = datetime.now()
    parameterDictionary = {
    "coilFrequency" : 900e3,
    "sensorFrequency" : 55e3,
    "coilAmplitude" : 3.3,
    "sensorAmplitude":4,
    "samplingPeriod" :  picoSamplingPeriod,
    "samplingFrequency" : 1/(picoSamplingPeriod * picoTimebase),
    "motorSpeed" : 200,
    "mmMovedX"   : 170,
    "mmMovedY"   : 20,
    "yResolutionMm"   : 0.5,
    "xResolutionMm"   : 0.5,
    "captures"   : 1,
    "gain"       : 1000,
    "PicoResolution" : "PS5000A_DR_16BIT",
    "PicoVoltageRange" : "PS5000A_10V",
    "PicoTimeBase": "PS5000A_NS",
    "filename" : now.strftime("%H%MFFTOutput.csv")

    }
    fGenControl.setFgenParams(parameterDictionary["coilFrequency"],parameterDictionary["coilAmplitude"],
                            parameterDictionary["sensorFrequency"],parameterDictionary["sensorAmplitude"])
    fGenControl.turnFgenOn()
    
    parameterDictionary["xStepRange"
    ],parameterDictionary["bufferSize"
    ],parameterDictionary["samplesPerPixel"
    ],parameterDictionary["yIncrement"
    ], parameterDictionary["nOfRows"] =  scanParams.calculateParameters(parameterDictionary["samplingFrequency"],
                                                                                            parameterDictionary["mmMovedX"],
                                                                                            parameterDictionary["motorSpeed"],
                                                                                            parameterDictionary["mmMovedY"],
                                                                                            parameterDictionary["yResolutionMm"])

    print(parameterDictionary)
    parameterDictionary["pixelsPerRow"] = parameterDictionary['bufferSize']/parameterDictionary['samplesPerPixel']
    print(parameterDictionary)
    fft = FFTLinePixels.FFTLine(parameterDictionary["filename"],
                                parameterDictionary["samplesPerPixel"],
                                parameterDictionary["coilFrequency"],
                                parameterDictionary["sensorFrequency"],
                                parameterDictionary["samplingFrequency"],
                                parameterDictionary["gain"])


    picoOb = pico.StreamData(parameterDictionary["PicoResolution"],
                            parameterDictionary["PicoVoltageRange"],
                            parameterDictionary["samplingPeriod"],
                            parameterDictionary["PicoTimeBase"],
                            parameterDictionary["bufferSize"],
                            parameterDictionary["captures"])
    

    motorWrapper.MotorStartup(parameterDictionary["motorSpeed"])
    print(parameterDictionary)
    Scan(parameterDictionary["nOfRows"],
        parameterDictionary["bufferSize"],
        parameterDictionary["xStepRange"],
        parameterDictionary["yIncrement"],fft,picoOb,parameterDictionary["pixelsPerRow"],parameterDictionary["filename"])
    motorWrapper.moveX(0)
    motorWrapper.moveY(0)
    picoOb.ClosePico()
    fGenControl.turnFgenOff()
    toc = time.perf_counter()
    print(f'Complete scan took {toc - tic:0.4f} seconds')
    #simpleIP.showImage(parameterDictionary["filename"])





            
       
                                
    #new function to input dimension of scan to and completes it, writing data to fft file
    