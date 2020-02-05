import cv2
import pydicom
import numpy as np


file = "/Users/adnanhafeez/Documents/TBCC Work/PicketFenceProblem/RI.ZPHYSICS_MONTHLY_U9.MV_90_0a1_0002.dcm"
dicom = pydicom.read_file(file)


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


def sortJaw(volume):
    ret, thresh = cv2.threshold(volume, 126, 255, 0)
    contours, hierarchy = cv2.findContours(thresh, 1, 2)
    cnt = contours[0]
    M = cv2.moments(cnt)
    x, y, w, h = cv2.boundingRect(cnt)
    img = cv2.rectangle(thresh, (x, y), (x + w, y + h), (0, 255, 0), 2)
    print(w,h)
    if w*0.5 > h:
        print("Y-jaw")
    elif h*0.5 > w:
        print("X-Jaw")
    else:
        print("Rotation Jaw")


sortJaw(rescale(dicom.pixel_array))

