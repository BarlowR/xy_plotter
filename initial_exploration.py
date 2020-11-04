import numpy as np
from PIL import Image, ImageOps
import matplotlib.pyplot as plt 
import cv2



img = cv2.imread('MiniContour.png',0)

new_width = 100
new_height = int(new_width/img.shape[1] * img.shape[0])

dim = (new_width, new_height)

img = cv2.resize(img, dim)


lapx64f = cv2.Laplacian(img,cv2.CV_64F)

canny = cv2.Canny(img, 100, 200)




sq = img/np.max(img)

contrast = sq*sq*sq

contrast[contrast>0.2] = 1
contrast[contrast<=0.2] = 0


plt.subplot(1,3,1), plt.imshow(canny,cmap = 'gray')

plt.subplot(1,3,2), plt.imshow(img,cmap = 'gray')

plt.subplot(1,3,3), plt.imshow(contrast,cmap = 'gray')



plt.show()

