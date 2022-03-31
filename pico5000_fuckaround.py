import csv
import time
import ctypes
import numpy as np
import pandas as pd
from picosdk.ps5000a import ps5000a as ps
import matplotlib.pyplot as plt
from picosdk.functions import adc2mV, assert_pico_ok

    #NOT NEEDED JUST FOR A TEST

#OFileName e.g. "something.csv"
#BitRes e.g. "PS5000A_DR_16BIT" change 16 to No'Bits required and copy and paste
#VoltRange e.g. 'PS5000A_1V'
#SampInterval e.g. any integer
#SampIntUnit  e.g. 'PS5000A_US' for microseconds
#BuffSize e.g. any int < 64M
#Caps e.g. any int < 250k
class StreamData:
    def __init__(self,OFileName,BitRes,VoltRange,SampInterval,SampIntUnit,BuffSize,Caps):
        self.OFileName = OFileName
        self.BitRes = BitRes
        self.VoltRange = VoltRange
        self.SampInterval = SampInterval
        self.SampIntUnit = SampIntUnit
        self.BuffSize = BuffSize
        self.Caps = Caps
        self.firstline = False

        self.chandle = ctypes.c_int16()
        self.status = {}

        f = open(self.OFileName, 'w') # open the file in the write mode
        f.close()

        # Open PicoScope 5000 Series device
        # Resolution set to 16 Bit
        
        self.resolution =ps.PS5000A_DEVICE_RESOLUTION[self.BitRes] ## 16bits needed
        # Returns handle to chandle for use in future API functions
        self.status["openunit"] = ps.ps5000aOpenUnit(ctypes.byref(self.chandle), None, self.resolution)

        try:
            assert_pico_ok(self.status["openunit"])
        except: # PicoNotOkError:

            self.powerStatus = self.status["openunit"]

            if self.powerStatus == 286:
                self.status["changePowerSource"] = ps.ps5000aChangePowerSource(self.chandle, self.powerStatus)
            elif self.powerStatus == 282:
                self.status["changePowerSource"] = ps.ps5000aChangePowerSource(self.chandle, self.powerStatus)
            else:
                raise

            self.assert_pico_ok(self.status["changePowerSource"])


        enabled = 1
        disabled = 0
        analogue_offset = 0.0

        # Set up channel A
        # handle = chandle
        # channel = PS5000A_CHANNEL_A = 0
        # enabled = 1
        # coupling type = PS5000A_DC = 1
        # range = PS5000A_2V = 7
        # analogue offset = 0 V
        self.channel_range = ps.PS5000A_RANGE[VoltRange]
        self.status["setChA"] = ps.ps5000aSetChannel(self.chandle,
                                                ps.PS5000A_CHANNEL['PS5000A_CHANNEL_A'],
                                                enabled,
                                                ps.PS5000A_COUPLING['PS5000A_DC'],
                                                self.channel_range,
                                                analogue_offset)
        assert_pico_ok(self.status["setChA"])

        # Size of capture
        self.sizeOfOneBuffer = BuffSize #64M
        self.numBuffersToCapture = Caps #maximum captures 250K

        self.totalSamples = self.sizeOfOneBuffer * self.numBuffersToCapture

        # Create buffers ready for assigning pointers for data collection
        global bufferAMax
        bufferAMax = np.zeros(shape=self.sizeOfOneBuffer, dtype=np.int16)
        self.memory_segment = 0

        # Set data buffer location for data collection from channel A
        # handle = chandle
        # source = PS5000A_CHANNEL_A = 0
        # pointer to buffer max = ctypes.byref(bufferAMax)
        # pointer to buffer min = ctypes.byref(bufferAMin)
        # buffer length = maxSamples
        # segment index = 0
        # ratio mode = PS5000A_RATIO_MODE_NONE = 0

        self.status["setDataBuffersA"] = ps.ps5000aSetDataBuffers(self.chandle,
                                                            ps.PS5000A_CHANNEL['PS5000A_CHANNEL_A'],
                                                            bufferAMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                            None,
                                                            self.sizeOfOneBuffer,
                                                            self.memory_segment,
                                                            ps.PS5000A_RATIO_MODE['PS5000A_RATIO_MODE_NONE'])
        assert_pico_ok(self.status["setDataBuffersA"])

        
    def GetVal(self,userSamples):
         tic = time.perf_counter()
         if(userSamples !=0):
            self.totalSamples = userSamples
        
         
         sampleInterval = ctypes.c_int32(self.SampInterval) ## sample frequency
         self.sampleUnits = ps.PS5000A_TIME_UNITS[self.SampIntUnit] #################################### After every 1 uS take a sample // rate = 1MHZ
        # We are not triggering:
         self.maxPreTriggerSamples = 0
         self.autoStopOn = 1
        # No downsampling:
         self.downsampleRatio = 1
         global bufferCompleteA
         bufferCompleteA = np.zeros(shape=self.totalSamples, dtype=np.int16)
         global nextSample
         nextSample = 0
         self.autoStopOuter = False
         wasCalledBack = False
         
         def streaming_callback(handle, noOfSamples, startIndex, overflow, triggerAt, triggered, autoStop, param):
            global nextSample, autoStopOuter, wasCalledBack, sourceEnd, destEnd
            wasCalledBack = True
            destEnd = nextSample + noOfSamples
            sourceEnd = startIndex + noOfSamples
            bufferCompleteA[nextSample:destEnd] = bufferAMax[startIndex:sourceEnd]
            nextSample += noOfSamples
            if autoStop:
                autoStopOuter = True


        # Convert the python function into a C function pointer.
         print('starting getting values')
         cFuncPtr = ps.StreamingReadyType(streaming_callback)
         self.status["runStreaming"] = ps.ps5000aRunStreaming(self.chandle,                    ######### read a second time
                                                        ctypes.byref(sampleInterval),
                                                        self.sampleUnits,
                                                        self.maxPreTriggerSamples,
                                                        self.totalSamples,
                                                        self.autoStopOn,
                                                        self.downsampleRatio,
                                                        ps.PS5000A_RATIO_MODE['PS5000A_RATIO_MODE_NONE'],
                                                        self.sizeOfOneBuffer)
         assert_pico_ok(self.status["runStreaming"])

         actualSampleInterval = sampleInterval.value
         actualSampleIntervalNs = actualSampleInterval ## sample frequency
        
         while nextSample < self.totalSamples and not self.autoStopOuter:
            wasCalledBack = False
            self.status["getStreamingLastestValues"] = ps.ps5000aGetStreamingLatestValues(self.chandle, cFuncPtr, None)
            if not wasCalledBack:
                # If we weren't called back by the driver, this means no data is ready. Sleep for a short while before trying
                # again.
                    time.sleep(0.01)
         toc = time.perf_counter()
         print(f'Finished Getting Values in {toc - tic:0.4f} seconds')
         
         tic = time.perf_counter()
         maxADC = ctypes.c_int16()
         self.status["maximumValue"] = ps.ps5000aMaximumValue(self.chandle, ctypes.byref(maxADC))
         assert_pico_ok
         (self.status["maximumValue"])
         timeArr = np.linspace(0, ((self.totalSamples - 1) * actualSampleIntervalNs), self.totalSamples)
    # Convert ADC counts data to mV
         #adc2mVChAMax = adc2mV(bufferCompleteA, self.channel_range, maxADC) 


         adc2mVChAMax = bufferCompleteA[0::10]
         #Combined = zip(adc2mVChAMax,timeArr)
         #columnHeads = ["Voltage","Time"]
         toc = time.perf_counter()
         print(f'starting file write in {toc - tic:0.4f}')
         
         tic = time.perf_counter()
         if self.firstline == False:
            f = open(self.OFileName, 'w') # open the file in the write mode
            wtr = csv.writer(f, delimiter=',', lineterminator='\n')
            wtr.writerow(["Voltage (mV)"])
            for x in adc2mVChAMax:
             wtr.writerow([x])
            self.firstline = True
        
         else:
            #print("values ", adc2mVChAMax)
            df = pd.read_csv(self.OFileName)
            new_column = pd.DataFrame({'Voltage (mV)': adc2mVChAMax}) 
            df = df.merge(new_column, left_index = True, right_index = True)
            df.to_csv(self.OFileName, index = False)
         toc = time.perf_counter()
         print(f"Done writing in {toc - tic:0.4f} .")
         
    def ClosePico (self):
        # Stop the scope
        # handle = chandle
        self.status["stop"] = ps.ps5000aStop(self.chandle)
        assert_pico_ok(self.status["stop"])

        # Disconnect the scope
        # handle = chandle
        self.status["close"] = ps.ps5000aCloseUnit(self.chandle)
        assert_pico_ok(self.status["close"])
        print("Picoscope Closed")

'''        
########################################################################################################################

def PicoVal(OFileName,BitRes,VoltRange,SampInterval,SampIntUnit,BuffSize,Caps):
    # Create chandle and status ready for use
    chandle = ctypes.c_int16()
    status = {}

    f = open(OFileName, 'w') # open the file in the write mode
    wtr = csv.writer(f, delimiter=',', lineterminator='\n')
    #writer = csv.writer(f)

    # Open PicoScope 5000 Series device
    # Resolution set to 16 Bit
    
    resolution =ps.PS5000A_DEVICE_RESOLUTION[BitRes] ## 16bits needed
    # Returns handle to chandle for use in future API functions
    status["openunit"] = ps.ps5000aOpenUnit(ctypes.byref(chandle), None, resolution)

    try:
        assert_pico_ok(status["openunit"])
    except: # PicoNotOkError:

        powerStatus = status["openunit"]

        if powerStatus == 286:
            status["changePowerSource"] = ps.ps5000aChangePowerSource(chandle, powerStatus)
        elif powerStatus == 282:
            status["changePowerSource"] = ps.ps5000aChangePowerSource(chandle, powerStatus)
        else:
            raise

        assert_pico_ok(status["changePowerSource"])


    enabled = 1
    disabled = 0
    analogue_offset = 0.0

    # Set up channel A
    # handle = chandle
    # channel = PS5000A_CHANNEL_A = 0
    # enabled = 1
    # coupling type = PS5000A_DC = 1
    # range = PS5000A_2V = 7
    # analogue offset = 0 V
    channel_range = ps.PS5000A_RANGE[VoltRange]
    status["setChA"] = ps.ps5000aSetChannel(chandle,
                                            ps.PS5000A_CHANNEL['PS5000A_CHANNEL_A'],
                                            enabled,
                                            ps.PS5000A_COUPLING['PS5000A_DC'],
                                            channel_range,
                                            analogue_offset)
    assert_pico_ok(status["setChA"])

    # Size of capture
    sizeOfOneBuffer = BuffSize #64M
    numBuffersToCapture = Caps #maximum captures 250K

    totalSamples = sizeOfOneBuffer * numBuffersToCapture

    # Create buffers ready for assigning pointers for data collection
    global bufferAMax
    bufferAMax = np.zeros(shape=sizeOfOneBuffer, dtype=np.int16)
    memory_segment = 0

    # Set data buffer location for data collection from channel A
    # handle = chandle
    # source = PS5000A_CHANNEL_A = 0
    # pointer to buffer max = ctypes.byref(bufferAMax)
    # pointer to buffer min = ctypes.byref(bufferAMin)
    # buffer length = maxSamples
    # segment index = 0
    # ratio mode = PS5000A_RATIO_MODE_NONE = 0

    status["setDataBuffersA"] = ps.ps5000aSetDataBuffers(chandle,
                                                        ps.PS5000A_CHANNEL['PS5000A_CHANNEL_A'],
                                                        bufferAMax.ctypes.data_as(ctypes.POINTER(ctypes.c_int16)),
                                                        None,
                                                        sizeOfOneBuffer,
                                                        memory_segment,
                                                        ps.PS5000A_RATIO_MODE['PS5000A_RATIO_MODE_NONE'])
    assert_pico_ok(status["setDataBuffersA"])

    # Begin streaming mode:
    sampleInterval = ctypes.c_int32(SampInterval) ## sample frequency
    sampleUnits = ps.PS5000A_TIME_UNITS[SampIntUnit] #################################### After every 1 uS take a sample // rate = 1MHZ
    # We are not triggering:
    maxPreTriggerSamples = 0
    autoStopOn = 1
    # No downsampling:
    downsampleRatio = 1
    
    status["runStreaming"] = ps.ps5000aRunStreaming(chandle,
                                                    ctypes.byref(sampleInterval),
                                                    sampleUnits,
                                                    maxPreTriggerSamples,
                                                    totalSamples,
                                                    autoStopOn,
                                                    downsampleRatio,
                                                    ps.PS5000A_RATIO_MODE['PS5000A_RATIO_MODE_NONE'],
                                                    sizeOfOneBuffer)
    assert_pico_ok(status["runStreaming"])

    
    actualSampleInterval = sampleInterval.value
    actualSampleIntervalNs = actualSampleInterval ## sample frequency

    print("Capturing at sample interval %s us" % actualSampleIntervalNs)

    # We need a big buffer, not registered with the driver, to keep our complete capture in.
    global bufferCompleteA
    bufferCompleteA = np.zeros(shape=totalSamples, dtype=np.int16)
    global nextSample
    nextSample = 0
    autoStopOuter = False
    wasCalledBack = False

    def streaming_callback(handle, noOfSamples, startIndex, overflow, triggerAt, triggered, autoStop, param):
        global nextSample, autoStopOuter, wasCalledBack, sourceEnd, destEnd
        wasCalledBack = True
        destEnd = nextSample + noOfSamples
        sourceEnd = startIndex + noOfSamples
        bufferCompleteA[nextSample:destEnd] = bufferAMax[startIndex:sourceEnd]
        nextSample += noOfSamples
        if autoStop:
            autoStopOuter = True


    # Convert the python function into a C function pointer.
    cFuncPtr = ps.StreamingReadyType(streaming_callback)
  ############################################################################################### Insert Flag here
    
    # Fetch data from the driver in a loop, copying it out of the registered buffers and into our complete one.
    while nextSample < totalSamples and not autoStopOuter:
        wasCalledBack = False
        status["getStreamingLastestValues"] = ps.ps5000aGetStreamingLatestValues(chandle, cFuncPtr, None)
        if not wasCalledBack:
            # If we weren't called back by the driver, this means no data is ready. Sleep for a short while before trying
            # again.
                import time
                time.sleep(0.01)

    print("Done grabbing values.")

    # Find maximum ADC count value
    # handle = chandle
    # pointer to value = ctypes.byref(maxADC)
    maxADC = ctypes.c_int16()
    status["maximumValue"] = ps.ps5000aMaximumValue(chandle, ctypes.byref(maxADC))
    assert_pico_ok
    (status["maximumValue"])

    # Convert ADC counts data to mV
    adc2mVChAMax = adc2mV(bufferCompleteA, channel_range, maxADC)

    # Create time data
    time = np.linspace(0, ((totalSamples - 1) * actualSampleIntervalNs), totalSamples)

    data_str=list(map(str,adc2mVChAMax))
    print(type(data_str[0]))
    
    Combined = zip(adc2mVChAMax,time)
    columnHeads = ["Voltage","Time"]
    wtr.writerow(columnHeads)
    for x in Combined:
        wtr.writerows([x])

    
    #writer.writerow(adc2mVChAMax)
    
    data_str=list(map(str,time))
    print(type(data_str[0]))

    #writer.writerow(time)
    print("Done writing.")
    f.close()
    counter = 0
    while counter != 3:
        status["runStreaming"] = ps.ps5000aRunStreaming(chandle,                    ######### read a second time
                                                        ctypes.byref(sampleInterval),
                                                        sampleUnits,
                                                        maxPreTriggerSamples,
                                                        totalSamples,
                                                        autoStopOn,
                                                        downsampleRatio,
                                                        ps.PS5000A_RATIO_MODE['PS5000A_RATIO_MODE_NONE'],
                                                        sizeOfOneBuffer)
        assert_pico_ok(status["runStreaming"])

        
        # Find maximum ADC count value
        # handle = chandle
        # pointer to value = ctypes.byref(maxADC)
        status["maximumValue"] = ps.ps5000aMaximumValue(chandle, ctypes.byref(maxADC))
        assert_pico_ok
        (status["maximumValue"])

        # Convert ADC counts data to mV
        nextSample = 0
        while nextSample < totalSamples and not autoStopOuter:
            wasCalledBack = False
            status["getStreamingLastestValues"] = ps.ps5000aGetStreamingLatestValues(chandle, cFuncPtr, None)
            if not wasCalledBack:
                # If we weren't called back by the driver, this means no data is ready. Sleep for a short while before trying
                # again.
                    import time
                    time.sleep(0.01)

        adc2amVChAMax = adc2mV(bufferCompleteA, channel_range, maxADC)
        
        df = pd.read_csv(OFileName)
        new_column = pd.DataFrame({'Voltage': adc2amVChAMax})
        df = df.merge(new_column, left_index = True, right_index = True)
        df.to_csv(OFileName, index = False)
        print("Done writing 2.")
        counter +=1

    # Stop the scope
    # handle = chandle
    status["stop"] = ps.ps5000aStop(chandle)
    assert_pico_ok(status["stop"])

    # Disconnect the scope
    # handle = chandle
    status["close"] = ps.ps5000aCloseUnit(chandle)
    assert_pico_ok(status["close"])

    # Display status returns
    print(status)
'''