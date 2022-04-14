
def calculateParameters(parameterDictionary):
    samplingFrequency = 1/(parameterDictionary["samplingPeriod"] * parameterDictionary["picoTimebase"])
    yTotalSteps = parameterDictionary["mmMovedY"] *200
    yIncrements =  parameterDictionary["mmMovedY"]/parameterDictionary["yResolutionMm"]
    yStepIncrement = yTotalSteps/yIncrements


    pulseDiv = 4 
    numerator = (16 * 10e6 * parameterDictionary["motorSpeed"])
    denom = (2**pulseDiv)*2048*32
    vpps = (numerator/denom)/10

    microsteps = 8
    rps = (vpps)/(200*microsteps)
 #print(f"revolutions per second {rps} .")
    speed = rps * 8 #speed in mm/s  
#print(f"Corresponding speed is {speed}")

#now you have worked out the speed of the motor


     #defectLength = 50e-6 #check 

    #coilFrequency = coilF

   
    
#calculate min defect length
    # = samplesPerSecond * speed * 1e-3

    #print(f'Min defect length is {MinDefectLength}')
    #numberofsteps = 35500
   
    numberofsteps = int(parameterDictionary["mmMovedX"]*200)  #return
    #print(f'mm moved is {mmMoved}')
    time =parameterDictionary["mmMovedX"]/speed
    #print(f'time is {time}, sampling frequency is {SamplingF}')
    NumberOfSamples = round(time * samplingFrequency)  #return this value
    #print(f'Number Of samples is: {NumberOfSamples}')
    PixelsPerSample = NumberOfSamples/(parameterDictionary["mmMovedX"]*(1/parameterDictionary['xResolutionMm']))
    PixelsPerSample = round(PixelsPerSample) #return
    

    #print(f'Omri\'s samples per pixel: {PixelsPerSample}')
    #samplesPerPixel = NumberOfSamples/numberOfPixels
    #print(f'My samples per pixel {samplesPerPixel}')
    #print(samplesPerPixel/PixelsPerSample)
    #mult = (50e-6)/MinDefectLength
    #print(mult)
    print(numberofsteps)
    print(NumberOfSamples)
    print(PixelsPerSample)
    return numberofsteps, NumberOfSamples, PixelsPerSample, yStepIncrement, yIncrements,samplingFrequency



#samplingFrequency = 2* CoilDr
