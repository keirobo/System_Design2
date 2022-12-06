import tkinter as tk
import PIL
import cv2
from PIL import Image, ImageTk, ImageOps  # 画像関連
 
def start_video():
         
    global photo
     
    # カメラ画像の取得(ret:画像の取得可否のTrue/Flase, frame:RGB画像)
    ret, frame1 = cap.read()

    frame = cv2.resize(frame1 , (canvas_w, canvas_h))

    # BGRで取得したものをRGBに変換する
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    # OpenCV frame を Pillow Photo に変換(canvasに表示するにはPillowの軽視にする必要がある)
    photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))       
    # canvasに画像を表示
    canvas_cam.create_image(canvas_w/2, canvas_h/2, image=photo)
    # 画像サイズをラベルに表示
    label_quality['text'] = 'Image shape:'+str(frame.shape)
     
    # 100msec後に start_video()を実行(繰り返し)-----------------
    root.after(100, start_video)
 
if __name__ == '__main__':
    root = tk.Tk()

    # カメラ --------------------------------------------------------------------
    # USBカメラの設定(idは、基本:0、カメラ搭載PC:1(0は搭載カメラ))
    camera_id = 0
    cap = cv2.VideoCapture(camera_id)
 
    # 基本情報 --------------------------------------------------------------------
    # タイトル
    root.title('USBカメラアプリ')
    # ウィンドサイズ フルスクリーン
    root.attributes('-fullscreen', True)
 
    # 構成要素 ----------------------------------------------------------------------
    # ラベル-1
    label_cam = tk.Label(root, text='カメラの映像')
    label_cam.pack()
    # ラベル-2
    label_quality = tk.Label(root, text='画質')
    label_quality.pack()

    # キャンバス(画像表示)
    canvas_cam = tk.Canvas(root,width=640*2.5,height=480*2.5,bg='yellow')
    canvas_cam.pack()
    # canvasのサイズ取得
    canvas_cam.update()
    canvas_w = canvas_cam.winfo_width()
    canvas_h = canvas_cam.winfo_height()
    
    start_video()
    # app = CameraApplication(master = root)
    root.mainloop()