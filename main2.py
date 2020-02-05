import argparse
import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt
import cv2


def loadDicom(input):
    for dirName, subdirList, fileList in os.walk(input):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check whether the file's DICOM
                dicomList.append(os.path.join(dirName,filename))
        sortJaw(dicomList, [int(np.shape(pydicom.read_file(dicomList[0]).pixel_array)[0]),int(np.shape(pydicom.read_file(dicomList[0]).pixel_array)[1])])


def sortJaw(dicomList, matrixSize):
    xJawArray = np.ndarray([matrixSize[0],matrixSize[1]])
    yJawArray = np.ndarray([matrixSize[0],matrixSize[1]])
    rotJawArray = np.ndarray([matrixSize[0],matrixSize[1]])
    for name in dicomList:
        ds_jaw = pydicom.read_file(name)
        ret, thresh = cv2.threshold(rescale(ds_jaw.pixel_array), 126, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cnt = contours[0]
        x, y, w, h = cv2.boundingRect(cnt)
        #print(w, h)
        if w * 0.5 > h:
            #print("Y-jaw")
            yJawArray += rescale(ds_jaw.pixel_array)
        elif h * 0.5 > w:
            #print("X-Jaw")
            xJawArray += rescale(ds_jaw.pixel_array)
        else:
            #print("Rotation Jaw")
            rotJawArray += rescale(ds_jaw.pixel_array)

    plotPlots(xJawArray, yJawArray, rotJawArray)


def rescale(input):
    # rescale original 16 bit image to 8 bit values [0,255]
    x0 = input.min()
    x1 = input.max()
    y0 = 0
    y1 = 255
    i8 = ((input - x0) * ((y1 - y0) / (x1 - x0))) + y0
    # create new array with rescaled values and unsigned 8 bit data type
    o8 = i8.astype(np.uint8)
    return o8


def plotPlots(a,b,c):
    fig, axs = plt.subplots(1, 3)
    axs[0].imshow(a,cmap='twilight')
    axs[0].set_title('X-Jaws')
    axs[1].imshow(b,cmap='twilight')
    axs[1].set_title('Y-Jaws')
    axs[2].imshow(c,cmap='twilight')
    axs[2].set_title('Rotation')
    plt.show()


dicomList = []
parser = argparse.ArgumentParser()
parser.add_argument('-input', dest='input', help='path to dicom directory', type=str)
results = parser.parse_args()
loadDicom(results.input)