import Tool_Estimation as TE
import SlackBot as SB
import Spreadsheet as SS
import configparser
import cv2 as cv
import numpy as np
from pyzbar.pyzbar import decode

def main():
  
  cap = cv.VideoCapture(0)
  #出力ウィンドウの設定
  # cap.set(3,640)
  # cap.set(3,480)

  # ここに処理を書く
  config = configparser.ConfigParser()

  config.read("config.ini", encoding="utf-8")
  Slack_Token = config['Slack']['token']
  key = config['Spreadsheet']['Key']

  print(key)

  SS.init(key)

  while(True):
    # print("main")

    ret, frame = cap.read()
    #フレームが正しく読み取られた場合、retはTrue
    if not ret:
        print("フレームは受信できません。終了しています...")
        break

    # 結果のフレーム表示
    # if cv.waitKey(1) & 0xFF == ord('q'):
    #     break
    codes = decode(frame)
    if len(codes) > 0:
      output = codes[0][0].decode('utf-8', 'ignore')
      print(output)
      if 'output' != None:
        #cap_cam.read()
        # cap.release()
    
        user_id = SS.get_user_id(output)

        if(str(user_id).startswith('None') == False): SB.write(Slack_Token, user_id)
    
    # if len(barcode) >= 1:
    #   #QRコードデータはバイトオブジェクトなので、カメラ上に描くために、文字列に変換する
    #   myData = barcode.data.decode('utf-8')
    #   print(myData)
    #   #QRコードの周りに長方形を描画しデータを表示する
    #   pts =np.array([barcode.polygon],np.int32)
    #   #polylines()関数で複数の折れ線を描画
    #   cv.polylines(frame,[pts],True,(255,0,0),5)
    #   pts2 =barcode.rect
    #   #putText()関数で文字列を描画
    #   cv.putText(frame,myData,(pts2[0],pts2[1]),cv.FONT_HERSHEY_COMPLEX,1,(255,0,0),2)
    # #imshow()関数で出力ウィンドウを表示
    # cv.imshow('test',frame)
    # #qキーが押されるまで待機
    # if cv.waitKey(1) & 0xFF == ord('q'):
    #   break
      
    # break


if __name__ == "__main__":
  main()