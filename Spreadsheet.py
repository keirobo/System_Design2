import gspread

key_name = 'data.json'
sheet_name = 'データ'

gc = gspread.service_account(filename = key_name)

wks = gc.open(sheet_name).sheet1
wks.update_cell(1, 1, 'Pythonから入力')