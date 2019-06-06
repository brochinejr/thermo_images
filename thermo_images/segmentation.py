import classification as cls
import os
import cv2
import imutils
import numpy as np

def plot_contours(image):

    # load the image, convert it to grayscale, and blur it slightly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    cv2.imshow("Image", gray)
    cv2.waitKey(0)

    # threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)
    #
    dimension = gray.shape
    X_DIMENSION = dimension[0]
    Y_DIMENSION = dimension[1]
    black_image = np.zeros((X_DIMENSION, Y_DIMENSION))
    #
    # find contours in thresholded image, then grab the largest one
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    # c = max(cnts, key=cv2.contourArea)
    # draw the outline of the object, then draw each of the
    for c in cnts:
        cv2.drawContours(black_image, [c], -1, (255, 0, 255), 2)

    # show the output image
    # cv2.imshow("Image", black_image)
    # cv2.waitKey(0)
    return black_image

pasta=r'/home/ccjunio/PycharmProjects/thermo_images/thermo_images/image_map/maps'
for image_path in os.listdir(pasta):
    print(image_path)
    dir=os.path.join(pasta,image_path)
    img = cv2.imread(dir)
    print(img.shape)
    bk = plot_contours(img)
    cv2.imshow("Image", bk)
    cv2.waitKey(0)