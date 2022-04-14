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
    plt.show()

showContour('1431FFTOutput.csv')