from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random
import requests
from bs4 import BeautifulSoup
import json
import datetime
import time
import pandas as pd


app = Flask(__name__)

# Channel Access Token
line_bot_api = LineBotApi('KUwPW2Ws4iN+QaS3Qg0mu1HjMaH/NSXse0gt9TC/YuzJ0DHD2LMhW4KO/L/yqC6VQ2eUTiQNYt3ODpdDv/+HGBPGEk41kZ2gBHT9p7/8KYc199fIDISjNCfBR6QEBZGEKGryBEnonz+zfXI4sNonOgdB04t89/1O/w1cDnyilFU=')
#or line_bot_api = 'Channel_token'

# Channel Secret
handler = WebhookHandler('a8133af7eb5c252d6585277053a33fae')
#or handler = 'Channel_secret'

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
# 抓到今天的時間
now = datetime.datetime.now()

# 先與網站請求抓到價格
def getstock(stocknumber='2801.tw'):
    url = 'http://61.220.30.176/GVE3/index.aspx' + stocknumber + '& =' + str(time.mktime(now.timetuple()))
    list_req = requests.get(url)
    soup = BeautifulSoup(list_req.content, "html.parser")
    getjson=json.loads(soup.text)
    
    # 判斷請求是否成功
    if getjson['stat'] != '很報前，沒有符合條件的資料!':
        return [getjson['data']]
    else:
        return [] #請求失敗回傳空值
    
# 開始計算股票的平均以及標轉差
def Standard_Deviation(stocknumber='2801.tw'):
    stocklist = getstock(stocknumber)
    
    # 判斷是否為空值
    if len(stocklist) != 0:
        stockdf = pd.DataFrame(stocklist[0],columns=["昨收價","成交價","成交量","漲跌","漲跌幅","委買價","委賣價","委買量","委賣價","單位股數"])
        stockAverage = pd.to_numeric(stockdf['成交價']).mean()
        stockSTD = pd.to_numeric(stockdf['成交價']).std()
        
        # 看看這支股票現在是否便宜 (平均=兩倍標轉差)
        buy='很貴不要買'
        if pd.to_numeric(stockdf['成交價'][-1：]).values[0] < stockAverage - (2*stockSTD):
            buy = '這支股票現在很便宜喔!'
            
        # 顯示結果
        print("成交價 = ' + stockdf['成交價'][-1:].values[0])
        print('\n中間價 = ' + str(stockAverage))
        print('\線距 = ' + str(stockSTD))
        print(buy)
    else:
        print('請求失敗，請您的股票代號')

Standard_Deviation(stocknumber='2081.tw')
           


    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    app.run()
