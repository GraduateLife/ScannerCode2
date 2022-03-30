
TimeBaseArr = ['PS5000A_FS','PS5000A_PS','PS5000A_NS','PS5000A_US','PS5000A_MS','PS5000A_S']

#at velocity 100 and acceleration 200 
# micro step frequency is 3051  
# rps is 0.05960
motorSpeed = 100
pulseDiv = 4 
numerator = (16 * 10e6 * motorSpeed)
denom = (2**pulseDiv)*2048*32
vpps = (numerator/denom)/10
print(f'Microstep Frequency ,calculated value:{vpps}')
microsteps = 8
rps = (vpps)/(200*microsteps)
print(f"revolutions per second {rps} .")
speed = rps * 8 #speed in mm/s  
print(f"Corresponding speed is {speed}")

#now you have worked out the speed of the motor


defectLength = 50e-6 #check 

coilFrequency = 400e3
SamplingFrequency = 1953125
samplesPerSecond  = 1/SamplingFrequency
#calculate min defect length
MinDefectLength = samplesPerSecond * speed * 1e-3

print(f'Min defect length is {MinDefectLength}')
numberofsteps = 19500
mmMoved = numberofsteps/200
print(f'mm moved is {mmMoved}')
time = mmMoved/speed
print(f'time is {time}')
NumberOfSamples = time * SamplingFrequency
print(f'Number Of samples is: {NumberOfSamples}')
PixelsPerSample = NumberOfSamples/(mmMoved*(1/0.1))
desiredResolution = 0.5
numberOfPixels = mmMoved/desiredResolution
print(f'Omri\'s samples per pixel: {PixelsPerSample}')
samplesPerPixel = NumberOfSamples/numberOfPixels
print(f'My samples per pixel {samplesPerPixel}')
print(samplesPerPixel/PixelsPerSample)
mult = (50e-6)/MinDefectLength
print(mult)




#samplingFrequency = 2* CoilDr