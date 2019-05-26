''' classification


    This module is used to classify the images into one of the tyoes:
        1.Foot
        2.Front Upper Body
        3.Back Upper Body
        4.Front Legs
        5.Back Legs

Created on 25/05/2019
@author: Carlos Cesar Brochine Junior

'''
import numpy as np
import cv2
import imutils
import os

def impanting(image_path,mask_path):
    """Image Impanting: this uses a mask to interpolate a mask region with surroundings pixels.

        Args:
            image_path(str): The path where the source image is stored.
            mask_path(str): The path where the mask is stored.

        Returns:
            image(cv2.image): impanted image
    """
    img = cv2.imread(image_path)
    mask = cv2.imread(mask_path, 0)
    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    return dst

def external_contour(image):
    """External contour: this function provides the most external contour in a image.
        Args:
            image(cv2.image): image loaded by cv2.imread.

        Returns:
            image(cv2.image): impanted image
        References:
            https://docs.opencv.org/3.4/d1/d32/tutorial_py_contour_properties.html
    """

    # load the image, convert it to grayscale, and blur it slightly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

    # threshold the image, then perform a series of erosions +
    # dilations to remove any small regions of noise
    thresh = cv2.threshold(gray, 45, 255, cv2.THRESH_BINARY)[1]
    thresh = cv2.erode(thresh, None, iterations=2)
    thresh = cv2.dilate(thresh, None, iterations=2)

    # find contours in thresholded image, then grab the largest one
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    c = max(cnts, key=cv2.contourArea)

    return c


def image_kind(image_path):
    """image_kind classifies the image from a path into one of the types desired

        Args:
            image_path(str): The path where the image is stored.

        Returns:
            kind(int): The number of classification according the relation:
                 1:Foot
                 2:Front Upper Body
                 3:Back Upper Body
                 4:Front Legs
                 5:Back Legs
        Examples:
            Examples should be written in doctest format, and should illustrate how
            to use the function.
    """
    mask_path=r'image_map/mask.jpeg'
    img = cv2.imread(image_path)
    dimension=img.shape
    # Foot images are landscape and others are portrait, so it is possible to define if foot by dimension
    if dimension[0] == 480:
        kind=1
        solidity,aspect_ratio='NA'
    else:
        kind='unknown'
        impant=impanting(image_path,mask_path)
        contorno = external_contour(impant)
        area=cv2.contourArea(contorno)
        c=contorno
        #solidity
        hull = cv2.convexHull(contorno)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area
        #aspect ratio
        x, y, w, h = cv2.boundingRect(contorno)
        aspect_ratio = float(w) / h
        if aspect_ratio>0.60:
            kind='dorso'
        elif aspect_ratio<0.60:
            kind='perna'
    return kind,solidity,aspect_ratio

if __name__ == '__main__':
    image_folder=r'../testes/images'
    image_file=r'../testes/images/dorso_costa01.jpeg'
    mask_path=r'image_map/mask.jpeg'
    teste=impanting(image_file,mask_path)
    contorno=external_contour(teste)

    # draw contours
    # cv2.drawContours(teste, [contorno], -1, (0, 255, 0), 3)
    # convex hull
    # cov=cv2.convexHull(contorno)
    # cv2.drawContours(teste, [cov], -1, (0, 255, 0), 3)
    # #
    # cv2.imshow("Image", teste)
    # cv2.waitKey()
    # cv2.destroyAllWindows()

    #contour Area
    print(cv2.contourArea(contorno))
    print('file,kind,area')
    for file in os.listdir(image_folder):
        file_path=os.path.join(image_folder,file)
        k,s,ar=image_kind(file_path)
        if k is not 1:
            print(file,k,s,ar)
