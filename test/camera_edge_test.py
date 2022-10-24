#!/usr/bin/env python

import cv2

deviceid=0 # it depends on the order of USB connection. 
capture = cv2.VideoCapture(deviceid)

ret, frame = capture.read()
cv2.imwrite('camera_test.jpg', frame)

gray_img = cv2.imread('camera_test.jpg', 0)

#エッジ検出
sobel_img = cv2.Sobel(gray_img, cv2.CV_32F, 1, 1, 1, 5) #sobel
laplacian_img = cv2.Laplacian(gray_img, cv2.CV_32F, 1, 5) #laplacian
canny_img = cv2.Canny(gray_img, 50, 150) #canny

#書き込み
# cv2.imwrite("sobel.jpg", sobel_img)
# cv2.imwrite("laplacian.jpg", laplacian_img)
cv2.imwrite("canny.jpg", canny_img)