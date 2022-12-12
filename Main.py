import Tool_Estimation as TE
import SlackBot as SB
import Spreadsheet as SS
import configparser
import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
import time
import joblib

def main():

  flag_once  = 0
  mode = False #False返却  #True貸し出し
  
  cap = cv.VideoCapture(0)
  #出力ウィンドウの設定
  # cap.set(3,640)
  # cap.set(3,480)

  config = configparser.ConfigParser()
  
  #Slackのトークンとスプレッドシートのキーを取得
  config.read("config.ini", encoding="utf-8")
  Slack_Token = config['Slack']['token']
  key = config['Spreadsheet']['Key']

  print(key)

  # 工具の初期データを読み込み
  init_img, init_tool, init_center = joblib.load(open("initial_data.txt", 'rb'))

  cv.imwrite("test_img00.jpg", init_img)
  cv.imwrite("test_img01.jpg", init_tool[0])
  cv.imwrite("test_img02.jpg", init_tool[1])

  #スプレッドシートのキーを使用してスプレッドシートを開く
  try:
    SS.init(key)
  except TimeoutError:
    print("ERROR:スプレッドシートに接続できません。終了しています...")

  while(True):
    # print("main")

    ret, frame = cap.read()
    #フレームが正しく読み取られた場合、retはTrue
    if not ret:
        print("ERROR:フレームは受信できません。終了しています...")
        break

    #QRコード読み込み処理
    codes = decode(frame)
    if len(codes) > 0 and flag_once == 0:
      flag_once = 1
      output = codes[0][0].decode('utf-8', 'ignore')
      print(output)

      #読み込み成功したら
      if 'output' != None:
        #画像撮影処理
        time.sleep(1.5)
        
        ret, frame = cap.read()
        cv.imwrite('camera_test.jpg', frame)
        
        #デバック用(不要時はコメントアウト)
        frame = cv.imread("now.jpg")
        
        #工具判別処理
        
        print("Now processing...")
        #グレースケールで読み込み    
        gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
        
        #画像のエッジ検出を行い、エッジの中を埋める
        now_img, tmp_tool, tmp_center = TE.img_processing(gray_img)
        
        #デバック用に画像出力(不要時はコメントアウト)
        cv.imwrite("test_img10.jpg", now_img)
        cv.imwrite("test_img11.jpg", tmp_tool[0])
        # cv.imwrite("test_img12.jpg", tmp_tool[1])

        print("process complete")
        print("現在の工具数:" + str(len(tmp_tool)))

        # 工具の順番を社期の順番と合わせる
        now_tool, now_center = TE.number_juggling(init_tool, init_center, tmp_tool, tmp_center)
    
        # if len(now_tool) > len(init_tool): num = len(now_tool)
        # else: num = len(init_tool)
        
        # for i in range(num):
        #     print("[", i, "]:", TE.estimation(init_tool[i], init_center[i][0], init_center[i][1], now_tool[i], now_center[i][0], now_center[i][1]))       

        #貸し出し OR 返却モード選択処理
        

        #スプレッドシート書き込み処理
        

        # user_id = SS.get_user_id(output)

        # if(str(user_id).startswith('None') == False): SB.write(Slack_Token, user_id)
    else:
      flag_once = 0
      # print("QRコード読み込みなし")


if __name__ == "__main__":
  main()