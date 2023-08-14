import json
from cProfile import label
import json
import sys
import datetime
import gspread
import os
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


# 處理MessageEvent
@handler.add(MessageEvent, message=TextMessage)

def handle_message(event):
    # 送訊息進來的line userID，透過userID取得line暱稱
    user_id = event.source.user_id  # line系統上的id，不是我們設定的line id
    profile = line_bot_api.get_profile(user_id) #透過id取得使用者檔案資訊
    user_name = profile.display_name # 取得line暱稱
    admin_ID = 'Uab2962645443138b692abcf0f1d369d4' # 開發者的line ID  每個人不同
    ngrok_url = 'https://d642-60-251-61-52.ngrok.io'

    # received_text=received_text_0=received_text_1=""

    received_text = event.message.text

    # if '14天再住院' in received_text :
    #     # 這行是主動推送訊息給某人，預設是管理者
    #     # line_bot_api.push_message(admin_ID, TextSendMessage(text=user_name + '回覆如下\n' + event.message.text))  
        
    #     # 回復訊息 不算主動推送
    #     查詢年月 = '2022年2月'
    #     出院人數 = '6148'
    #     近期再入院率 = '11.3%'
    #     非計劃性近期再入院率 = '1.9%'
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text = str(user_name) + '您好, ' + str(查詢年月) \
    #                                                                         + '總出院人數為' + str(出院人數) + ',' \
    #                                                                         +'近期再入院率為' + str(近期再入院率) +','\
    #                                                                         +'非計劃性近期再入院率為' + str(非計劃性近期再入院率)
    #                                                                 ))
    #     return received_text

    if '查詢指標' == received_text:
        # message = TemplateSendMessage(
        # alt_text='查詢指標', template=ButtonsTemplate(thumbnail_image_url='https://i.imgur.com/TLE3Fl9.jpg', title = received_text, text = '選擇品管指標',
        #                              actions=[MessageTemplateAction(label='14天再住院', text= received_text + '一月'),
        #                                       MessageTemplateAction(label='三日內重返急診', text= received_text + '二月')]))
        # line_bot_api.reply_message(event.reply_token, message)  
        FlexMessage = json.load(open('flex_messange/select_indicator.json','r',encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('查詢指標',FlexMessage)) 

    elif '查詢14天再住院' == received_text:
        FlexMessage = json.load(open('flex_messange/select_month_readmission.json','r',encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('選擇月份',FlexMessage)) 
    
    elif '查詢三日內重返急診' == received_text:
        FlexMessage = json.load(open('flex_messange/select_month_erafterdischarge.json','r',encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('選擇月份',FlexMessage)) 
    
    elif '查詢趨勢圖' == received_text:
        message = ImageSendMessage(
        original_content_url='https://b42f-60-251-53-35.ngrok.io/Image/trend.PNG',
        preview_image_url='https://b42f-60-251-53-35.ngrok.io/Image/trend.PNG'
        )
        line_bot_api.reply_message(event.reply_token, message)


    elif '查詢二月份14天再住院率' == received_text :
        查詢年月 = '2022年2月'
        出院人數 = '6148'
        近期再入院率 = '11.3%'
        非計劃性近期再入院率 = '1.9%'
        # a = b'\x31\xE2\x83\xA3'
        # str(a.decode('UTF-8','strict')
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = str(user_name) + '您好🏥 ' + str(查詢年月) \
                                                                            + '🔸總出院人數為' + str(出院人數) \
                                                                            +'🔸近期再入院率為' + str(近期再入院率) \
                                                                            +'🔸非計劃性近期再入院率為' + str(非計劃性近期再入院率))
                                                                    )
                   
    elif '查詢二月份三日內重返急診率' == received_text : 
        查詢年月 = '2022年2月'
        出院人數 = '6148'
        三日內重返急診率 = '1.35%'
        line_bot_api.reply_message(event.reply_token, TextSendMessage(text = str(user_name) + '您好🏥 ' + str(查詢年月) \
                                                                            + '🔸總出院人數為' + str(出院人數) \
                                                                            +'🔸出院後三日內重返急診率為' + str(三日內重返急診率) 
                                                                    )
                                    )
    else:
        FlexMessage = json.load(open('flex_messange/main_bubble.json','r',encoding='utf-8'))
        line_bot_api.reply_message(event.reply_token, FlexSendMessage('🏥點我查看更多資訊📊',FlexMessage)) 
    
    
    # else:
    #     message = TemplateSendMessage(
    #     alt_text='Buttons template', template=ButtonsTemplate(thumbnail_image_url='https://i.imgur.com/TLE3Fl9.jpg', title = received_text, text = '請選擇月份',
    #                                  actions=[MessageTemplateAction(label='一月', text= received_text + '一月'),
    #                                           MessageTemplateAction(label='二月', text= received_text + '二月'),
    #                                           URITemplateAction(label='前往品管中心', uri='https://wd.vghtpe.gov.tw/mqmc/Index.action')]))
    #     line_bot_api.reply_message(event.reply_token, message)
        #圖片訊息  圖片訊息要解決url網址的問題
        # ImageSendMessage物件中的輸入
        # original_content_url 以及 preview_image_url都要寫才不會報錯。
        #輸入的網址要是一個圖片，應該說只能是一個圖片，不然不會報錯但是傳過去是灰色不能用的圖

        # image_url = 'https://i.imgur.com/eTldj2E.png?1'
        # local_save = '/Image/logo.jpg'
        # line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url = ngrok_url+local_save, preview_image_url = ngrok_url+local_save))

        # line_bot_api.reply_message(event.reply_token, ImageSendMessage(original_content_url = ngrok_url + "/static/" + event.message.id + ".png", preview_image_url = ngrok_url + "/static/" + event.message.id + ".png"))

    # else:
    #     line_bot_api.reply_message(event.reply_token, TextSendMessage(text=str(user_name) + '您好, ' \
    #                                                         + '輸入資訊有錯誤，請確認查詢項目。' \
    #                                                         + '若仍有其他問題，請聯繫管理員。')
    #                                 )
    #     return received_text


if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
    a = 'ppppp'
