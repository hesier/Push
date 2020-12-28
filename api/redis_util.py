# -*- coding: utf-8 -*-
import redis

from config import CONFIG


host = CONFIG['redis']['host']
port = CONFIG['redis']['port']
db = CONFIG['redis']['db']
password = CONFIG['redis']['password']

r = redis.StrictRedis(host=host, port=port, db=db, password=password, decode_responses=True)


def del_name(name):
    """删除 key"""
    return r.delete(name)


def add_string(name, time, values):
    """string 中添加元素"""
    return r.setex(name, time, values)


def get_string(name):
    """string 中获取元素"""
    return r.get(name)


def add_set(name, *values):
    """set 中添加元素"""
    return r.sadd(name, *values)


def is_set_exist(name, value):
    """判断 value 是否存在"""
    return r.sismember(name, value)


def add_hash(name, key, value):
    """hash 中添加元素"""
    return r.hset(name, key, str(value))


def get_hash(name, key):
    """hash 中获取元素"""
    return eval(r.hget(name, key))


def get_all_hash(name):
    """获取所有 hash，只有 value 值"""
    return r.hvals(name)


def del_hash(name, key):
    """hash 中删除元素"""
    return r.hdel(name, key)


def is_hash_exist(name, key):
    """判断 key 是否存在"""
    return r.hexists(name, key)

