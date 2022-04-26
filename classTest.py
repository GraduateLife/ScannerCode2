from datetime import datetime
import cleanScannerCode
import motorWrapper
import time


now = datetime.now()





parameterDictionary = {
    "coilFrequency" : 900e3,
    "sensorFrequency" : 55e3,
    "coilAmplitude" :3.8,
    "sensorAmplitude":4,
    "samplingPeriod" :  64,
    "picoTimebase" : 1e-9,
    "motorSpeed" : 200,
    "mmMovedX"   : 70,
    "mmMovedY"   : 80,
    "yResolutionMm"   : 0.5,
    "xResolutionMm"   : 0.1,
    "captures"   : 1,
    "gain"       : 1000,
    "PicoResolution" : "PS5000A_DR_16BIT",
    "PicoVoltageRange" : "PS5000A_5V",
    "PicoTimeBase": "PS5000A_NS",
    "filename" : now.strftime("%d%mFFTOutput%H%M")
}


print(parameterDictionary["filename"])
try:
    
    scanner = cleanScannerCode.scannerControl()
    scanner.startMotors()
    scanner.setScanParams(parameterDictionary)
    #time.sleep(120)
    scanner.Scan()
    scanner.endScan()
        
except KeyboardInterrupt:
    scanner.endScan()
    print ("Shutdown requested...exiting")




