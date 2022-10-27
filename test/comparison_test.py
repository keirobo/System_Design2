import cv2
import numpy as np
import random
import sys


if __name__ == '__main__':
    #グレースケールで読み込み
    initial_img = cv2.imread("initial.jpg", 0)

    # 写真撮るとき ============================
    # deviceid=0 # it depends on the order of USB connection. 
    # capture = cv2.VideoCapture(deviceid)

    # ret, gray_img = capture.read()

    #==========================================

    gray_img = cv2.imread("data1.jpg", 0)
    
    #エッジ検出
    sobel_img = cv2.Sobel(gray_img, cv2.CV_32F, 1, 1, 1, 5) #sobel
    laplacian_img = cv2.Laplacian(gray_img, cv2.CV_32F, 1, 5) #laplacian
    canny_img = cv2.Canny(gray_img, 50, 150) #canny

    # 画像をグレースケールで読み込み
    # gray_src = cv2.imread(canny_img, 0)
    # canny_img
    # 前処理（平準化フィルターを適用した場合）
    # 前処理が不要な場合は下記行をコメントアウト
    blur_src = cv2.GaussianBlur(canny_img, (5, 5), 2)
    # 二値変換
    # 前処理を使用しなかった場合は、blur_srcではなくgray_srcに書き換えるする
    mono_src = cv2.threshold(blur_src, 48, 255, cv2.THRESH_BINARY_INV)[1]
    mono_src = 255 - mono_src
    # ラベリング結果書き出し用に二値画像をカラー変換
    color_src01 = cv2.cvtColor(mono_src, cv2.COLOR_GRAY2BGR)
    color_src02 = cv2.cvtColor(mono_src, cv2.COLOR_GRAY2BGR)
    # ラベリング処理
    label = cv2.connectedComponentsWithStats(mono_src)
    # オブジェクト情報を項目別に抽出
    n = label[0] - 1
    tmp_data = np.delete(label[2], 0, 0)
    tmp_center = np.delete(label[3], 0, 0)
    data = []
    center = []
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

        cv2.rectangle(color_src01, (x0, y0), (x1, y1), (0, 0, 255))
        # # 各オブジェクトのラベル番号と面積に黄文字で表示
        # cv2.putText(color_src01, "ID: " +str(i + 1), (x1 - 20, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        cv2.putText(color_src01, "S: " +str(data[i][4]), (x1 - 20, y1 + 15), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        # # 各オブジェクトの重心座標を黄文字で表示
        cv2.putText(color_src01, "X: " + str(int(center[i][0])), (x1 - 20, y1 + 30), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))
        cv2.putText(color_src01, "Y: " + str(int(center[i][1])), (x1 - 20, y1 + 45), cv2.FONT_HERSHEY_PLAIN, 1, (0, 255, 255))

    # 結果の表示
    cv2.imwrite("test_img.jpg", color_src01)