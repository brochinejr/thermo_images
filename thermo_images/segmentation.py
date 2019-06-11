import classification as cls
from PIL import Image
import os
import cv2
import imutils
import numpy as np
from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.segmentation import watershed
from skimage.segmentation import mark_boundaries
import matplotlib



def fill_contour(img,contours):
    stencil = np.zeros(img.shape).astype(img.dtype)
    color = [255, 255, 255]
    cv2.fillPoly(stencil, contours, color)
    result = cv2.bitwise_and(img, stencil)
    return result


def watershed_easy(img):
    print("test")
    gradient = sobel(rgb2gray(img))
    segments_watershed = watershed(gradient, markers=150, compactness=0.001)
    temp=mark_boundaries(img, segments_watershed)
    matplotlib.image.imsave('temp/temp.jpeg', temp)
    watershed_res = cv2.imread('./temp/temp.jpeg')
    return watershed_res

def extremes(image,c):

    new_image=image.copy()
    extLeft = tuple(c[c[:, :, 0].argmin()][0])
    extRight = tuple(c[c[:, :, 0].argmax()][0])
    extTop = tuple(c[c[:, :, 1].argmin()][0])
    extBot = tuple(c[c[:, :, 1].argmax()][0])
    points=[extLeft,extRight,extTop,extBot]

    cv2.circle(new_image, extLeft , 8, (255, 0, 0), -1)
    cv2.circle(new_image, extRight, 8, (255, 0, 0), -1)
    cv2.circle(new_image, extTop  , 8, (255, 0, 0), -1)
    cv2.circle(new_image, extBot  , 8, (255, 0, 0), -1)

    return new_image,points


def alignImages(im1, im2):

    MAX_FEATURES = 500
    GOOD_MATCH_PERCENT = 0.15

    # Detect ORB features and compute descriptors.
    orb = cv2.ORB_create(MAX_FEATURES)
    keypoints1, descriptors1 = orb.detectAndCompute(im1, None)
    keypoints2, descriptors2 = orb.detectAndCompute(im2, None)

    # Match features.
    matcher = cv2.DescriptorMatcher_create(cv2.DESCRIPTOR_MATCHER_BRUTEFORCE_HAMMING)
    matches = matcher.match(descriptors1, descriptors2, None)

    # Sort matches by score
    matches.sort(key=lambda x: x.distance, reverse=False)

    # Remove not so good matches
    numGoodMatches = int(len(matches) * GOOD_MATCH_PERCENT)
    matches = matches[:numGoodMatches]

    # Draw top matches
    imMatches = cv2.drawMatches(im1, keypoints1, im2, keypoints2, matches, None)
    cv2.imwrite("matches.jpg", imMatches)

    # Extract location of good matches
    points1 = np.zeros((len(matches), 2), dtype=np.float32)
    points2 = np.zeros((len(matches), 2), dtype=np.float32)

    for i, match in enumerate(matches):
        points1[i, :] = keypoints1[match.queryIdx].pt
        points2[i, :] = keypoints2[match.trainIdx].pt

    # Find homography
    h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)

    # Use homography
    height, width, channels = im2.shape
    im1Reg = cv2.warpPerspective(im1, h, (width, height))

    return im1Reg, h


def convert_to_cv2(points):
    pts = np.array(points)
    pts = np.float32(pts[:, np.newaxis, :])
    return pts

# ************ general definitions
mask=r'/home/ccjunio/PycharmProjects/thermo_images/thermo_images/image_map/mask.jpeg'
kind={1:'Foot',2:'Front Upper Body',3: 'Back Upper Body',4: 'Front Legs', 5:'Back Legs'}

# ************ dorso costa image

image_path=r'/home/ccjunio/PycharmProjects/thermo_images/testes/images/dorso_costa00.jpeg'
k=cls.image_kind(image_path)
print(kind[k])

img=cv2.imread(image_path)
imp=cls.impanting(img,mask)
contour,c=cls.plot_contours(imp)


teste_fill=fill_contour(img,[c])
cv2.imshow("Image", teste_fill)
cv2.waitKey(0)
#
# ************ map dorso costa image

map_path=r'/home/ccjunio/PycharmProjects/thermo_images/thermo_images/image_map/maps/upper_body_b_resized_p.jpeg'
map=cv2.imread(map_path)
contour_map,cmap=cls.plot_contours(map)

# cv2.imshow("Image", contour_map)
# cv2.waitKey(0)

# numpy_horizontal_concat = np.concatenate((contour, contour_map), axis=1)
# cv2.imshow('Numpy Horizontal Concat', numpy_horizontal_concat)
# cv2.waitKey(0)

# edges = cv2.Canny(map,100,200)
# cv2.imshow("Edges",edges)
# cv2.waitKey(0)

map_extreme,p_map=extremes(contour_map,cmap)
extreme,p=extremes(contour,c)

print(p[2][0])
print(p_map[2][0])
numpy_horizontal_concat = np.concatenate((contour_map, contour), axis=1)
# cv2.imshow('Numpy Horizontal Concat', numpy_horizontal_concat)
# cv2.waitKey(0)


watershed_simple=watershed_easy(img)
fill=fill_contour(watershed_simple,[c])
cv2.imshow("Image", fill)
cv2.waitKey(0)

watershed_map=watershed_easy(map)
fill_map=fill_contour(watershed_map,[cmap])
cv2.imshow("Image", fill_map)
cv2.waitKey(0)


# points1=convert_to_cv2(p_map)
# points2=convert_to_cv2(p)
# #
# h, mask = cv2.findHomography(points1, points2, cv2.RANSAC)
#
# # # Use homography
# height, width, channels = img.shape
# mapReg = cv2.warpPerspective(contour_map, h, (width, height))
#
# cv2.imshow("homography",mapReg)
# cv2.waitKey(0)
# print(mapReg.shape)
#
# print(edges.shape)
# print(img.shape)
# print(contours.shape)
# added_image = cv2.addWeighted(contours,0.4,edges,0.1,0)
# cv2.imshow("teste",added_image)
# cv2.waitKey(0)