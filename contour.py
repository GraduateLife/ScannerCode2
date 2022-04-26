import pandas as pd 
import matplotlib.pyplot as plt 
import numpy as np


def showContour(filename):
    img = pd.read_csv(filename)
    imgArray = np.asarray(img)
    print(imgArray.shape)
    rows, columns = imgArray.shape
    maxVal = np.max(imgArray)
    minVal = np.min(imgArray)
    print(maxVal)
    print(minVal)

    # Q1 = np.quantile(imgArray,0.25)
    # Q3 = np.quantile(imgArray,0.75)
    # IQR = Q3 - Q1
    # low = Q1 - 1.5*IQR
    # up = Q3 + 1.5*IQR

    # for i in range(len(FFTLinemax)):
    #     #FFTLinemax[i] = FFTLinemax[i] - (aver)
    #     if FFTLinemax[i]>up or FFTLinemax[i]<low:
    #         FFTLinemax[i] = aver
        
    #     # elif FFTLinemax[i]<(0):
    #     #     FFTLinemax[i]= 0
    #     else:
    #         # FFTLinemax[i]=np.abs(FFTLinemax[i])
    #         FFTLinemax[i]=FFTLinemax[i]



    resized = np.zeros((rows,int(columns/10)))
    for row in range(rows):
        for column in range(0,int(columns),10):
            upperLimit = column +9
            PixelSum = np.sum(imgArray[row,column:upperLimit])
            PixelAverage = PixelSum/10
            normalised = (PixelAverage-minVal)/(maxVal-minVal)
            finalValue = normalised
            resized[row,int(column/10)] = finalValue


    getShape = img.shape
    print(resized.shape)

    x = np.arange(columns/10)
    #print(f'array for x axis is {x}')
    y = np.arange(rows)
    #print(y)
    x, y = np.meshgrid(x, y)

    # Array = fftDataframe.to_numpy()
    # paddedArray =np.pad(Array,738)
    #print(f'shape of padded array is {paddedArray.shape}')
    fig = plt.figure()
    ax = plt.axes(projection='3d')
    ax.contour3D(x, y, resized, 50, cmap='coolwarm')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.set_title('3D contour')
    ax.view_init(20, 100)
    # fig,ax=plt.subplots(1,1)
    # cp = ax.contourf(x, y, resized)
    # fig.colorbar(cp) # Add a colorbar to a plot
    # ax.set_title('Filled Contours Plot')
    # #ax.set_xlabel('x (cm)')
    # ax.set_ylabel('y (cm)')
    plt.show()





    plt.show()

showContour('./Results/2204FFTOutput1554.csv')