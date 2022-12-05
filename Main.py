import Tool_Estimation as TE
import SlackBot as SB
import Spreadsheet as SS
import configparser
import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode
import time

def main():

  flag_once  = 0
  
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

  #スプレッドシートのキーを使用してスプレッドシートを開く
  try:
    SS.init(key)
  except TimeoutError:
    print("Error")

  while(True):
    # print("main")

    ret, frame = cap.read()
    #フレームが正しく読み取られた場合、retはTrue
    if not ret:
        print("フレームは受信できません。終了しています...")
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
        
        #工具判別処理
        

        #貸し出し OR 返却モード選択処理
        

        #スプレッドシート書き込み処理
        

        # user_id = SS.get_user_id(output)

        # if(str(user_id).startswith('None') == False): SB.write(Slack_Token, user_id)
    else:
      flag_once = 0
      # print("QRコード読み込みなし")

if __name__ == "__main__":
  main()