import gspread
from google.oauth2.service_account import Credentials
import re
import wrapt_timeout_decorator

# @wrapt_timeout_decorator.timeout(dec_timeout=10)
def init(key):
  global workbook
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

  print(workbook)

  return workbook


def get_slack_id(id):
  # シートを開く
  worksheet = workbook.worksheet('Slack')

  tmp1 = worksheet.find(str(id))
  tmp2 = worksheet.find("Slack_ID")
  
  if(str(tmp1).startswith('None')): return "None"
  
  # print(tmp1)
  # print(tmp2)
  
  # print(str(tmp1.row) + " " + str(tmp2.col))

  return worksheet.cell(tmp1.row, tmp2.col).value


def get_max_id():
  worksheet = workbook.worksheet('ユーザー情報')
  
  tmp1 = worksheet.find("ユーザーID")
  data = worksheet.col_values(tmp1.col)
  
  data.pop(0)
  data = [int(i) for i in data]

  max_id = max(data)

  return max_id


def get_name(id):
  worksheet = workbook.worksheet('ユーザー情報')
  
  tmp1 = worksheet.find(str(id))
  tmp2 = worksheet.find("氏名")

  return worksheet.cell(tmp1.row, tmp2.col).value
  

def get_tool_name(id):
  worksheet = workbook.worksheet('工具情報')
  
  tmp1 = worksheet.find(str(id+1))
  tmp2 = worksheet.find("工具名")

  return worksheet.cell(tmp1.row, tmp2.col).value


def write_return(user_id, tool_id, time):
  worksheet = workbook.worksheet('貸し出し情報')
  
  tmp1 = worksheet.find("ユーザーID")
  write_row = (len(worksheet.col_values(tmp1.col)) + 1)
  # print(write_row)
  
  worksheet.update_cell(write_row, 1, str(user_id))
  worksheet.update_cell(write_row, 2, str(tool_id+1))
  worksheet.update_cell(write_row, 3, str(time))
  worksheet.update_cell(write_row, 4, str(0))


def write_lend(user_id, tool_id, time):
  worksheet = workbook.worksheet('貸し出し情報')
  
  tmp1 = worksheet.find("ユーザーID")
  write_row = (len(worksheet.col_values(tmp1.col)) + 1)
  # print(write_row)
  
  worksheet.update_cell(write_row, 1, str(user_id))
  worksheet.update_cell(write_row, 2, str(tool_id+1))
  worksheet.update_cell(write_row, 3, str(time))
  worksheet.update_cell(write_row, 4, str(1))

def get_lend_info():
  worksheet = workbook.worksheet('貸し出し情報')
  
  tmp = worksheet.find("工具ID")
  id_data = worksheet.col_values(tmp.col)

  tmp = worksheet.find("貸出フラグ")
  flag_data = worksheet.col_values(tmp.col)

  return id_data, flag_data