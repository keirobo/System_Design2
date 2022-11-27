import Tool_Estimation
import SlackBot as SB
import Spreadsheet as SS
import configparser

def main():
  # ここに処理を書く
  config = configparser.ConfigParser()

  #ログイン情報
  config.read("config.ini", encoding="utf-8")
  Slack_Token = config['Slack']['token']
  key = config['Spreadsheet']['Key']

  print(key)

  SS.init(key)

  user_id = SS.get_user_id(1)

  # print(user_id)

  if(str(user_id).startswith('None') == False): SB.write(Slack_Token, user_id)

  while(True):
    # print("main")
    break


if __name__ == "__main__":
  main()