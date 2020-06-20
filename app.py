from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *

import random



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

# 處理訊息
@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    get = event.message.text
#event.gessage.text接收使用者文字資訊

    if(get == '?'):
        message = TextSendMessage(text = '?')
           

    line_bot_api.reply_message(event.reply_token, message)

if __name__ == "__main__":
    app.run()
