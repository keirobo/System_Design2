import Tool_Estimation as TE
import SlackBot as SB
import Spreadsheet as SS
import configparser
import cv2 as cv
import numpy as np
# from pyzbar.pyzbar import decode
import time
import joblib
import datetime

def main():

  flag_once  = 0
  mode = False #False返却  #True貸し出し
  
  print("カメラ起動中...")
  cap = cv.VideoCapture(0)
  detector = cv.QRCodeDetector()
  #出力ウィンドウの設定
  # cap.set(3,640)
  # cap.set(3,480)
  print("カメラ起動完了")
  
  print("各種初期データを取得中...")
  config = configparser.ConfigParser()
  
  #Slackのトークンとスプレッドシートのキーを取得
  config.read("config.ini", encoding="utf-8")
  slack_token = config['Slack']['token']
  key = config['Spreadsheet']['Key']

  print(key)
  print(slack_token)

  # 工具の初期データを読み込み
  init_img, init_tool, init_center = joblib.load(open("initial_data.txt", 'rb'))
  
  past_img = init_img
  past_tool = init_tool
  past_center = init_center
  
  # print(past_center)
  # print(past_img)
  # print(init_img)

  print("データ取得完了")

  # cv.imwrite("test_img00.jpg", init_img)
  # cv.imwrite("test_img01.jpg", init_tool[0])
  # cv.imwrite("test_img02.jpg", init_tool[1])

  # cv.imwrite("test_img100.jpg", past_img)
  # cv.imwrite("test_img101.jpg", past_tool[0])
  # cv.imwrite("test_img102.jpg", past_tool[1])

  #スプレッドシートのキーを使用してスプレッドシートを開く
  print("スプレッドシートとSlackBotの設定中...")
  try:
    SS.init(key)
    SB.init(slack_token)
    print("スプレッドシートとSlackBotの設定完了")
  except TimeoutError:
    print("[ERROR/SS] スプレッドシートに接続できません。終了しています...")
  
  print("QRコードをかざしてください") 

  while(True):
    # print("main")

    ret, frame = cap.read()
    #フレームが正しく読み取られた場合、retはTrue
    if not ret:
        print("[ERROR] フレームは受信できません。終了しています...")
        break

    #QRコード読み込み処理
    # codes = decode(frame)
    try:
      output = detector.detectAndDecode(frame)
  
      if output[0] != "" and flag_once == 0:
        flag_once = 1
        last_time = datetime.datetime.now()
        print(last_time.strftime('%Y-%m-%d %H:%M:%S') + "  id:" + str(output[0]))

        #読み込み成功したら
        if 'output' != None:
          #画像撮影処理
          time.sleep(1.5)
          
          ret, frame = cap.read()
          cv.imwrite('camera_test.jpg', frame)
          
          #デバック用(不要時はコメントアウト)
          frame = cv.imread("now.jpg")
          
          #工具判別処理
          
          print("処理中")
          #グレースケールで読み込み    
          gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
          
          #画像のエッジ検出を行い、エッジの中を埋める
          now_img, tmp_tool, tmp_center = TE.img_processing(gray_img)
          
          #デバック用に画像出力(不要時はコメントアウト)
          # cv.imwrite("test_img10.jpg", now_img)
          # cv.imwrite("test_img11.jpg", tmp_tool[0])
          # cv.imwrite("test_img12.jpg", tmp_tool[1])
  
          print("現在の工具数:" + str(len(tmp_tool)))
  
          # 今の工具の順番を初期の画像の順番と合わせる
          now_tool, now_center = TE.number_sequencing(init_tool, init_center, tmp_tool, tmp_center)
  
          print(now_center)
  
          # 前回の工具の画像と順番に比較していって
          # 無くなっていたら貸し出し関数、戻っていたら返却関数を呼び出す
          TE.comparison(output[0], past_tool, past_center, now_tool, now_center, last_time)
          
          #今回の値を次回に引き継ぎ
          past_tool = now_tool
          past_center = now_center
  
          print("処理完了")
          print("QRコードをかざしてください")
      else:
        flag_once = 0
        # print("QRコード読み込みなし")
    except cv.error:  #QRコード周りでエラーがちょくちょく出るのでとりあえずこれで対応
      print("error出たよ")


if __name__ == "__main__":
  main()