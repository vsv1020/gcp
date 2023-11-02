import functions_framework
from google.cloud import storage
import requests
import json
import os
import feedparser
import time
import hmac
import hashlib
import base64
import datetime

def blob_init(bucket_name,file_name):
    # 初始化 Cloud Storage 客户端
    client = storage.Client()
    bucket = client.get_bucket(bucket_name)
    blob = bucket.blob(file_name)
    return blob


def check_feed(blob,rss_url,webhook,webhook_key):
    # 解析 RSS feed
    feed = feedparser.parse(rss_url)
    new_entry = feed.entries
    print(len(new_entry))

    # 读取上次更新的信息
    last_data = blob.download_as_text().strip() or '{}' 
    ldata = json.loads(last_data)

    info = []
    # 把title放到一个数组里面
    last_entry_title = []
    for d in ldata:
        last_entry_title.append(d['LAST_ENTRY_TITLE'])
        variables = {
            'LAST_ENTRY_TITLE': d['LAST_ENTRY_TITLE'],
            'LAST_ENTRY_LINK': d['LAST_ENTRY_LINK']
        }
        info.append(variables)
    
    
    # 获取所有的信息
    for entry in new_entry:

        # 将更新更新到一个数组里面
        if entry.title in last_entry_title:
            pass
        else:
            variables = {
                'LAST_ENTRY_TITLE': entry.title,
                'LAST_ENTRY_LINK': entry.link
            }
            info.append(variables)
            print("----------------------")
            webhook_send(webhook, webhook_key, entry)
            
    # 更新本次更新的信息
    blob.upload_from_string(json.dumps(info))
            
    return("ok")
    # 解析 RSS feed
    feed = feedparser.parse(rss_url)
    new_entry = feed.entries

    # 读取上次更新的信息
    last_data = blob.download_as_text().strip() or '{}' 
    ldata = json.loads(last_data)
    
    info = []
    # 获取所有的信息
    for entry in new_entry:

        # 将更新更新到一个数组

        for d in ldata:
            if d['LAST_ENTRY_TITLE'] == entry.title and d['LAST_ENTRY_LINK'] == entry.link:
                return 'No new entry'
                break
        else:
            variables = {
                'LAST_ENTRY_TITLE': entry.title,
                'LAST_ENTRY_LINK': entry.link
            }
            info.append(variables)
            webhook_send(webhook, webhook_key, entry)
            
    # 更新本次更新的信息
    blob.upload_from_string(json.dumps(info))
            
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
    bucket_name = os.getenv('BUCKET_NAME')
    file_name = os.getenv('FILE_NAME')

    blob = blob_init(bucket_name,file_name)
    check_feed(blob,rss_url,webhook,webhook_key)

    return("ok")


