from cgi import test
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft
import csv
import time
import ctypes
import os
filewrite = ctypes.CDLL('./fileio.dll')


class FFTLine:
    def __init__(self,VoltageFile,FFTOutFile,SamplesPerPixel,CoilFrequency,SensorFrequency,SampleFrequency,Gain):
        self.VoltageFile = VoltageFile
        self.FFTOutFile = FFTOutFile
        self.SamplesPerPixel = SamplesPerPixel
        self.CoilFrequency = CoilFrequency
        self.SensorFrequency = SensorFrequency
        self.SampleFrequency = SampleFrequency
        self.Gain = Gain
        self.firstline = False
        
        

    def FFTData(self, rowCounter):
        f = open(self.FFTOutFile, 'w') # open the file in the write mode
        wtr = csv.writer(f, delimiter=',', lineterminator='\n')
        inputFile = f'Row{rowCounter}.csv'
        with open(inputFile,'r') as fileobj:
            reader_obj = csv.reader(fileobj,quoting=csv.QUOTE_NONNUMERIC)
            rowCounter = 0
            tic = time.perf_counter()
            for row in reader_obj:
                toc = time.perf_counter()
                print(f"for loop takes {toc - tic:0.4f} .")
                rowCounter += 1
                #this is dumb but it works
                
                nprow = np.array(row)
                
                if (rowCounter)%2 == 0:
                    rowlist=rowlist[::-1]
                    
                    


                #print(f'length of row should now be 10000: {len(rowlist)}')
                def chunks(lst, n): # splits into chunks of n
                    """Yield successive n-sized chunks from lst."""
                    #print('calling chunks')
                    for i in range(0, len(lst), n):
                        yield lst[i:i + n]

                
                a = chunks(nprow,self.SamplesPerPixel)
                
                FFTLineabs = []
                FFTLinemax = []
                dt = 1/self.SampleFrequency
                for val in a:
                    
                    FFTPixel = rfft(val) #rfft((val/(100*1000)))*dt taken out: (self.Gain*1000)
                    FFTLineabs = abs(FFTPixel)
                    #plt.xlabel('Frequency (Hz)')
                    #plt.ylabel('Voltage (V)')
                
                    freq=rfftfreq(len(val),d=dt)
                
                    #plt.plot(freq,FFTLineabs)
                    #plt.show()
                    points_per_freq = len(FFTLineabs) / (self.SampleFrequency / 2)
                    CoilFreq = int(points_per_freq * self.CoilFrequency)
                    upperBandCutoff = int(points_per_freq * (self.CoilFrequency+self.SensorFrequency))
                    lowerBandCutoff = int(points_per_freq * (self.CoilFrequency-self.SensorFrequency)) ##get rid of 200KHz
                    SensorBias = int(points_per_freq * self.SensorFrequency) ##get rid of 30KHz
                    FFTLineabs[CoilFreq - 40 : CoilFreq + 40] = 0 ##Set Freq bin of Coil to 0
                    FFTLineabs[SensorBias - 50 : SensorBias + 50] = 0
                    FFTLineabs[upperBandCutoff +1: 10000000] = 0 ##Set Sensor Biasing Freq bin to 0
                    FFTLineabs[0 :  lowerBandCutoff-1] = 0 ##Set DC Freq bin to 0
                
                
                # plt.plot(freq,FFTLineabs)
                # plt.show()
                    #FFTLineabs[counter] = abs(FFTPixel)
                    
                    FFTLinemax.append(np.amax(FFTLineabs)) #add largest absolute values to array
            wtr.writerow(FFTLinemax)
            os.system(f'rm Row{rowCounter}.csv')
            '''
            if self.firstline == False: 
                
                wtr.writerows([FFTLinemax])
                #wtr.writerow(["Voltage (mV)"])
                for x in FFTLinemax:
                    wtr.writerow([x])
                self.firstline = True
                f.close()  
            
            else:
                #print("values ", adc2mVChAMax)
                df = pd.read_csv(self.FFTOutFile)
                new_column = pd.DataFrame(FFTLinemax) 
                df = df.merge(new_column, left_index = True, right_index = True)
                df.to_csv(self.FFTOutFile, index = False)
             '''    
        #pd.read_csv(self.FFTOutFile, header=None).T.to_csv('Transpose.csv', header=False, index=False) #Transpose csv file

            
            
        

    






