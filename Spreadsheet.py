import gspread
from google.oauth2.service_account import Credentials
import re

# # お決まりの文句
# # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
# scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
# #ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
# credentials = Credentials.from_service_account_file("data.json", scopes=scope)
# #OAuth2の資格情報を使用してGoogle APIにログイン。
# gc = gspread.authorize(credentials)
# #スプレッドシートIDを変数に格納する。
# SPREADSHEET_KEY = '1TbHWzz_DXu8TPnwO-rwzJTcQct0bKgsgQmNFsuwz0Fs'
# # スプレッドシート（ブック）を開く
# workbook = gc.open_by_key(SPREADSHEET_KEY)

# # シートの一覧を取得する。（リスト形式）
# worksheets = workbook.worksheets()
# print(worksheets)
# # シートを開く
# worksheet = workbook.worksheet('シート1')
# # セルA1に”test value”という文字列を代入する。
# worksheet.update_cell(1, 1, 'test value')

# data = worksheet.find("aa")
# print(data)

def init(key):
  global KEY, gc, workbook
  # お決まりの文句
  # 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
  scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
  #ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
  credentials = Credentials.from_service_account_file("data.json", scopes=scope)
  #OAuth2の資格情報を使用してGoogle APIにログイン。
  gc = gspread.authorize(credentials)
  #スプレッドシートIDを変数に格納する。
  KEY = key
  workbook = gc.open_by_key(KEY)

def get_user_id(id):
  # シートを開く
  worksheet = workbook.worksheet('ユーザー情報')

  tmp1 = worksheet.find(str(id))
  tmp2 = worksheet.find("Slack_ID")
  
  if(str(tmp1).startswith('None')): return "None"
  
  # print(tmp1)
  # print(tmp2)
  
  print(str(tmp1.row) + " " + str(tmp2.col))

  return worksheet.cell(tmp1.row, tmp2.col).value