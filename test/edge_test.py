import cv2

#グレースケールで読み込み
gray_img = cv2.imread("IMG_7406.jpg", 0)

#エッジ検出
sobel_img = cv2.Sobel(gray_img, cv2.CV_32F, 1, 1, 1, 5) #sobel
laplacian_img = cv2.Laplacian(gray_img, cv2.CV_32F, 1, 5) #laplacian
canny_img = cv2.Canny(gray_img, 50, 150) #canny

#書き込み
# cv2.imwrite("sobel.jpg", sobel_img)
# cv2.imwrite("laplacian.jpg", laplacian_img)
cv2.imwrite("canny.jpg", canny_img)