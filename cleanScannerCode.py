#imports
import motorWrapper
import PicoScopewithFFT as pico
import FFTLinePixels as FFTLinePixels
import scanParams
import threading
import time
from datetime import datetime
import simpleIP
thread_local = threading.local()



def Scan(nOfRows,BufferSize,xRange,yIncrement,fft,picoOb):
    rowCounter = 0 
    for z in range(int(nOfRows/2)):
        
        picoT1 = threading.Thread(target=picoOb.GetVal,args=(BufferSize,rowCounter,fft))
        print(f'writing to row {rowCounter}')
        #fftT1 = threading.Thread(target=fft.FFTData,args=(rowCounter,))
        rowCounter += 1
        picoT2 = threading.Thread(target=picoOb.GetVal,args=(BufferSize,rowCounter,fft))
        print(f'writing to row {rowCounter}')
        rowCounter += 1
        picoT1.start()
        motorWrapper.moveX(xRange)
        picoT1.join()
        motorWrapper.moveY(((2*yIncrement)*z)+yIncrement)
        picoT2.start()
        #fftT1.start()
        motorWrapper.moveX(0)
        picoT2.join()
        #fftT1.join()
        motorWrapper.moveY(((2*yIncrement)*z)+(2*yIncrement))


if __name__ == "__main__":
    tic = time.perf_counter()
    #first, set scanning parameters
    #a dictionary of scanning parameters is absolutely necessary
    picoSamplingPeriod = 512
    picoTimebase = 1e-9
    now = datetime.now()
    parameterDictionary = {
    "coilFrequency" : 400e3,
    "sensorFrequency" : 33e3,
    "samplingPeriod" :  picoSamplingPeriod,
    "samplingFrequency" : 1/(picoSamplingPeriod * picoTimebase),
    "motorSpeed" : 400,
    "mmMovedX"   : 170,
    "mmMovedY"   : 30,
    "yResolutionMm"   : 1,
    "xResolutionMm"   : 0.5,
    "captures"   : 1,
    "gain"       : 100,
    "PicoResolution" : "PS5000A_DR_16BIT",
    "PicoVoltageRange" : "PS5000A_5V",
    "PicoTimeBase": "PS5000A_NS",
    "filename" : now.strftime("%H%MFFTOutput.csv")

    }
    
    
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
        parameterDictionary["yIncrement"],fft,picoOb)
    motorWrapper.moveX(0)
    motorWrapper.moveY(0)
    picoOb.ClosePico()
    toc = time.perf_counter()
    print(f'Complete scan took {toc - tic:0.4f} seconds')
    simpleIP.showImage(parameterDictionary["mmMovedY"],parameterDictionary["pixelsPerRow"],parameterDictionary["filename"])





            
       
                                
    #new function to input dimension of scan to and completes it, writing data to fft file
    