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

    # 读取上次更新的信息
    last_data = blob.download_as_text().strip() or '{}' 
    ldata = json.loads(last_data)

    # 获取上次更新的标题
    last_entry_title = ldata.get('LAST_ENTRY_TITLE')
    # 获取上次更新的链接
    last_entry_link = ldata.get('LAST_ENTRY_LINK')


    # 获取所有的信息
    for entry in new_entry:
        if last_entry_title == entry.title and last_entry_link == entry.link:
            return 'No new entry'
        else:
            webhook_send(webhook, webhook_key, entry)
            variables = {
                'LAST_ENTRY_TITLE': entry.title,
                'LAST_ENTRY_LINK': entry.link
            }
            # 更新上次更新的信息
            blob.upload_from_string(json.dumps(variables))

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
