from cgi import test
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft
from scipy.stats import iqr
import csv
from scipy.signal import butter, lfilter
import os
import ctypes
from datetime import datetime
import heapq as hp
filewrite = ctypes.CDLL('./fileio.dll')

class FFTLine:
    def __init__(self,filename,SamplesPerPixel,CoilFrequency,SensorFrequency,SampleFrequency,Gain):
        now = datetime.now()
        self.FFTOutFile = now.strftime("%H%MFFTOutput.csv")
        self.SamplesPerPixel = SamplesPerPixel
        self.CoilFrequency = CoilFrequency
        self.SensorFrequency = SensorFrequency
        self.SampleFrequency = SampleFrequency
        self.Gain = Gain
        self.firstline = False
        
        

    def FFTData(self,rowCounter,rowArray):
        # def butter_bandpass(lowcut, highcut, fs, order=5):
        #     return butter(order, [lowcut, highcut], fs=fs, btype='band')

        # def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
        #     b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        #     y = lfilter(b, a, data)
        #     return y
        f = open(self.FFTOutFile, 'a') # open the file in the write mode
        wtr = csv.writer(f, delimiter=',', lineterminator='\n')
        if (rowCounter)%2 == 0:
                    rowArray=rowArray[::-1]

        def chunks(lst, n): # splits into chunks of n
                    """Yield successive n-sized chunks from lst."""
                    #print('calling chunks')
                    for i in range(0, len(lst), n):
                        yield lst[i:i + n]   

        sum = 0
        aver = 0     
        a = chunks(rowArray,self.SamplesPerPixel)
        #a = butter_bandpass_filter(a , 360e3,380e3, 1953125, order=9)
        FFTLineabs = []
        FFTLinemax = []
        dt = 1/self.SampleFrequency
    
        for val in a:
            
            FFTPixel = rfft(val) #rfft((val/(100*1000)))*dt
            FFTLineabs = abs(FFTPixel)
            
            #plt.xlabel('Frequency (Hz)')
            #plt.ylabel('Voltage (V)')
        
            freq=rfftfreq(len(val),d=dt)
            # FFTOutput = zip(freq,FFTLineabs)
            # FFTDF = pd.DataFrame(FFTOutput)
            # FFTDF.to_csv('preFilterFFT.csv')
            # plt.plot(freq,FFTLineabs)
            # plt.savefig('preFilterFFT.jpg')

            points_per_freq = len(FFTLineabs) / (self.SampleFrequency / 2)
            CoilFreq = int(points_per_freq * self.CoilFrequency)
            upperBandCutoff = int(points_per_freq * (self.CoilFrequency+self.SensorFrequency))
            lowerBandCutoff = int(points_per_freq * (self.CoilFrequency-self.SensorFrequency)) ##get rid of 200KHz
            SensorBias = int(points_per_freq * self.SensorFrequency) ##get rid of 30KHz
            FFTLineabs[CoilFreq - 40 : CoilFreq + 40] = 0 ##Set Freq bin of Coil to 0
            FFTLineabs[SensorBias - 50 : SensorBias + 50] = 0
            FFTLineabs[upperBandCutoff +1: 10000000] = 0 ##Set Sensor Biasing Freq bin to 0
            FFTLineabs[0 :  lowerBandCutoff-1] = 0
            
            # FFTOutput = zip(freq,FFTLineabs)
            # FFTDF = pd.DataFrame(FFTOutput)
            # FFTDF.to_csv('postFilterFFT.csv')

             ##Set DC Freq bin to 0
            # plt.plot(freq,FFTLineabs)
            # plt.savefig('postFilterFFT.jpg')
            #FFTLineabs[counter] = abs(FFTPixel)
            #FFTs = hp.nlargest(2,FFTLineabs)
            #FFTout = np.sum(FFTs)
            #print(FFTout)
            FFTout =np.amax(FFTLineabs)
            sum = sum+ round(FFTout)
            FFTLinemax.append(FFTout) #add largest absolute values to array
        
        aver = sum /(len(FFTLinemax))

        #added some code to remove outliers
        

        Q1 = np.quantile(FFTLinemax,0.25)
        Q3 = np.quantile(FFTLinemax,0.75)
        IQR = Q3 - Q1
        low = Q1 - 1.5*IQR
        up = Q3 + 1.5*IQR

        for i in range(len(FFTLinemax)):
            #FFTLinemax[i] = FFTLinemax[i] - (aver)
            if FFTLinemax[i]>up or FFTLinemax[i]<low:
                FFTLinemax[i] = aver
            
            # elif FFTLinemax[i]<(0):
            #     FFTLinemax[i]= 0
            else:
               # FFTLinemax[i]=np.abs(FFTLinemax[i])
                FFTLinemax[i]=FFTLinemax[i]

            #FFTLinemax[i] = FFTLinemax[i]*(255/(np.amax(FFTLinemax)-np.amin(FFTLinemax)))
        print (aver)
        print(up)
        print(low)
        
        aver = 0
        sum = 0
        # FFTLinemax =  np.array(FFTLinemax)
        # print(f'Data type of array is{FFTLinemax.dtype}')
        # string1 : ctypes.Array[ctypes.c_char] = ctypes.create_string_buffer(bytes(self.FFTOutFile,'utf-8'))
        # arrayPointer = ctypes.POINTER(ctypes.c_int16)
         
        # filewrite.write_to_csv(string1,FFTLinemax.ctypes.data_as(arrayPointer),len(FFTLinemax),rowCounter)
        wtr.writerow(FFTLinemax)


        
        print('FFT Done')
               
                
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

            
            
        

    






