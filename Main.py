import Tool_Estimation as TE
import SlackBot as SB
import Spreadsheet as SS
import configparser
import cv2 as cv
import numpy as np
import time
import joblib
import datetime
import random

INTERVAL = 10 #[minute]
notice_time = [["12:00", "16:20"], [False, False]] #一旦工具の返却を促す時間の設定(通知回数の増減は配列の要素数)

def main():

  flag_once  = 0
  last_time = datetime.datetime.now()
  
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

  print("データ取得完了")

  cv.imwrite("test_img00.jpg", init_img)
  cv.imwrite("test_img01.jpg", init_tool[0])
  cv.imwrite("test_img02.jpg", init_tool[1])

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

    judge_notice()

    #QRコード読み込み処理
    try:
      output = detector.detectAndDecode(frame)
  
      if (output[0] != "" and flag_once == 0) or time_comparison(last_time):
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
          # frame = cv.imread("initial.jpg")
          # 0:initial 1:ペンチなし 2:ドライバーとラジオペンチなし 3:やすりとペンチとはさみなし 4:ドライバーなし 5:ペンチとラジオペンチとドライバーなし
          rand_num = random.randint(0, 5)
          frame = cv.imread("now_images/now" + str(rand_num) + ".jpg")
          print("rand_num:" + str(rand_num))
          
          #工具判別処理
          
          print("処理中")
          #グレースケールで読み込み    
          gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
          
          #画像のエッジ検出を行い、エッジの中を埋める
          now_img, tmp_tool, tmp_center = TE.img_processing_debug(gray_img)
          
          #デバック用に画像出力(不要時はコメントアウト) 
          # cv.imwrite("test_img10.jpg", now_img)
          # cv.imwrite("test_img11.jpg", tmp_tool[0])
          # # cv.imwrite("test_img12.jpg", tmp_tool[1])
  
          print("現在の工具数:" + str(len(tmp_tool)))
  
          # 今の工具の順番を初期の画像の順番と合わせる
          now_tool, now_center = TE.number_sequencing(init_tool, init_center, tmp_tool, tmp_center)

          cv.imwrite("test_img10.jpg", now_img)
          #デバク用
          for i in range(len(now_tool)):
            if(now_tool[i] != "none"):
              cv.imwrite("test_img1"+str(i+1)+".jpg", now_tool[i])
  
          print(now_center)
  
          # 前回の工具の画像と順番に比較していって
          # 無くなっていたら貸し出し関数、戻っていたら返却関数を呼び出す
          TE.comparison(output[0], init_tool, past_tool, past_center, now_tool, now_center, last_time)
          
          #今回の値を次回に引き継ぎ
          past_tool = now_tool
          past_center = now_center
  
          print("処理完了")
          print("QRコードをかざしてください")
      else:
        flag_once = 0

    except Exception as e:  #QRコード周りでエラーがちょくちょく出るのでとりあえずこれで対応
      print("error出たよ")
      print('=== エラー内容 ===')
      print('type:' + str(type(e)))
      print('args:' + str(e.args))
      print('e自身:' + str(e))
      print('=================')
      print("QRコードをかざしてください")


def time_comparison(last_time):
  now_time = datetime.datetime.now()

  if now_time > last_time + datetime.timedelta(minutes = INTERVAL): return True
  else: return False

def judge_notice():
  now_time = datetime.datetime.now()

  for i in range(len(notice_time[0])):
    divided_time = notice_time[0][i].split(':')
    comparison_time = now_time.replace(hour=int(divided_time[0]), minute=int(divided_time[1]), second=0, microsecond=0)

    if now_time > comparison_time: # 指定時間を過ぎた
      minute = now_time.minute - comparison_time.minute
      hour = now_time.hour - comparison_time.hour

      if (hour == 0) and (minute <= 10) and (notice_time[1][i] == False): # 指定時間+10分以内
        print("通知")
        SB.write_channel("#random", "時間です。使用していない工具は一旦返却しましょう!")
        
        notice_time[1][i] = True
        if len(notice_time[0])-1 >= i+1:
          notice_time[1][i+1] = False
        else:
          notice_time[1][0] = False


if __name__ == "__main__":
  main()