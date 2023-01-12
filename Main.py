import Tool_Estimation as TE
import SlackBot as SB
import Spreadsheet as SS
import configparser
import cv2 as cv
import time
import joblib
import datetime
import tkinter
import tkinter.ttk as ttk
import sys
# import keyboard
from PIL import Image, ImageTk
import threading
#デバック用
import random

INTERVAL = 10 #[minute]
notice_time = [["12:00", "16:20"], [False, False]] #一旦工具の返却を促す時間の設定(通知回数の増減は配列の要素数)
values = []

def init():
  flag_once = 0

  last_time = datetime.datetime.now()
  
  print("カメラ起動中...")
  cap = cv.VideoCapture(0)
  detector = cv.QRCodeDetector()
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

  print("データ取得完了")

  #スプレッドシートのキーを使用してスプレッドシートを開く
  print("スプレッドシートとSlackBotの設定中...")
  try:
    SS.init(key)
    SB.init(slack_token)
    print("スプレッドシートとSlackBotの設定完了")
  except TimeoutError:
    print("[ERROR/SS] スプレッドシートに接続できません。終了しています...")

  # 前回起動時のデータをスプレッドシートから取得
  past_tool, past_center = TE.past_data_acquisition(init_tool, init_center)

  print(past_center)
  print("QRコードをかざしてください") 

  return last_time, cap, detector, init_img, init_tool, init_center, past_img, past_tool, past_center, flag_once


def main(last_time, cap, detector, init_tool, init_center, past_tool, past_center, flag_once):
  ret, frame = cap.read()

  if flag_once == 0:
    update_main_canvas(ret, frame)
  
  #フレームが正しく読み取られた場合、retはTrue
  if not ret:
      print("[ERROR] フレームは受信できません。終了しています...")

  judge_notice()
  
  try:
    #QRコード読み込み処理
    output = detector.detectAndDecode(frame)
  
    if (output[0] != "" and flag_once == 0) or time_comparison(last_time):
      # cam1_frame.tkraise()
      last_time = datetime.datetime.now()
      print(last_time.strftime('%Y-%m-%d %H:%M:%S') + "  id:" + str(output[0]))
      flag_once = 1
      #読み込み成功したら
      if 'output' != None:
        print("処理")
        thread = threading.Thread(target=processing, args=(output[0], last_time, cap, frame, init_tool, init_center, past_tool, past_center, flag_once))
        thread.start()
  
    if len(values) > 0:
      main_frame.tkraise()
      flag_once = values[0]
      past_tool = values[1]
      past_center = values[2]
  
      values.clear()
  except:
    print("error1")

  root.after(1,main, last_time, cap, detector, init_tool, init_center, past_tool, past_center, flag_once)


def processing(id, last_time, cap, frame, init_tool, init_center, past_tool, past_center, flag_once):
  #画像撮影処理
  time.sleep(1)
  
  ret, frame = cap.read()
  # cv.imwrite('camera_test.jpg', frame)

  #デバック用(不要時はコメントアウト)
  # frame = cv.imread("initial.jpg")
  # 0:initial 1:ペンチなし 2:ドライバーとラジオペンチなし 3:やすりとペンチとはさみなし 4:ドライバーなし 5:ペンチとラジオペンチとドライバーなし
  rand_num = random.randint(0, 5)
  frame = cv.imread("now_images/now" + str(rand_num) + ".jpg")
  print("rand_num:" + str(rand_num))

  # update_canvas(ret, frame)

  # time.sleep(0.5)

  # cam2_frame.tkraise()
  
  #工具判別処理
  
  print("処理中")
  #グレースケールで読み込み    
  gray_img = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
  
  #画像のエッジ検出を行い、エッジの中を埋める
  now_img, tmp_tool, tmp_center = TE.img_processing_debug(gray_img) #デバック用
  # now_img, tmp_tool, tmp_center = TE.img_processing(gray_img)
  update_main_canvas(ret, now_img)

  time.sleep(1)

  print("現在の工具数:" + str(len(tmp_tool)))

  cam1_frame.tkraise()

  # 今の工具の順番を初期の画像の順番と合わせる
  now_tool, now_center = TE.number_sequencing(init_tool, init_center, tmp_tool, tmp_center)
  # cv.imwrite("test_img10.jpg", now_img)
  #デバク用
  # for i in range(len(now_tool)):
  #   if(now_tool[i] != "none"):
  #     cv.imwrite("test_img1"+str(i+1)+".jpg", now_tool[i])

  print(now_center)

  # 前回の工具の画像と順番に比較していって
  # 無くなっていたら貸し出し関数、戻っていたら返却関数を呼び出す
  TE.comparison(id, init_tool, past_tool, past_center, now_tool, now_center, last_time)
  
  #今回の値を次回に引き継ぎ
  past_tool = now_tool
  past_center = now_center

  print("処理完了")
  print("QRコードをかざしてください")

  flag_once = 0

  # return flag_once, past_tool, past_center
  values.append(flag_once)
  values.append(past_tool)
  values.append(past_center)

  # except Exception as e:  #QRコード周りでエラーがちょくちょく出るのでとりあえずこれで対応
  #   print("error出たよ")
  #   print('=== エラー内容 ===')
  #   print('type:' + str(type(e)))
  #   print('args:' + str(e.args))
  #   print('e自身:' + str(e))
  #   print('=================')
  #   print("QRコードをかざしてください")


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


def end_program():
  root.destroy()
  print("処理を終了しました。")
  sys.exit()


def window(last_time, cap, detector, init_tool, init_center, past_tool, past_center, flag_once):
  global root, cam11_canvas, cam12_canvas, main_canvas
  global main_frame, cam1_frame

  root = tkinter.Tk()
  root.state('zoomed')
  # root.attributes("-fullscreen", True)
  root.resizable(False, False)
  m_width, m_height = get_monitor_size(root)

  root.title("Tkinter_cv2")

  # ウィンドウの大きさを決定
  root.geometry("800x600")

  # ウィンドウのグリッドを 1x1 にする
  # この処理をコメントアウトすると配置がズレる
  root.grid_rowconfigure(0, weight=1)
  root.grid_columnconfigure(0, weight=1)

#-----------------------------main_frame---------------------------------
  # メインページフレーム作成
  main_frame = tkinter.Frame()
  main_frame.grid(row=0, column=0, sticky="nsew")

  margin = 0

  # タイトルラベル作成
  titleLabel0 = tkinter.Label(main_frame, text="QRコードをかざしてください", font=('Helvetica', '35'))
  titleLabel0.grid(row=0, column=0, sticky="nsew")

  main_canvas = tkinter.Canvas(main_frame, width = m_width, height = m_height)
  main_canvas.grid(row=1, column=0, sticky="nsew")

#-----------------------------cam1_frame---------------------------------
  # カメラ1用フレーム作成
  cam1_frame = tkinter.Frame()
  cam1_frame.grid(row=0, column=0, sticky="nsew")

  titleLabel1 = tkinter.Label(cam1_frame, text="処理中．．．", font=('Helvetica', '35'))
  titleLabel1.grid(row=0, column=0, padx=margin, sticky="nsew")
  # # カメラ1用キャンバス作成
  # cam11_canvas = tkinter.Canvas(cam1_frame, width = m_width/2, height = m_height)
  # cam11_canvas.grid(row=1, column=0, padx=0, sticky="nsew")
  
  # cam12_canvas = tkinter.Canvas(cam1_frame, width = m_width/2, height = m_height)
  # cam12_canvas.grid(row=1, column=1, padx=0, sticky="nsew")

  #main_frameを一番上に表示
  main_frame.tkraise()

  main(last_time, cap, detector, init_tool, init_center, past_tool, past_center, flag_once)

  root.mainloop()


def changePage(page):
  page.tkraise()


def update_main_canvas(ret, frame):#update
  global img
  
  if ret:
    width, height = get_monitor_size(root)
    img_resize = cv.resize(frame, (640*2, 480*2))
    img = ImageTk.PhotoImage(Image.fromarray(cv.cvtColor(img_resize, cv.COLOR_BGR2RGB)))
    main_canvas.create_image (width/2, height/2.2, image=img)
  else:
    print("u-Fail")


def get_monitor_size(root):
  m_width = root.winfo_screenwidth() #モニターの横幅を渡す
  m_height = root.winfo_screenheight() #モニターの縦幅を渡す

  return m_width, m_height


if __name__ == "__main__":

  last_time, cap, detector, init_img, init_tool, init_center, past_img, past_tool, past_center, flag_once = init()

  window(last_time, cap, detector, init_tool, init_center, past_tool, past_center, flag_once)