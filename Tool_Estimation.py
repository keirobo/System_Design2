import cv2
import numpy as np
import math
import random
import Spreadsheet as SS
import SlackBot as SB
import copy

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

def img_processing_debug(img):
  color_src01 = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
  
  label = cv2.connectedComponentsWithStats(img)
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

    if abs(ret) < 10 :
      return ret, True
    else:
      return ret, False
  else:
    return False


def maching(img1, img2):
  # OBR 特徴量検出器を作成する。
  detector = cv2.AKAZE_create()
  
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

  # dst = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None)
  # cv2.imwrite("test.jpg", dst)
      
  ret = sum(dist) / len(dist)
  print("ret:" + str(ret))
          
  # マッチング結果を描画する。
  # dst = cv2.drawMatches(img1, kp1, img2, kp2, good_matches, None)
  # cv2.imwrite("test.jpg", dst)

  return ret


#一番最初の画像と比べて、工具の貸し借りで工具数が増減しても工具の配列番号を一定にする
def number_sequencing(init_data, init_center, now_data, now_center):
  n_tool = ["none"] * len(init_data)
  n_center = ["none"] * len(init_data)
  data = "none"
  
  # 現在画像側のループ
  for i in range(len(now_data)):
    now_x = now_center[i][0]
    now_y = now_center[i][1]
    # 初期画像と現在の画像の中心間距離を格納する変数を0番目で初期化
    min_dist = math.sqrt((init_center[i][0] - now_center[0][0]) ** 2 + (init_center[i][1] - now_center[0][1]) ** 2)
    # 初期画像側のループ
    for j in range(len(init_data)):
      init_x = init_center[j][0]
      init_y = init_center[j][1]
      # print("i:" + str(i) + "j:" + str(j))
      # print("x:"+ str(now_x) + ", y:" + str(now_y))
      # print("x:"+ str(init_x) + ", y:" + str(init_y))
        
      # 初期画像と現在画像の中心間距離の計算
      tmp_dist = math.sqrt((init_x - now_x)**2 + (init_y - now_y)**2)

      # print("i:" + str(i) + ", j:"+ str(j) + ", tmp_dist:" + str(tmp_dist) + ", min_dist:" + str(min_dist))
      
      # 今格納されている値よりも小さければ値を更新
      if min_dist >= tmp_dist:
        data = j
        min_dist = tmp_dist
      
      # print("mindist:" + str(min_dist))
      # print("data:" + str(data))
      
    # 最終的にreturnするデータの格納
    if data != "none":
      if n_tool[data] == "none" and n_center[data] == "none":
        n_tool[data] = now_data[i]
        n_center[data] = now_center[i]
      else:
        print("[ERROR/TE] データ重複") #データの位置が被ったときにどうしよう、対策が必要      
    
    data = "none"
  
  return n_tool, n_center


def comparison(id, init_tool, past_tool, past_center, now_tool, now_center, time):
    
  for i in range(len(past_tool)):
    # 返却処理
    if((np.isin(['none'], past_center[i]) == True) and (np.isin(['none'], now_center[i]) != True)):
      print("返却処理")
      ret = maching(init_tool[i], now_tool[i])
      if(ret <= 60):
        # return_tool(id, i, past_tool[i], now_tool[i])
        SS.write_return(id, i, time)
      else:
        different_tool(i)

    # 貸し出し処理  
    elif((np.isin(['none'], past_center[i]) != True) and (np.isin(['none'], now_center[i]) == True)):
      print("貸し出し処理")
      SS.write_lend(id, i, time)
    
    # 変化なし
    else:
      if(np.isin(['none'], past_center[i]) != True) and (np.isin(['none'], now_center[i]) != True):
        ret = maching(past_tool[i], now_tool[i])
        #違う工具と判別された場合はランダムに指定して確認をお願いする
        if(ret > 60):
          different_tool(i)
        else:
          print("変化なし")
      else:
        print("変化なし")


def different_tool(tool_id):
  print("工具が違う")

  max_id = SS.get_max_id()
  rand_id = random.randint(1, max_id)
  print("rand_id:" + str(rand_id))
  slack_id = SS.get_slack_id(rand_id)

  name = SS.get_name(rand_id)
  tool_name = SS.get_tool_name(tool_id)
  message = "工具ID [" + str(tool_id) + "]:" + tool_name + "が違う工具になっています" + name + "さんが代表して確認をお願いします"
  SB.write_DM(slack_id, message)

def past_data_acquisition(init_tool, init_center):
  tool_id, tool_flag = SS.get_lend_info()
  past_tool = copy.copy(init_tool)
  past_center = copy.copy(init_center)
  
  for i in range(len(init_tool)): #工具IDを移動
    for j in range(len(tool_id)-1, 0, -1): #取得したtool_idを移動(後ろから)
      if (str(i+1) == tool_id[j]) and (tool_flag[j] == str(1)):
        past_tool[i] = "none"
        past_center[i] = "none"
        break
      elif (str(i+1) == tool_id[j]) and (tool_flag[j] == str(0)):
        past_tool[i] = init_tool[i]
        past_center[i] = init_center[i]
        break
  
  return past_tool, past_center
