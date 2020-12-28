# -*- coding: utf-8 -*-
import time
import hmac
import hashlib
import base64
import urllib.parse
import requests

from config import CONFIG

secret = CONFIG['dingtalk']['secret']
access_token = CONFIG['dingtalk']['access_token']

bot_url = "https://oapi.dingtalk.com/robot/send?access_token=" + access_token

text_msg = '{"msgtype":"text","text":{"content":"%s"}}'
markdown_msg = '{"msgtype":"markdown","markdown":{"title":"%s","text":"%s"}}'

headers = {'Content-Type': 'application/json'}


def send_text(content):
    """推送 text """
    body = text_msg % content
    requests.post(bot_url + get_sign(), data=body.encode("utf-8"), headers=headers)


def send_markdown(title, text):
    """推送 markdown """
    body = markdown_msg % (title, text)
    requests.post(bot_url + get_sign(), data=body.encode("utf-8"), headers=headers)


def get_sign():
    timestamp = str(round(time.time() * 1000))
    secret_enc = secret.encode('utf-8')
    string_to_sign = '{}\n{}'.format(timestamp, secret)
    string_to_sign_enc = string_to_sign.encode('utf-8')
    hmac_code = hmac.new(secret_enc, string_to_sign_enc, digestmod=hashlib.sha256).digest()
    sign = urllib.parse.quote_plus(base64.b64encode(hmac_code))
    return f'&timestamp={timestamp}&sign={sign}'
