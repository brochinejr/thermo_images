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
import math


def plot_contours(image):

    # load the image, convert it to grayscale, and blur it slightly
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)

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
    c = max(cnts, key=cv2.contourArea)

    # draw the outline of the object, then draw each of the
    cv2.drawContours(black_image, [c], -1, (255, 0, 255), 2)

    # show the output image
    # cv2.imshow("Image", black_image)
    # cv2.waitKey(0)
    return black_image,c





def skeleton(img):
    """Topolopgical Skeleton: this function provides topoloical skeleton of an image.
        Args:
            image(cv2.image): image loaded by cv2.imread.

        Returns:
            image(cv2.image): skeletonized image
        References:
            - https://en.wikipedia.org/wiki/Topological_skeleton
            - http://opencvpython.blogspot.com/2012/05/skeletonization-using-opencv-python.html
    """
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    size = np.size(img)
    skel = np.zeros(img.shape, np.uint8)

    ret, img = cv2.threshold(img, 127, 255, 0)
    element = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))
    done = False
    while (not done):
        eroded = cv2.erode(img, element)
        temp = cv2.dilate(eroded, element)
        temp = cv2.subtract(img, temp)
        skel = cv2.bitwise_or(skel, temp)
        img = eroded.copy()

        zeros = size - cv2.countNonZero(img)
        if zeros == size:
            done = True
    return skel

# def impanting(image_path,mask_path):
def impanting(img,mask_path):
    """Image Impanting: this uses a mask to interpolate a mask region with surroundings pixels.

        Args:
            image_path(str): The path where the source image is stored.
            mask_path(str): The path where the mask is stored.

        Returns:
            image(cv2.image): impanted image
    """
    # img = cv2.imread(image_path)
    mask = cv2.imread(mask_path, 0)
    dst = cv2.inpaint(img, mask, 3, cv2.INPAINT_TELEA)
    return dst

def shape_match(im1,im2):
    """Shape Distance: returns de distance between two images based on Hu moments.

        Args:
            im1(cv2.image): gray image 1.
            im2(cv2.image): gray image 2

        Returns:
            d1,d2,d3 (float): distance based on Hu moments

        References:
            https://www.learnopencv.com/shape-matching-using-hu-moments-c-python/
    """
    # im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    _, im1 = cv2.threshold(im1, 128, 255, cv2.THRESH_BINARY)
    _, im2 = cv2.threshold(im2, 128, 255, cv2.THRESH_BINARY)
    d1 = cv2.matchShapes(im1, im2, cv2.CONTOURS_MATCH_I1, 0)
    d2 = cv2.matchShapes(im1, im2, cv2.CONTOURS_MATCH_I2, 0)
    d3 = cv2.matchShapes(im1, im2, cv2.CONTOURS_MATCH_I3, 0)
    return d1,d2,d3

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
def image_resize(img,name):
    ''' resize image to the patern 640 x 480 or 480 x 640

    Args:
        image(cv2.image): image loaded by cv2.imread.
    Returns:
        image(cv2.image): impanted image

    '''
    dimension = img.shape
    if dimension[0]>dimension[1]:
        newimg = cv2.resize(img, (480, 640))
    elif dimension[1]>dimension[0]:
        newimg = cv2.resize(img, (640, 480))
    newname=name.replace('.jpeg','_resized.jpeg')
    filename=os.path.join('resized', newname)
    cv2.imwrite(os.path.join('resized', newname), newimg)
    return newimg,filename

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
    if ((dimension[0] != 640) and (dimension[0] != 480)) or ((dimension[1] != 640) and (dimension[1] != 480)) :
        print('==============resizing')
        name=os.path.basename(image_path)
        img,image_path=image_resize(img,name)
        print(image_path)
        print(img.shape)
    # Foot images are landscape and others are portrait, so it is possible to define if foot by dimension
    if dimension[0] == 480:
        kind=1
        solidity,aspect_ratio='NA'
    else:
        kind='unknown'
        # impant=impanting(image_path,mask_path)
        impant = impanting(img, mask_path)
        plot_contours(impant)
        contorno = external_contour(impant)
        area=cv2.contourArea(contorno)
        c=contorno
        # solidity
        hull = cv2.convexHull(contorno)
        hull_area = cv2.contourArea(hull)
        solidity = float(area) / hull_area
        # aspect ratio
        x, y, w, h = cv2.boundingRect(contorno)
        aspect_ratio = float(w) / h
        if aspect_ratio>0.60:
            kind='dorso'
            back_pth = r'image_map/skeleton/dorso_costa_model.jpeg'
            front_pth = r'image_map/skeleton/dorso_frente_model.jpeg'
            back = cv2.imread(back_pth,cv2.COLOR_BGR2GRAY)
            front = cv2.imread(front_pth,cv2.COLOR_BGR2GRAY)
            ske=skeleton(impant)
            b1, b2, b3 = shape_match(ske, back)
            b=math.sqrt(b1**2+b2**2+b3**2)
            f1, f2, f3 = shape_match(ske, front)
            f = math.sqrt(f1 ** 2 + f2 ** 2 + f3 ** 2)
            if f<b:
                kind=2
            else:
                kind=3
        elif aspect_ratio<0.60:
            kind='perna'
            back_pth = r'image_map/skeleton/perna_costa_model.jpeg'
            front_pth = r'image_map/skeleton/perna_frente_model.jpeg'
            back = cv2.imread(back_pth,cv2.COLOR_BGR2GRAY)
            front = cv2.imread(front_pth,cv2.COLOR_BGR2GRAY)
            ske=skeleton(impant)
            b1, b2, b3 = shape_match(ske, back)
            b=math.sqrt(b1**2+b2**2+b3**2)
            f1, f2, f3 = shape_match(ske, front)
            f = math.sqrt(f1 ** 2 + f2 ** 2 + f3 ** 2)
            if f<b:
                kind=4
            else:
                kind=5
    return kind

if __name__ == '__main__':
    image_folder=r'../testes/images'
    kind={1:'Foot',2:'Front Upper Body',3: 'Back Upper Body',4: 'Front Legs', 5:'Back Legs'}
    for file in os.listdir(image_folder):
        image_path=os.path.join(image_folder,file)
        k=image_kind(image_path)
        print(file,':',kind[k])
        if k is not 1:
            imp=impanting(cv2.imread(image_path),r'image_map/mask.jpeg')
        else:
            imp=cv2.imread(image_path)
        bk,_=plot_contours(imp)
        cv2.imshow("Image",bk)
        cv2.waitKey(0)