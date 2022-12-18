from slack_sdk import WebClient

def init(_token):
  global token
  token = _token

def get_user_id():
  client = WebClient()
  res = client.users_list()

  for member in res['members']:
    print(member['name'])
    print(member['id'])
    print()


def write_DM(user_id, message):
  print("write")
  client = WebClient(token)
  
  # DMを開き，channelidを取得する．
  res = client.conversations_open(users=user_id)
  dm_id = res['channel']['id']
  
  # DMを送信する
  client.chat_postMessage(channel=dm_id, text=message)