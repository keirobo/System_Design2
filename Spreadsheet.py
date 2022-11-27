import gspread
from google.oauth2.service_account import Credentials
# お決まりの文句
# 2つのAPIを記述しないとリフレッシュトークンを3600秒毎に発行し続けなければならない
scope = ['https://www.googleapis.com/auth/spreadsheets','https://www.googleapis.com/auth/drive']
#ダウンロードしたjsonファイル名をクレデンシャル変数に設定。
credentials = Credentials.from_service_account_file("data.json", scopes=scope)
#OAuth2の資格情報を使用してGoogle APIにログイン。
gc = gspread.authorize(credentials)
#スプレッドシートIDを変数に格納する。
SPREADSHEET_KEY = '1TbHWzz_DXu8TPnwO-rwzJTcQct0bKgsgQmNFsuwz0Fs'
# スプレッドシート（ブック）を開く
workbook = gc.open_by_key(SPREADSHEET_KEY)

# シートの一覧を取得する。（リスト形式）
worksheets = workbook.worksheets()
print(worksheets)
# シートを開く
worksheet = workbook.worksheet('シート1')
# セルA1に”test value”という文字列を代入する。
worksheet.update_cell(1, 1, 'test value')

data = worksheet.find("aa")
print(data)