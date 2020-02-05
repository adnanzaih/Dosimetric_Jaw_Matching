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


def sortJaw(input, matrixSize):
    xJawArray = np.zeros(shape=(2,matrixSize[0],matrixSize[1]))
    yJawArray = np.zeros(shape=(4,matrixSize[0],matrixSize[1]))
    rotJawArray = np.zeros(shape=(4,matrixSize[0],matrixSize[1]))
    i = 0
    k = 0
    z = 0
    for name in dicomList:
        ds_jaw = pydicom.read_file(name)
        ret, thresh = cv2.threshold(rescale(ds_jaw.pixel_array), 126, 255, 0)
        contours, hierarchy = cv2.findContours(thresh, 1, 2)
        cnt = contours[0]
        x, y, w, h = cv2.boundingRect(cnt)
        #print(w, h)
        if w * 0.5 > h:
            #print("Y-jaw")
            yJawArray[i] = np.array(rescale(ds_jaw.pixel_array))
            i += 1
        elif h * 0.5 > w:
            #print("X-Jaw")
            xJawArray[k] = np.array(rescale(ds_jaw.pixel_array))
            k += 1
        else:
            #print("Rotation Jaw")
            #further_sort_rot(ds_jaw)
            if x < 400 and y < 300:
                rotJawArray[0] = np.array(rescale(ds_jaw.pixel_array))
                print("rot 1",x,y)
            elif x > 400 and y < 300:
                rotJawArray[1] = np.array(rescale(ds_jaw.pixel_array))
                print("rot 2", x,y)
            elif x < 400 and y > 300:
                rotJawArray[2] = np.array(rescale(ds_jaw.pixel_array))
                print("rot 3", x, y)
            elif x > 400 and y > 300:
                rotJawArray[3] = np.array(rescale(ds_jaw.pixel_array))
                print("rot 4", x, y)

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
    axs[0].imshow((a[0]+np.roll(a[1],-1,axis=1)))
    axs[0].set_title('X-Jaws')
    axs[1].imshow((b[0]+b[1]+b[2]+b[3]))
    axs[1].set_title('Y-Jaws')
    axs[2].imshow((c[0]+c[1]+c[2]+c[3]))
    axs[2].set_title('Rotation')
    plt.show()


dicomList = []
imageList = []
parser = argparse.ArgumentParser()
parser.add_argument('-input', dest='input', help='path to dicom directory', type=str)
results = parser.parse_args()
loadDicom(results.input)
