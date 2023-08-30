import cv2
import numpy as np
import matplotlib.pyplot as plt


img_path = "data/遗漏项/二十六册/54.jpg"
img = cv2.imdecode(np.fromfile(img_path, dtype=np.uint8), cv2.IMREAD_COLOR)


"""图像腐蚀"""
kernel = np.ones((3,3),np.uint8)
erosion = cv2.erode(img,)
dilation = cv2.dilate(img,kernel)
dilation = cv2.bilateralFilter(dilation,55,100,100)


gauss = cv2.GaussianBlur(img,(55,55),0,0)
bilateral = cv2.bilateralFilter(img,55,100,100)


cv2.imshow("gauss",gauss)

cv2.waitKey(200)
cv2.imshow("img",bilateral)
cv2.waitKey(200)
cv2.imshow("dilation",dilation)
cv2.waitKey()