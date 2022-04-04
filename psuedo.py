
def param(SamplingF,mm):
    motorSpeed = 100
    pulseDiv = 4 
    numerator = (16 * 10e6 * motorSpeed)
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

    SamplingFrequency = SamplingF
    
#calculate min defect length
    # = samplesPerSecond * speed * 1e-3

    #print(f'Min defect length is {MinDefectLength}')
    #numberofsteps = 35500
    mmMoved = mm
    numberofsteps = int(mm*200)  #return
    #print(f'mm moved is {mmMoved}')
    time = mmMoved/speed
    #print(f'time is {time}')
    NumberOfSamples = round(time * SamplingFrequency)  #return this value
    #print(f'Number Of samples is: {NumberOfSamples}')
    PixelsPerSample = NumberOfSamples/(mmMoved*(1/0.1))
    PixelsPerSample = round(PixelsPerSample) #return
    desiredResolution = 0.5
    numberOfPixels = mmMoved/desiredResolution
    #print(f'Omri\'s samples per pixel: {PixelsPerSample}')
    #samplesPerPixel = NumberOfSamples/numberOfPixels
    #print(f'My samples per pixel {samplesPerPixel}')
    #print(samplesPerPixel/PixelsPerSample)
    #mult = (50e-6)/MinDefectLength
    #print(mult)
    return numberofsteps, NumberOfSamples, PixelsPerSample



#samplingFrequency = 2* CoilDr
