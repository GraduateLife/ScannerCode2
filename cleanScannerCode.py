#imports
# import motorWrapper
# import PicoScopewithFFT as pico
import psuedo






if __name__ == "__main__":
    #first, set scanning parameters
    #a dictionary of scanning parameters is absolutely necessary
    picoSamplingPeriod = 512
    picoTimebase = 1e-9
    parameterDictionary = {
    "coilFrequency" : 400e3,
    "sensorFrequency" : 33e3,
    "samplingPeriod" :  picoSamplingPeriod,
    "samplingFrequency" : 1/(picoSamplingPeriod * picoTimebase),
    "motorSpeed" : 100,
    "mmMovedX"   : 170,
    "mmMovedY"   : 30,
    "captures"   : 1,
    "gain"       : 100

    }
    
    motorWrapper.MotorStartup(parameterDictionary["motorSpeed"])
    
    parameterDictionary["nOfSteps"],parameterDictionary["bufferSize"],parameterDictionary["samplesPerPixel"] =  psuedo.param(parameterDictionary["samplingFrequency"],
                                                        parameterDictionary["mmMovedX"],
                                                        parameterDictionary["motorSpeed"])

    print(parameterDictionary)
    fft = FFTLinePixels.FFTLine(parameterDictionary["samplesPerPixel"],
                                parameterDictionary["coilFrequency"],
                                parameterDictionary["sensorFrequency"],
                                parameterDictionary["samplingFrequency"],
                                parameterDictionary["gain"])
                                
    #new function to input dimension of scan to and completes it, writing data to fft file
    