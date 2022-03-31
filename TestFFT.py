import FFTLinePixels as FFTLinePixels
VoltageFile = 'PicoValues.csv'
FFTOutFile = 'IndexInvertNew.csv'
#VoltageFile = 'LineData1.csv'
#FFTOutFile = 'LineDataTest.csv'
SamplesPerPixel =  25600

SensorFrequency = 30000
    
Gain = 100



# SamplesPerPixel =  10000
CoilFrequency = 400e3
SensorFrequency = 30e3
SamplingFrequency = 1/(512*1e-9)
Gain = 100
test1 = FFTLinePixels.FFTLine(VoltageFile,FFTOutFile,SamplesPerPixel,CoilFrequency,SensorFrequency,SamplingFrequency,Gain)
test1.FFTData()

