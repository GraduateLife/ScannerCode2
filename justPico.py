import pico5000 as pico5000

if __name__ == '__main__':

    CoilFrequency = 300e3
    SamplingFrequency = 800e3
    SamplingInterval = int((1/SamplingFrequency)*1e9)
    BufferSize = 88000
    Captures = 100
    test1 = pico5000.StreamData('PicoValues.csv',"PS5000A_DR_16BIT",'PS5000A_1V',SamplingInterval,'PS5000A_NS',BufferSize,Captures)
    test1.GetVal(1000)
    test1.ClosePico()