import os
import feedparser
from dotenv import load_dotenv,set_key
import base64
import requests
import json
import hashlib
import hmac
import time
# from google.cloud import pubsub_v1
# from google.oauth2 import service_account
# from googleapiclient.discovery import build

# # 加载.env文件
load_dotenv()

## 从环境变量中获取配置
rss_url = os.getenv('RSS_URL')
webhook = os.getenv('webhook')
webhook_key = os.getenv('webhook_key')

def check_feed(rss_url):
    # 解析 RSS feed
    feed = feedparser.parse(rss_url)
    new_entry = feed.entries
    print(len(new_entry))
    # print(new_entry.title)
    # print(new_entry.link)
    # print(new_entry.summary)

    # 获取上次更新的标题
    last_entry_title = os.getenv('last_entry_title')
    # 获取上次更新的链接
    last_entry_link = os.getenv('last_entry_link')

    # 获取所有的信息
    for entry in new_entry:
        print(entry)
        print(entry.title)
        print(entry.link)
        print(entry.summary)
        print('------------------------')


        # 如果标题和链接都相同，则不发送消息
        if last_entry_title == entry.title and last_entry_link == entry.link:
            return 'No new entry'
        else:
            # 更新环境变量
            os.environ['last_entry_title'] = entry.title
            os.environ['last_entry_link'] = entry.link
            
            # 更新.env文件
            set_key('.env', 'last_entry_title', entry.title)
            set_key('.env', 'last_entry_link', entry.link)

            # 发送消息
            webhook_send(webhook, webhook_key, entry)
            # return 'Sent message'

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

if __name__ == '__main__':
    # 获取环境变量

    check_feed(rss_url)
