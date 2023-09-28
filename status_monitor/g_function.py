import functions_framework
import requests
import json
import os
import feedparser
import time
import hmac
import hashlib
import base64



def check_feed(rss_url,webhook,webhook_key):
    # 解析 RSS feed
    feed = feedparser.parse(rss_url)
    new_entry = feed.entries

    # 获取所有的信息
    for entry in new_entry:
        webhook_send(webhook, webhook_key, entry)

    return("ok")

def gen_sign(timestamp, secret):
  # 拼接timestamp和secret
  string_to_sign = '{}\n{}'.format(timestamp, secret)
  hmac_code = hmac.new(string_to_sign.encode("utf-8"), digestmod=hashlib.sha256).digest()

  # 对结果进行base64处理
  sign = base64.b64encode(hmac_code).decode('utf-8')

  return sign

def webhook_send(webhook, webhook_key, message):
    # 生成签名
    timestamp = str(int(time.time()))
    
    sign = gen_sign(timestamp, webhook_key)

    # 构造 webhook url
    webhook_url = webhook

    # 构造消息
    content = {
        "timestamp": timestamp,        
        "sign": sign,  
        "msg_type": "interactive",
        "card": 
                {
                "elements": [
                    {
                    "tag": "markdown",
                    "content": message.summary + '\n' + '[Read more](' + message.link + ')'
                    }
                ],
                "header": {
                    "template": "blue",
                    "title": {
                    "content": message.title,
                    "tag": "plain_text"
                    }
                }
        }
    }
    # 发送消息
    r = requests.post(webhook_url, data=json.dumps(content), headers={'Content-Type': 'application/json'})

    #查看返回值
    # print(r.text)
    return(r.text)

@functions_framework.http
def hello_http(request):
    request_json = request.get_json(silent=True)
    request_args = request.args


    rss_url = os.getenv('RSS_URL')
    webhook = os.getenv('webhook')
    webhook_key = os.getenv('webhook_key')

    check_feed(rss_url,webhook,webhook_key)

    return("ok")
