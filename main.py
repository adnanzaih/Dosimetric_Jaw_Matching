import argparse
import os
import numpy as np
import pydicom
import matplotlib.pyplot as plt



def loadDicom(input):
    for dirName, subdirList, fileList in os.walk(input):
        for filename in fileList:
            if ".dcm" in filename.lower():  # check whether the file's DICOM
                dicomList.append(os.path.join(dirName,filename))
        Analyze(dicomList)


def Analyze(input):
    for x in input:
        ds = pydicom.read_file(x)
        matrixSize = ds[0x0028,0x0010].value
        seriesList.append(ds[0x0020,0x0011].value)
    combinePlots(seriesList, input, matrixSize)

def combinePlots(seriesList, input, matrixSize):
    xjaws = np.ndarray([matrixSize,matrixSize])
    yjaws = np.ndarray([matrixSize,matrixSize])
    rotjaws = np.ndarray([matrixSize,matrixSize])
    for name in input:
        ds = pydicom.read_file(name)
        if ds[0x0020,0x0011].value == np.asarray(seriesList).min():
            # print("X-Jaws is ", y)
            xjaws += ds.pixel_array
        elif ds[0x0020,0x0011].value == np.asarray(seriesList).max():
            # print("Y-Jaws is ", y)
            yjaws += ds.pixel_array
        else:
            # print("Rotation Jaw is ", y)
            rotjaws += ds.pixel_array

    plotPlots(xjaws, yjaws, rotjaws)


def plotPlots(a, b, c):
    a8bit = rescale(a)
    b8bit = rescale(b)
    c8bit = rescale(c)
    fig, axs = plt.subplots(1, 3)
    axs[0].imshow(a8bit)
    axs[0].set_title('X-Jaws')
    axs[1].imshow(b8bit)
    axs[1].set_title('Y-Jaws')
    axs[2].imshow(c8bit)
    axs[2].set_title('Rotation')
    plt.show()


def rescale(input):
    # rescale original 16 bit image to 8 bit values [0,255]
    x0 = input.min()
    x1 = input.max()
    y0 = 0
    y1 = 255.0
    i8 = ((input - x0) * ((y1 - y0) / (x1 - x0))) + y0
    # create new array with rescaled values and unsigned 8 bit data type
    o8 = i8.astype(np.uint8)
    return -o8


dicomList = []
seriesList = []
parser = argparse.ArgumentParser()
parser.add_argument('-input', dest='input', help='path to dicom directory', type=str)
results = parser.parse_args()
loadDicom(results.input)