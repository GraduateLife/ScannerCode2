import pandas as pd
import cv2 as cv
import numpy as np
import matplotlib.pyplot as plt



def showImage(rows,columns,filename):
    img = pd.read_csv(filename)
    imgArray = np.asarray(img)
    print(imgArray.shape)
    maxVal = np.max(imgArray)
    minVal = np.min(imgArray)
    print(maxVal)
    print(minVal)
    resized = np.zeros((rows,int(columns/10)))
    for row in range(rows):
        for column in range(0,columns,10):
            upperLimit = column +9
            PixelSum = np.sum(imgArray[row,column:upperLimit])
            PixelAverage = PixelSum/10
            normalised = (PixelAverage-minVal)/(maxVal-minVal)
            finalValue = normalised
            resized[row,int(column/10)] = finalValue
            #print(f'Value in array is {imgArray[row,column]}')


    # im_color = cv.applyColorMap(resized, cv.COLORMAP_JET)
    # cv.imshow('Image',im_color)
    # cv.waitKey(0)
    # cv.destroyAllWindows
    plt.imshow(resized,cmap='coolwarm')
    plt.savefig('ScanOutput.png')

]

