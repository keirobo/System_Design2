from slack_sdk import WebClient

def get_user_id(token):
  client = WebClient(token)
  res = client.users_list()

  for member in res['members']:
    print(member['name'])
    print(member['id'])
    print()

def write(token, user_id):
  print("write")
  client = WebClient(token)
  
  # DMを開き，channelidを取得する．
  res = client.conversations_open(users=user_id)
  dm_id = res['channel']['id']
  
  # DMを送信する
  client.chat_postMessage(channel=dm_id, text='DMです')