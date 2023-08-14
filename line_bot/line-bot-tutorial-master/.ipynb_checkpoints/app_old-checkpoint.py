import json
import sys
import datetime
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
from datetime import datetime,timezone,timedelta

from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
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
    #message = TextSendMessage(text='mytets ' + event.message.text)
    #line_bot_api.reply_message(event.reply_token, message)

    if event.message.text != "":
        #line_bot_api.reply_message(event.reply_token,TextSendMessage(text="紀錄成功"))
        
        pass
        #GDriveJSON就輸入下載下來Json檔名稱
        #GSpreadSheet是google試算表名稱
        GDriveJSON = 'key.json'
        #GSpreadSheet = 'LineBotTest'
        #line_bot_api.push_message(event.push_token, TextSendMessage(text="succesu_ppp"))
        while True:
            try:
                scope = ['https://spreadsheets.google.com/feeds']#, 'https://www.googleapis.com/auth/drive']
                key = SAC.from_json_keyfile_name(GDriveJSON, scope)
                gc = gspread.authorize(key)
                #worksheet = gc.open(GSpreadSheet).sheet1
                worksheet =gc.open_by_key("1t-7GgERBxs9ibTG6mQxS-qfyXNqKrshZmdzk82NaSik").sheet1
                print ("connected OK!")
                
                #line_bot_api.push_message(event.push_token, TextSendMessage(text="成功連線"))
            except Exception as ex:
                print('無法連線Google試算表')
                #print('無法連線Google試算表', ex)
                #line_bot_api.push_message(event.push_token, TextSendMessage(text="無法連線"))
                sys.exit(1)
                      
            received_text=received_text_0=received_text_1=""
            received_text+=event.message.text
            
            if len(received_text.split(',')) == 2:
                received_text_0+=received_text.split(',')[0]
                received_text_1+=received_text.split(',')[1]
                now_time = datetime.utcnow().replace(tzinfo=timezone.utc)
                now_time = str(now_time.astimezone(timezone(timedelta(hours=8)))).split('.')[0] # 轉換時區 -> 東八區取道時間就好
                worksheet.append_row([now_time, received_text_0, received_text_1])
                #print (datetime.datetime.now(), textt)
                #worksheet.append_row([textt])
                print('新增一列資料到試算表', worksheet,"新增內容",now_time, received_text_0, received_text_1 )
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="紀錄成功"))
                #line_bot_api.push_message(event.push_token, TextSendMessage(text="新增一列資料到試算表"))
                return received_text    
            else:
                line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤，正確格式=姓名,姓名"))
                return '格式錯誤,'



import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
