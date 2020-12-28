# -*- coding: utf-8 -*-
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.redis import RedisJobStore
from gevent.pywsgi import WSGIServer

from myscheduler import *
from wechat import *

from flask import Flask, request
from flask_apscheduler import APScheduler

from config import CONFIG

ip = secret = CONFIG['server']['ip']
port = CONFIG['server']['port']


class APSchedulerConfig(object):

    SCHEDULER_TIMEZONE = 'Asia/Shanghai'
    # 存储位置
    SCHEDULER_JOBSTORES = {
        'default': RedisJobStore(host="localhost", port=6379, db=0, password='')
    }
    # 线程池配置
    SCHEDULER_EXECUTORS = {
        'default': {'type': 'threadpool', 'max_workers': 20}
    }


app = Flask(__name__)
app.config.from_object(APSchedulerConfig())


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/time/<string:openid>', methods=['GET', 'POST'])
def add_push(openid):
    """添加定时单次推送"""
    if not user_exist(openid):
        return {"code": 101, "msg": "user error"}
    if request.method == 'GET':
        message = request.args.get("message")
        send_time = request.args.get("time")
    else:
        message = request.get_json()['message']
        send_time = request.get_json()['time']
    add_send_template(send_time, openid, message)
    return {"code": 0, "msg": "ok"}


@app.route('/cron/<string:openid>', methods=['POST'])
def add_cron(openid):
    """添加 cron 推送"""
    if not user_exist(openid):
        return {"code": 101, "msg": "openId 不存在！"}
    message = request.get_json()['message']
    cron = request.get_json()['cron']

    if add_cron_template(cron, openid, message):
        return {"code": 0, "msg": "ok"}
    else:
        return {"code": 101, "msg": "cron error！"}


@app.route('/pause/<string:openid>', methods=['POST'])
def pause_cron(openid):
    """暂停 cron 推送"""
    if not user_exist(openid):
        return {"code": 101, "msg": "openId 不存在！"}

    uid = request.get_json()['uid']
    if not job_exist(openid, uid):
        return {"code": 101, "msg": "job error"}

    pause_send_job(openid, uid)
    return {"code": 0, "msg": "ok"}


@app.route('/resume/<string:openid>', methods=['POST'])
def resume_cron(openid):
    """重启 cron 推送"""
    if not user_exist(openid):
        return {"code": 101, "msg": "openId 不存在！"}

    uid = request.get_json()['uid']
    if not job_exist(openid, uid):
        return {"code": 101, "msg": "job error"}

    if resume_send_job(openid, uid):
        return {"code": 0, "msg": "ok"}
    else:
        return {"code": 101, "msg": "cron error"}


@app.route('/remove/<string:openid>', methods=['POST'])
def remove_cron(openid):
    """删除 cron 推送"""
    if not user_exist(openid):
        return {"code": 101, "msg": "openId 不存在！"}

    uid = request.get_json()['uid']
    if not job_exist(openid, uid):
        return {"code": 101, "msg": "job error"}

    remove_send_job(openid, uid)
    return {"code": 0, "msg": "ok"}


@app.route('/get/<string:openid>', methods=['GET', 'POST'])
def get_cron(openid):
    """获取 cron 推送列表"""
    if not user_exist(openid):
        return {"code": 101, "msg": "openId 不存在！"}

    return {'code': 0, 'data': get_send_job(openid)}


@app.route('/now/<string:openid>/<path:message>')
def send_now(openid, message):
    """立即推送"""
    if not user_exist(openid):
        return {"code": 101, "msg": "openId 不存在！r"}
    if send_template(openid, message):
        return {"code": 0, "msg": "ok"}
    else:
        return {"code": 101, "msg": "send error"}


if __name__ == '__main__':

    start = refresh_token()

    if not start:
        print("启动失败！")
        exit()
    print(f'Running on http://{ip}:{port}/')

    scheduler = APScheduler(BackgroundScheduler(timezone="Asia/Shanghai"))
    scheduler.init_app(app)
    scheduler.add_job(id='refresh_token', func=refresh_token, trigger='interval', seconds=7000, replace_existing=True)
    scheduler.start()
    http_server = WSGIServer((ip, port), app)
    http_server.serve_forever()
