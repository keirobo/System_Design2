import cv2
import numpy as np
import random
import sys

def img_processing(img):
    #エッジ検出
    canny_img = cv2.Canny(img, 60, 141) #canny
    # 画像をグレースケールで読み込み
    
    # 前処理（平準化フィルターを適用した場合）
    # 前処理が不要な場合は下記行をコメントアウト
    blur_src = cv2.GaussianBlur(canny_img, (5, 5), 3)
    # 二値変換
    # 前処理を使用しなかった場合は、blur_srcではなくgray_srcに書き換えるする
    mono_src = cv2.threshold(blur_src, 48, 255, cv2.THRESH_BINARY_INV)[1]
    # ラベリング結果書き出し用に二値画像をカラー変換
    
    th, src_th = cv2.threshold(mono_src, 220, 255, cv2.THRESH_BINARY_INV)
     
    # Copy the thresholded image.
    im_floodfill = src_th.copy()
     
    # Mask used to flood filling.
    # Notice the size needs to be 2 pixels than the image.
    h, w = src_th.shape[:2]
    mask = np.zeros((h+2, w+2), np.uint8)
     
    # Floodfill from point (0, 0)
    cv2.floodFill(im_floodfill, mask, (10,10), 255)
     
    # Invert floodfilled image
    im_floodfill_inv = cv2.bitwise_not(im_floodfill)
     
    # Combine the two images to get the foreground.
    src_out = src_th | im_floodfill_inv
    
    color_src01 = cv2.cvtColor(src_out, cv2.COLOR_GRAY2BGR)
    # color_src02 = cv2.cvtColor(src_out, cv2.COLOR_GRAY2BGR)
    
    # cv2.imwrite("data_initial.jpg", color_src02)
    
    label = cv2.connectedComponentsWithStats(src_out)
    # オブジェクト情報を項目別に抽出
    n = label[0] - 1
    tmp_data = np.delete(label[2], 0, 0)
    tmp_center = np.delete(label[3], 0, 0)
    data = []
    center = []
    tool = []
    j = 0
    # オブジェクト情報を利用してラベリング結果を画面に表示
    for i in range(n):
        if tmp_data[i][4] > 2000: # 小さい判定を無視
            data.append(tmp_data[i])
            center.append(tmp_center[i])
            j += 1
    
    for i in range(j):
        # 各オブジェクトの外接矩形を赤枠で表示
        x0 = data[i][0]
        y0 = data[i][1]
        x1 = data[i][0] + data[i][2]
        y1 = data[i][1] + data[i][3]
      
        tool.append(color_src01[y0 : y1, x0: x1])
      
        # cv2.rectangle(color_src01, (x0, y0), (x1, y1), (0, 0, 255))
        # # # 各オブジェクトのラベル番号と面積に黄文字で表示
        # # cv2.putText(color_src01, "ID: " +str(i + 1), (x1 - 20, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        # cv2.putText(color_src01, "S: " +str(data[i][4]), (x1 - 20, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        # # # 各オブジェクトの重心座標を黄文字で表示
        # cv2.putText(color_src01, "X: " + str(int(center[i][0])), (x1 - 20, y1 + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        # cv2.putText(color_src01, "Y: " + str(int(center[i][1])), (x1 - 20, y1 + 45), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))

    return color_src01, tool, center

def estimation(i_tool, i_x, i_y, n_tool, n_x, n_y):
    if abs(i_x - n_x) < 100 and abs(i_y - n_y) < 100:
        ret = maching(i_tool, n_tool)

        if(abs(ret) < 20):
            return ret, True
        else:
            return ret, False
    else:
        return False

def maching(i_img, n_img):
    target_img = i_img
    bf = cv2.BFMatcher(cv2.NORM_HAMMING)
    # detector = cv2.ORB_create()
    detector = cv2.AKAZE_create()
    (target_kp, target_des) = detector.detectAndCompute(target_img, None)
    
    try:
        comparing_img = n_img
        (comparing_kp, comparing_des) = detector.detectAndCompute(comparing_img, None)
        matches = bf.match(target_des, comparing_des)
        dist = [m.distance for m in matches]
        ret = sum(dist) / len(dist)
    except cv2.error:
        ret = 100000

    print(ret)
    return ret

if __name__ == '__main__':
    #グレースケールで読み込み
    initial = cv2.imread("data0.jpg", 0)

    init_img, init_tool, init_center = img_processing(initial)
    
    cv2.imwrite("test_img00.jpg", init_img)
    cv2.imwrite("test_img01.jpg", init_tool[0])
    cv2.imwrite("test_img02.jpg", init_tool[1])


    # 写真撮るとき ============================
    # deviceid=0 # it depends on the order of USB connection. 
    # capture = cv2.VideoCapture(deviceid)

    # ret, gray_img = capture.read()

    #==========================================

    gray_img = cv2.imread("data1.jpg", 0)

    now_img, now_tool, now_center = img_processing(gray_img)

    cv2.imwrite("test_img10.jpg", now_img)
    cv2.imwrite("test_img11.jpg", now_tool[0])
    cv2.imwrite("test_img12.jpg", now_tool[1])

    if len(now_tool) > len(init_tool): num = len(now_tool)
    else: num = len(init_tool)
    
    for i in range(num):
        print("[", i, "]:", estimation(init_tool[i], init_center[i][0], init_center[i][1], now_tool[i], now_center[i][0], now_center[i][1]))

    # 結果の表示
    # cv2.imwrite("test_img.jpg", estimation(gray_img))