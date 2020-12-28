# -*- coding: utf-8 -*-
import datetime
import requests
import time
import redis_util as r
import dingtalk as d

from config import CONFIG

appid = CONFIG['wechat']['appid']
secret = CONFIG['wechat']['secret']
template_id = CONFIG['wechat']['template_id']
dingtalk_on = CONFIG['dingtalk']['on']

user_url = "https://api.weixin.qq.com/cgi-bin/user/get?access_token="
token_url = "https://api.weixin.qq.com/cgi-bin/token"
template_url = 'https://api.weixin.qq.com/cgi-bin/message/template/send?access_token='
text_url = 'https://api.weixin.qq.com/cgi-bin/message/custom/send?access_token='

text_body = '{"touser":"%s","text":{"content":"%s"},"msgtype":"text"}'

template_body = '{"touser":"%s",' \
           '"template_id":"%s",' \
           '"data": {"message": {' \
           '"value":"%s"}}}'


def send_text(user, content):
    """推送 text """
    body = text_body % (user, content)
    response = requests.post(text_url + access_token(), data=body.encode("utf-8"))
    if dingtalk_on:
        d.send_text(content)
    if eval(response.text)['errcode'] == 0:
        return True
    else:
        return False


def send_template(user, content):
    """推送 template """
    body = template_body % (user, template_id, content)
    response = requests.post(template_url + access_token(), data=body.encode("utf-8"))
    if dingtalk_on:
        d.send_text(content)
    if eval(response.text)['errcode'] == 0:
        return True
    else:
        return False


def send_cron_template(user, uid):
    """推送 template """
    send_value = r.get_hash(user, uid)

    body = template_body % (user, template_id, send_value['content'])
    response = requests.post(template_url + access_token(), data=body.encode("utf-8"))
    if dingtalk_on:
        d.send_text(send_value['content'])
    if eval(response.text)['errcode'] == 0:
        send_value['run_time'] = time.strftime("%Y-%m-%d %H:%M", time.localtime())  # 更新执行时间
        r.add_hash(user, uid, send_value)
        return True
    else:
        return False


def refresh_token():
    """刷新 token """
    url = token_url + "?appid=" + appid + "&secret=" + secret + "&grant_type=client_credential"
    response = requests.get(url)
    res = eval(response.text)
    if res['access_token']:
        r.add_string('access_token', res['expires_in'], res['access_token'])  # 将 access_token 放入 redis
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M') + ' - 刷新 access_token 完成')
        init_user()  # 刷新关注用户的openid
        return True
    else:
        return False


def init_user():
    """刷新关注的用户"""
    response = requests.get(user_url + access_token())
    res = eval(response.text)
    if res['data']['openid']:
        r.del_name('openid')  # 先清空
        r.add_set('openid', *set(res['data']['openid']))  # 插入 openid


def user_exist(openid):
    """判断用户 openid 是否存在"""
    return r.is_set_exist('openid', openid)


def job_exist(openid, uid):
    """判断用户的推送任务是否存在"""
    return r.is_hash_exist(openid, uid)


def access_token():
    """从 redis 中获取当前的 token """
    return r.get_string('access_token')
