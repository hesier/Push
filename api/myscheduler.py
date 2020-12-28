# -*- coding: utf-8 -*-
import uuid
import time

from flask import current_app

from wechat import *
import redis_util as r


def add_send_text(date, user, content):
    """添加 text 推送"""
    current_app.apscheduler.scheduler.add_job(send_text, 'date', run_date=date, args=[user, content])


def add_send_template(date, user, content):
    """添加 template 推送"""
    current_app.apscheduler.scheduler.add_job(send_template, 'date', run_date=date, args=[user, content])


def add_send_now_template(user, content):
    """立刻发送 template 推送"""
    current_app.apscheduler.scheduler.add_job(send_template, 'date', args=[user, content])


def add_cron_template(cron, user, content):
    """添加 cron 的 template 推送"""

    uid = str(uuid.uuid4()).replace('-', '')
    #  插入redis
    r.add_hash(user, uid, {
        'create_time': time.strftime("%Y-%m-%d %H:%M", time.localtime()),
        'run_time': '',
        'uid': uid,
        'cron': cron,
        'status': 'on',
        'content': content
    })
    return add_cron_job(cron, user, uid)


def pause_send_job(user, uid):
    """暂停 推送任务"""
    current_app.apscheduler.scheduler.remove_job(uid)
    send_value = r.get_hash(user, uid)
    send_value['status'] = 'off'
    r.add_hash(user, uid, send_value)


def resume_send_job(user, uid):
    """恢复 推送任务"""
    send_value = r.get_hash(user, uid)
    send_value['status'] = 'on'
    r.add_hash(user, uid, send_value)
    cron = send_value['cron']

    return add_cron_job(cron, user, uid)


def add_cron_job(cron, user, uid):
    crons = cron.split(' ')
    if len(crons) != 5:
        return False
    else:
        minute = crons[0]
        hour = crons[1]
        day = crons[2]
        month = crons[3]
        day_of_week = ''
        for week in crons[4]:
            if week.isdigit():
                week = str(int(week) - 1)
            day_of_week += week
    current_app.apscheduler.scheduler.add_job(send_cron_template,
                                              'cron',
                                              id=uid,
                                              minute=minute,
                                              hour=hour,
                                              day=day,
                                              month=month,
                                              day_of_week=day_of_week,
                                              args=[user, uid])
    return True


def remove_send_job(user, uid):
    """删除 推送任务"""
    send_value = r.get_hash(user, uid)
    if send_value['status'] == 'on':
        current_app.apscheduler.scheduler.remove_job(uid)
    r.del_hash(user, uid)


def get_send_job(user):
    """获取 推送任务"""
    all_list = r.get_all_hash(user)

    res = []
    for i in all_list:
        res.append(eval(i))

    return res
