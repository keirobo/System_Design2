import cv2

img1 = cv2.imread("test_img02.jpg")
img2 = cv2.imread("test_img12.jpg")

# OBR 特徴量検出器を作成する。
detector = cv2. AKAZE_create()
# detector = cv2. ORB_create()

# 特徴点を検出する。
kp1, desc1 = detector.detectAndCompute(img1, None)
kp2, desc2 = detector.detectAndCompute(img2, None)

# マッチング器を作成する。
bf = cv2.BFMatcher(cv2.NORM_HAMMING)

# マッチングを行う。
matches = bf.knnMatch(desc1, desc2, k=2)

# レシオテストを行う。
good_matches = []
thresh = 0.7
for first, second in matches:
    if first.distance < second.distance * thresh:
        good_matches.append(first)

dist = [m.distance for m in good_matches]
    
ret = sum(dist) / len(dist)
print(ret)
        
# マッチング結果を描画する。
dst = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None)
cv2.imwrite("test.jpg", dst)