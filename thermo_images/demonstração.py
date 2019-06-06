import classification as classification
import cv2

img=r'/home/ccjunio/PycharmProjects/thermo_images/testes/new_images/im1.jpeg'
# img=r'/home/ccjunio/PycharmProjects/thermo_images/testes/new_images/im2.jpeg'
k=classification.image_kind(img)
print(k)
imp=classification.impanting(cv2.imread(r'/home/ccjunio/PycharmProjects/thermo_images/thermo_images/resized/im1_resized.jpeg'),r'image_map/mask.jpeg')
bk = classification.plot_contours(imp)
cv2.imshow("Image", bk)
cv2.waitKey(0)