import tkinter as tk
import PIL
import cv2
from PIL import Image, ImageTk, ImageOps  # 画像関連
 
 
class CameraApplication(tk.Frame):
    def __init__(self, master = None):
        super().__init__(master)
         
        # カメラ --------------------------------------------------------------------
        # USBカメラの設定(idは、基本:0、カメラ搭載PC:1(0は搭載カメラ))
        camera_id = 0
        self.cap = cv2.VideoCapture(camera_id)
        # 撮影制御用(True:撮影中  False:停止中)
        # self.cap_flg = True
 
        # 基本情報 --------------------------------------------------------------------
        # タイトル
        root.title('USBカメラアプリ')
        # ウィンドサイズ
        # root.geometry('800x600')
        root.attributes('-fullscreen', True)
 
        # 構成要素 ----------------------------------------------------------------------
        # ラベル-1
        label_cam = tk.Label(root, text='カメラの映像')
        label_cam.pack()
        # ラベル-2
        self.label_quality = tk.Label(root, text='画質')
        self.label_quality.pack()

        # キャンバス(画像表示)
        self.canvas_cam = tk.Canvas(self.master,width=1280,height=960,bg='yellow')
        self.canvas_cam.pack()
        # canvasのサイズ取得
        self.canvas_cam.update()
        self.canvas_w = self.canvas_cam.winfo_width()
        self.canvas_h = self.canvas_cam.winfo_height()
        
        self.start_video()
 
    # 動画再生(再帰的に自身を呼ぶ)
    def start_video(self):
         
        global photo
         
        # カメラ画像の取得(ret:画像の取得可否のTrue/Flase, frame:RGB画像)
        ret, frame1 = self.cap.read()
        # print(str(self.canvas_w) + ' ' + str(self.canvas_h))
        # print(self.canvas_h)

        frame = cv2.resize(frame1 , (self.canvas_w, self.canvas_h))
        # print(str(frame.shape))

        # BGRで取得したものをRGBに変換する
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # OpenCV frame を Pillow Photo に変換(canvasに表示するにはPillowの軽視にする必要がある)
        photo = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))       
        # canvasに画像を表示
        self.canvas_cam.create_image(self.canvas_w/2, self.canvas_h/2, image=photo)
        # 画像サイズをラベルに表示
        self.label_quality['text'] = 'Image shape:'+str(frame.shape)
         
        # 100msec後に start_video()を実行(繰り返し)-----------------
        self.after(100, self.start_video)
 
 
if __name__ == '__main__':
    root = tk.Tk()
    app = CameraApplication(master = root)
    app.mainloop()