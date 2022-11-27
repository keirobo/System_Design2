import Tool_Estimation
import SlackBot as SB
import Spreadsheet
import configparser

def main():
  # ここに処理を書く
  config = configparser.ConfigParser()

  #ログイン情報
  config.read("config.ini", encoding="utf-8")
  
  Slack_Token = config['user']['Slack_Token']

  print(Slack_Token)

  SB.write(Slack_Token, "U01T72KE2VC")

  while(True):
    print("main")
    break


if __name__ == "__main__":
  main()