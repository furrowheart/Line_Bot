import json
import sys
import datetime
import gspread
import os
from oauth2client.service_account import ServiceAccountCredentials as SAC
from datetime import datetime,timezone,timedelta
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('hXPg265f8nuWlpgRcWY50h+nlf9UPhRGiF7Lq9pREzTch00QwWW4b7SyZCPAZHKd9GBOQ1ZNlWbp3kntYq7F/+MGp0KV7+Tv4FQc6Rz74Hk/dLIUzxNE6Di8XZIxCfHajCxMEa0P8CYeoqBJNdnfUQdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('07e15acd70615b639f361eb459b201bc')

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'


# 處理訊息
@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    #GDriveJSON就輸入下載下來Json檔名稱
    GDriveJSON = 'key.json'
    
    user_id = event.source.user_id
    profile = line_bot_api.get_profile(user_id)
    user_name = profile.display_name
    admin_ID='Uab2962645443138b692abcf0f1d369d4'
    #print("user_id =", user_id)
    
    while True:
        try:
            scope = ['https://spreadsheets.google.com/feeds']
            key = SAC.from_json_keyfile_name(GDriveJSON, scope)
            gc = gspread.authorize(key)
            worksheet =gc.open_by_key("1t-7GgERBxs9ibTG6mQxS-qfyXNqKrshZmdzk82NaSik").sheet1
            print ("connected OK!")
        except Exception as ex:
            print('無法連線Google試算表')
            #line_bot_api.push_message(event.push_token, TextSendMessage(text="無法連線"))
            sys.exit(1)
        received_text=received_text_0=received_text_1=""
        received_text+=event.message.text
        if '出坡' in received_text :
            line_bot_api.push_message(admin_ID, TextSendMessage(text=user_name + '回覆如下\n' + event.message.text))
            line_bot_api.reply_message(event.reply_token, TextSendMessage(text='阿彌陀佛，感恩菩薩回覆!!，已將您的出坡訊息傳送給管理員。'))
            return received_text
                   
        elif '登記' in received_text : 
            if len(received_text.split('@')) == 3:
                received_text_0+=received_text.split('@')[1]
                received_text_1+=received_text.split('@')[2]
                now_time = datetime.utcnow().replace(tzinfo=timezone.utc)
                now_time = str(now_time.astimezone(timezone(timedelta(hours=8)))).split('.')[0] # 轉換時區 -> 東八區取道時間就好
                #worksheet.append_row([now_time, received_text_0, received_text_1]) #寫入資料表
                print('新增一列資料到試算表', worksheet,"新增內容",now_time, received_text_0, received_text_1 )
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="紀錄成功"))
                print(str(event.reply_token))
                return received_text    
            else :
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤，正確格式=姓名,姓名"))
                return '格式錯誤,'
        else:
            line_bot_api.push_message(user_id, TextSendMessage(text='阿彌陀佛，提醒菩薩本帳號僅供回覆大出坡使用。\n'+
                                                               '若要回覆登記出坡，請在內容中加入"出坡"兩字即可。\n'+
                                                               '若仍有其他問題，請直接聯繫管理員。'))
            return received_text


if __name__ == "__main__":
    app.run()
