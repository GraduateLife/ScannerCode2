from cgi import test
import numpy as np
import pandas as pd
import sys
from matplotlib import pyplot as plt
from scipy.fft import fft, fftfreq
from scipy.fft import rfft, rfftfreq
from scipy.fft import irfft
import csv
from scipy.signal import butter, lfilter

class FFTLine:
    def __init__(self,FFTOutFile,SamplesPerPixel,CoilFrequency,SensorFrequency,SampleFrequency,Gain):
       
        self.FFTOutFile = FFTOutFile
        self.SamplesPerPixel = SamplesPerPixel
        self.CoilFrequency = CoilFrequency
        self.SensorFrequency = SensorFrequency
        self.SampleFrequency = SampleFrequency
        self.Gain = Gain
        self.firstline = False
        
        

    def FFTData(self,rowCounter):
        # def butter_bandpass(lowcut, highcut, fs, order=5):
        #     return butter(order, [lowcut, highcut], fs=fs, btype='band')

        # def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
        #     b, a = butter_bandpass(lowcut, highcut, fs, order=order)
        #     y = lfilter(b, a, data)
        #     return y
        f = open(self.FFTOutFile, 'a') # open the file in the write mode
        wtr = csv.writer(f, delimiter=',', lineterminator='\n')
        sum = 0
        aver = 0
        inputFile = f'Row{rowCounter}.csv'
        with open(inputFile,'r') as fileobj:
            reader_obj = csv.reader(fileobj,quoting=csv.QUOTE_NONNUMERIC)
            rowCounter = 1
            for row in reader_obj:
                
                #this is dumb but it works
                
                
                rowlist = np.array(row)
                
                
                
                
                
                if (rowCounter)%2 == 0:
                    rowlist=rowlist[::-1]
                    
                    
                rowCounter += 1    


                #print(f'length of row should now be 10000: {len(rowlist)}')
                def chunks(lst, n): # splits into chunks of n
                    """Yield successive n-sized chunks from lst."""
                    #print('calling chunks')
                    for i in range(0, len(lst), n):
                        yield lst[i:i + n]

                
                a = chunks(rowlist,self.SamplesPerPixel)
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
                    #plt.plot(freq,FFTLineabs)
                    #plt.show()
                    #FFTLineabs[counter] = abs(FFTPixel)
                    FFTout = np.amax(FFTLineabs)
                    #print(FFTout)
                    sum = sum+ round(FFTout)
                    
                    FFTLinemax.append(FFTout) #add largest absolute values to array
                
                aver = sum /(len(FFTLinemax))
                average = 0
                sum2 = 0
                for i in range(len(FFTLinemax)):
                    FFTLinemax[i] = FFTLinemax[i] - aver
                    if FFTLinemax[i]<(aver*0.04):
                        FFTLinemax[i]=0
                    else:
                        FFTLinemax[i]=FFTLinemax[i]
                    FFTLinemax[i] = FFTLinemax[i]*(255/(np.amax(FFTLinemax)-np.amin(FFTLinemax)))
                print (aver)
                aver = 0
                sum = 0
                wtr.writerow(FFTLinemax)
                #os.system(f'rm Row{rowCounter}.csv')
                
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

            
            
        

    






