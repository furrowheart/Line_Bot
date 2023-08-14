# import json
# import sys
# import datetime
# import gspread
# from oauth2client.service_account import ServiceAccountCredentials as SAC
# from datetime import datetime,timezone,timedelta

import pandas as pd
import requests
from io import StringIO
import time

from flask import Flask, request, abort

from linebot import (LineBotApi, WebhookHandler)
from linebot.exceptions import (InvalidSignatureError)
from linebot.models import *

app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('6sktHQ9uyxefvG6JMYWm8AjIU5+og4fxjd9EnTUEORoxcKU3n3XwMrXH3iNMtmWN7UsZN+EeF28D3iBCuBWIZLcqnnIl/XlpkT1DN7cZcrmFTU06p81FzijQnWhaYANgN4Jtk6hkua7ycLFlqbvPMwdB04t89/1O/w1cDnyilFU=')
# Channel Secret
handler = WebhookHandler('b1dcd87b70535434a20afe8102bc9634')

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
        input_message = event.message.text
        try:
            int(input_message)
            result = stock_dog(input_message)
            push_message = '\n'.join(result)
            # print (result)
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text=push_message))
        except:
            line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤"))
        
        # pass
        # #GDriveJSON就輸入下載下來Json檔名稱
        # #GSpreadSheet是google試算表名稱
        # GDriveJSON = 'key.json'
        # #GSpreadSheet = 'LineBotTest'
        # #line_bot_api.push_message(event.push_token, TextSendMessage(text="succesu_ppp"))
        # while True:
        #     try:
        #         scope = ['https://spreadsheets.google.com/feeds']#, 'https://www.googleapis.com/auth/drive']
        #         key = SAC.from_json_keyfile_name(GDriveJSON, scope)
        #         gc = gspread.authorize(key)
        #         #worksheet = gc.open(GSpreadSheet).sheet1
        #         worksheet =gc.open_by_key("1t-7GgERBxs9ibTG6mQxS-qfyXNqKrshZmdzk82NaSik").sheet1
        #         print ("connected OK!")
                
        #         #line_bot_api.push_message(event.push_token, TextSendMessage(text="成功連線"))
        #     except Exception as ex:
        #         print('無法連線Google試算表')
        #         #print('無法連線Google試算表', ex)
        #         #line_bot_api.push_message(event.push_token, TextSendMessage(text="無法連線"))
        #         sys.exit(1)
                      
        #     received_text=received_text_0=received_text_1=""
        #     received_text+=event.message.text
            
        #     if len(received_text.split(',')) == 2:
        #         received_text_0+=received_text.split(',')[0]
        #         received_text_1+=received_text.split(',')[1]
        #         now_time = datetime.utcnow().replace(tzinfo=timezone.utc)
        #         now_time = str(now_time.astimezone(timezone(timedelta(hours=8)))).split('.')[0] # 轉換時區 -> 東八區取道時間就好
        #         worksheet.append_row([now_time, received_text_0, received_text_1])
        #         #print (datetime.datetime.now(), textt)
        #         #worksheet.append_row([textt])
        #         print('新增一列資料到試算表', worksheet,"新增內容",now_time, received_text_0, received_text_1 )
        #         line_bot_api.reply_message(event.reply_token,TextSendMessage(text="紀錄成功"))
        #         #line_bot_api.push_message(event.push_token, TextSendMessage(text="新增一列資料到試算表"))
        #         return received_text    
        #     else:
        #         line_bot_api.reply_message(event.reply_token,TextSendMessage(text="輸入錯誤，正確格式=姓名,姓名"))
        #         return '格式錯誤,'

def stock_dog(stock_num):
    # stock_num ='1101'
    result=[]
    安全邊際=0.8
    url_StockDividendPolicy = 'https://goodinfo.tw/tw/StockDividendPolicy.asp?STOCK_ID=' + stock_num
    # 偽瀏覽器
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    # 下載該年月的網站，並用pandas轉換成 dataframe
    r = requests.get(url_StockDividendPolicy, headers=headers)
    r.encoding = 'UTF-8'
    try:
        dfs_StockDividendPolicy = pd.read_html(StringIO(r.text), encoding='UTF-8')
        股票名稱 = (pd.concat([df for df in dfs_StockDividendPolicy if df.shape[1] <=8  and df.shape[1] > 5]).iloc[0].index[0][0])
        print (股票名稱)
        result.append(股票名稱)
        for i ,df_ in pd.concat([df for df in dfs_StockDividendPolicy if df.shape[1] <=8  and df.shape[1] > 5]).iloc[0].reset_index().T.drop('level_0',axis=0).T.iterrows():
            print(list(df_))
            result.append(':'.join(df_))

        df_StockDividendPolicy = pd.concat([df for df in dfs_StockDividendPolicy if df.shape[1] <= 54 and df.shape[1] > 23])
        df_StockDividendPolicy = df_StockDividendPolicy[[(  '股 利 政 策',     '股利發放年度',   '股利發放年度', '股利發放年度'),(  '盈餘分配率統計',    '盈餘分配率統計', '盈餘分配率(%)',     '合計'),('殖 利 率 統 計',  '殖 利 率 統 計', '年均殖利率(%)',     '合計')]]#[['股利發放年度','合計']]
        df_StockDividendPolicy.columns = df_StockDividendPolicy.columns.droplevel().droplevel().droplevel()
        df_StockDividendPolicy.columns=['股利發放年度','合計盈餘分配率','合計年均殖利率']
        new_df_StockDividendPolicy=[]
        for i,datas in df_StockDividendPolicy.iterrows():
            try: 
                int(datas[0]) and float(datas[1])
                new_df_StockDividendPolicy.append(datas)
            except:
                pass
        df_stock_rate = pd.DataFrame(new_df_StockDividendPolicy).reset_index(drop=True)
        if df_stock_rate.empty:
            print ('查無歷年股利資料')
            result.append('查無歷年股利資料')
        else:
            近五年 = df_stock_rate.iloc[0:5]
            起年 = 近五年['股利發放年度'][4]
            訖年 = 近五年['股利發放年度'][0]

            total_分配率=0
            total_殖利率=0
            for i in range(5):
                total_分配率 = total_分配率 + float(近五年['合計盈餘分配率'][i])
                total_殖利率 = total_殖利率 + float(近五年['合計年均殖利率'][i])
            五年平均發放率 = total_分配率/5
            五年平均殖利率 = total_殖利率/5
            print (起年+訖年+'五年平均盈餘發放率: '+ str(round(五年平均發放率,2)))
            print (起年+訖年+'五年平均殖利率: '+ str(round(五年平均殖利率,2)))

            result.append(f'{起年}~{訖年} 五年平均盈餘發放率: {str(round(五年平均發放率,2))}')
            result.append(f'{起年}~{訖年} 五年平均殖利率: {str(round(五年平均殖利率,2))}')

        url_FinDetail = 'https://goodinfo.tw/tw/StockFinDetail.asp?RPT_CAT=IS_M_QUAR_ACC&STOCK_ID=' + stock_num
        # 偽瀏覽器
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        # 下載該年月的網站，並用pandas轉換成 dataframe
        r_FinDetail = requests.get(url_FinDetail, headers=headers)
        r_FinDetail.encoding = 'UTF-8'
        dfs_FinDetail = pd.read_html(StringIO(r_FinDetail.text), encoding='UTF-8')
        try:
            df_FinDetail = pd.concat([df for df in dfs_FinDetail if df.shape[1] <= 15 and df.shape[1] > 10])

            df_FinDetail.columns = df_FinDetail.columns.droplevel(1)
            df_FinDetail = df_FinDetail.T
            df_FinDetail.columns = df_FinDetail.iloc[0]
            df_FinDetail = df_FinDetail.drop('本業獲利',axis=0).reset_index()

            df_FinDetail = df_FinDetail[['index','每股稅後盈餘(元)']]

            new_df_FinDetail=[]
            for i,datas in df_FinDetail.iterrows():
                try: 
                    float(datas[1])
                    new_df_FinDetail.append(datas)
                except:
                    pass
            df_stock_findetail = pd.DataFrame(new_df_FinDetail).reset_index(drop=True)

            年季度 = df_stock_findetail['index'][0]
            稅後盈餘 = df_stock_findetail['每股稅後盈餘(元)'][0]

            print ('累積至'+str(年季度)+' 每股稅後盈餘 '+ str(稅後盈餘))

            print ('推估每股價格'+str(round(float(稅後盈餘)*五年平均發放率/五年平均殖利率*安全邊際,2)))
            
            result.append('累積至'+str(年季度)+' 每股稅後盈餘 '+ str(稅後盈餘))
            result.append('推估每股價格'+str(round(float(稅後盈餘)*五年平均發放率/五年平均殖利率*安全邊際,2)))
        except:
            print('每股稅後盈餘資料有誤，或查無資料')
            result.append('每股稅後盈餘資料有誤，或查無資料')
        print(result)
    except:
        print(r.text)
        result.append(r.text)
    return result




import os
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
