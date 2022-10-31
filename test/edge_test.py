import cv2

#グレースケールで読み込み
# gray_img = cv2.imread("initial.jpg", 0)
    
# #エッジ検出
# sobel_img = cv2.Sobel(gray_img, cv2.CV_32F, 1, 1, 1, 5) #sobel
# laplacian_img = cv2.Laplacian(gray_img, cv2.CV_32F, 1, 5) #laplacian
# canny_img = cv2.Canny(gray_img, 50, 150) #canny

# #書き込み
# # cv2.imwrite("sobel.jpg", sobel_img)
# # cv2.imwrite("laplacian.jpg", laplacian_img)
# cv2.imwrite("canny.jpg", canny_img)

gray_img = cv2.imread("initial.jpg", 0)
    
#エッジ検出
sobel_img = cv2.Sobel(gray_img, cv2.CV_32F, 1, 1, 1, 5) #sobel
laplacian_img = cv2.Laplacian(gray_img, cv2.CV_32F, 1, 5) #laplacian
canny_img = cv2.Canny(gray_img, 35, 140) #canny
# 画像をグレースケールで読み込み
# gray_src = cv2.imread(canny_img, 0)
canny_img
# 前処理（平準化フィルターを適用した場合）
# 前処理が不要な場合は下記行をコメントアウト
blur_src = cv2.GaussianBlur(canny_img, (5, 5), 2)
# 二値変換
# 前処理を使用しなかった場合は、blur_srcではなくgray_srcに書き換えるする
mono_src = cv2.threshold(blur_src, 48, 255, cv2.THRESH_BINARY_INV)[1]
# mono_src = 255 - mono_src
# ラベリング結果書き出し用に二値画像をカラー変換
color_src01 = cv2.cvtColor(mono_src, cv2.COLOR_GRAY2BGR)

cv2.imwrite("canny.jpg", color_src01)