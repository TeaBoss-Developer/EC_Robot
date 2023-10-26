import requests
import json
import websocket
import time
import threading
import datetime
heart_beat_time=0
header={
    "Content-Type": "application/json",
    "Authorization": "Bot 102072390.Jsb7oWr0V2yF2FnOmNpJQLdYym5VElKf"
}
auth={
    "op": 2,
    "d": {
        "token": "Bot 102072390.Jsb7oWr0V2yF2FnOmNpJQLdYym5VElKf",
        "intents": 1073745920
    }
}
def on_open(wsapp):
    print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Event:"+"on_open")
def on_close(wsapp):
    print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Event:"+"on_close")
    data={
        "op": 6,
        "d": {
        "token": "my_token",
        "session_id": "session_id_i_stored",
        "seq": 1337
        }
    }
    wsapp.send(json.dumps(data))
def on_bot_msg(type1,channel_id,guild_id,sender_id,sender_name,msg,msg_id,re_id):
    if(type1=="DIRECT_MESSAGE_CREATE"):#私聊
        print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]Robot Event:"+"DM")
    if(type1=="AT_MESSAGE_CREATE"):
        if("/菜单" in msg):
            data = {"content":"已经收到您的菜单请求啦~","msg_id":msg_id,"message_reference":{"message_id":re_id}}
            url = 'https://sandbox.api.sgroup.qq.com/channels/'+channel_id+'/messages'
            print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Api Result:"+"Api_Result:"+requests.post(url=url,data=json.dumps(data),headers=header).text)
def on_message(wsapp, message):
    print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Message:"+"on_message:", message)
    msg = json.loads(message)
    if(msg["op"]==10):
        heart_beat_time=msg["d"]["heartbeat_interval"]
        print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Event:"+'send_auth',json.dumps(auth))
        wsapp.send(json.dumps(auth))
        def heart_beat():
            while True:
                time.sleep(heart_beat_time/1000)
                wsapp.send(json.dumps({"op": 1,"d": 251}))
        threading.Thread(target=heart_beat).start()
    if(msg['op']==0):
        on_bot_msg(msg["t"],msg['d']["channel_id"],msg['d']["guild_id"],msg['d']["author"]["id"],msg['d']["author"]["username"],msg["d"]["content"],msg['id'],msg['d']['id'])
    if(msg['op']==11):
        print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Event:"+"Heart_Beat_ACK")
wsapp = websocket.WebSocketApp(json.loads(requests.get("https://sandbox.api.sgroup.qq.com/gateway",headers=header).text)["url"],on_open=on_open,on_message=on_message,on_close=on_close)
wsapp.run_forever()


