import requests
import json
import websocket
import time
import threading
import datetime
import Config
heart_beat_time=0
token=f"Bot {str(Config.appid)}.{Config.token}"
session_id=""
header={#common header
    "Content-Type": "application/json",
    "Authorization": token
}
auth={#login
    "op": 2,
    "d": {
        "token": token,
        "intents": 1677726721#私域全部1946162689公域全部1677726721
    }
}
def on_open(wsapp):
    print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Event:"+"on_open")
def on_close(wsapp):
    print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Event:"+"on_close")
def on_bot_msg(type1,channel_id,guild_id,sender_id,sender_name,msg,msg_id,re_id):
    if(type1=="DIRECT_MESSAGE_CREATE"):#私聊Todo
        print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]Robot Event:"+"DM")
    if(type1=="AT_MESSAGE_CREATE"):#已完成部分
        if("/菜单" in msg):
            data = {"content":"已经收到您的菜单请求啦~","msg_id":msg_id,"message_reference":{"message_id":re_id}}
            url = 'https://sandbox.api.sgroup.qq.com/channels/'+channel_id+'/messages'
            print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Api Result:"+"Api_Result:"+requests.post(url=url,data=json.dumps(data),headers=header).text)
        if("获取频道列表" in msg):
            url="https://sandbox.api.sgroup.qq.com/users/@me/guilds"
            result = requests.get(url,headers=header).text
            alls=""
            for re in json.loads(result):
                alls+="\n"
                alls+=f"[{re['id']}]{re['name']}\n所有者ID:{re['owner_id']}\n人数{re['member_count']}/{re['max_members']}\n__________________________________\n"
            data = {"content":alls,"msg_id":msg_id,"message_reference":{"message_id":re_id}}
            url = 'https://sandbox.api.sgroup.qq.com/channels/'+channel_id+'/messages'
            print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Api Result:"+"Api_Result:"+requests.post(url=url,data=json.dumps(data),headers=header).text)
        if('获取子频道列表 ' in msg):#未生效_ToFix
            try:
                guild_id=str(msg).split(' ')[1]
            except:
                data = {"content":"出现错误","msg_id":msg_id,"message_reference":{"message_id":re_id}}
                url = 'https://sandbox.api.sgroup.qq.com/channels/'+channel_id+'/messages'
                print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Api Result:"+"Api_Result:"+requests.post(url=url,data=json.dumps(data),headers=header).text)
            if(guild_id == ""):
                data = {"content":"频道ID为空","msg_id":msg_id,"message_reference":{"message_id":re_id}}
                url = 'https://sandbox.api.sgroup.qq.com/channels/'+channel_id+'/messages'
                print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Api Result:"+"Api_Result:"+requests.post(url=url,data=json.dumps(data),headers=header).text)
            url="https://sandbox.api.sgroup.qq.com/guilds/"+guild_id+"/channels"
            result = requests.get(url,headers=header).text
            alls=""
            for re in json.loads(result):
                alls+=f"\n[{re['id']}({re['guild_id']})]{re['name']}|type:{re['type']}|position:{re['position']}/{json.loads(result)}"
            data = {"content":alls,"msg_id":msg_id,"message_reference":{"message_id":re_id}}
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
        if(msg['t']=="READY"):
            session_id=msg['d']['session_id']
        on_bot_msg(msg["t"],msg['d']["channel_id"],msg['d']["guild_id"],msg['d']["author"]["id"],msg['d']["author"]["username"],msg["d"]["content"],msg['id'],msg['d']['id'])
    if(msg['op']==11):
        print(f"[LOG time:{str(datetime.datetime.now()).split('.')[0]}]System Event:"+"Heart_Beat_ACK")
wsapp = websocket.WebSocketApp(json.loads(requests.get("https://sandbox.api.sgroup.qq.com/gateway",headers=header).text)["url"],on_open=on_open,on_message=on_message,on_close=on_close)
wsapp.run_forever()


