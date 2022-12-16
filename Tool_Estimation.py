import cv2
import numpy as np
import math

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


#一番最初の画像と比べて、工具の貸し借りで工具数が増減しても工具の配列番号を一定にする
#工具が借りられてないところには、ないと分かるデータを挿入する
#   →  工具の最大数は決まっているので予めその数の工具なしデータを挿入した配列を作っておく方がいい
#     →  そこに代入していく感じで行く
def number_juggling(init_data, init_center, now_data, now_center):
    n_tool = ["none"] * len(init_data)
    n_center = ["none"] * len(init_data)
    data = "none"
    
    # 初期画像と現在の画像の中心間距離を格納する変数を0番目で初期化
    min_dist = math.sqrt((init_center[0][0] - now_center[0][0]) ** 2 + (init_center[0][1] - now_center[0][1]) ** 2)
    
    # 現在画像側のループ
    for i in range(len(now_data)):
        now_x = now_center[i][0]
        now_y = now_center[i][1]
        # 初期画像側のループ
        for j in range(len(init_data)):
            init_x = init_center[j][0]
            init_y = init_center[j][1]
            
            # 初期画像と現在画像の中心間距離の計算
            tmp = math.sqrt((init_x - now_x)**2 + (init_y - now_y)**2)
            
            # 今格納されている値よりも小さければ値を更新
            if(min_dist >= tmp):
                min_dist = tmp
                data = j
        
        # 最終的にreturnするデータの格納
        if(data != "none"):
            if(n_tool[data] == "none" and n_center[data] == "none"):
                n_tool[data] = now_data[i]
                n_center[data] = now_center[i]
            else:
                print("[ERROR] データ重複") #データの位置が被ったときにどうしよう、対策が必要
        
        data = "none"
    
    return n_tool, n_center
        
    