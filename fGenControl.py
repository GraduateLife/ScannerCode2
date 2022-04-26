import pyvisa 

def turnFgenOn():
    rm = pyvisa.ResourceManager()
    #print(rm.list_resources())
    my_instrument = rm.open_resource('USB0::0x1AB1::0x0642::DG1ZA190300033::0::INSTR')
    my_instrument.read_termination = '\n'
    my_instrument.write_termination = '\n'
    my_instrument.write(':OUTP1 ON')
    my_instrument.write(':OUTP2 ON')
    my_instrument.close()



def setFgenParams(coilFrequency, coilAmplitude,sensorFrequency, sensorAmplitude):
    rm = pyvisa.ResourceManager()
    #print(rm.list_resources())
    my_instrument = rm.open_resource('USB0::0x1AB1::0x0642::DG1ZA190300033::0::INSTR')

    my_instrument.read_termination = '\n'
    my_instrument.write_termination = '\n'
    my_instrument.write(':SOUR1:VOLT:UNIT VRMS')
    my_instrument.write(':SOUR2:VOLT:UNIT VRMS')

    my_instrument.write(f':SOUR1:APPL:SIN {coilFrequency},{coilAmplitude},0,0')
    my_instrument.write(f':SOUR2:APPL:SIN {sensorFrequency},{sensorAmplitude},0,0')
    my_instrument.close()




def turnFgenOff():
    rm = pyvisa.ResourceManager()
    my_instrument = rm.open_resource('USB0::0x1AB1::0x0642::DG1ZA190300033::0::INSTR')
    my_instrument.write(':OUTP1 OFF')
    my_instrument.write(':OUTP2 OFF')
    my_instrument.close()
