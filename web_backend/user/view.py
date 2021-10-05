from datetime import datetime
from flask import Blueprint, request, Response
import json
import mysql.pymysql as pymysql
import re
import hashlib
from web_backend.user import logic


user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():
    username = request.json.get('username', None).lower()
    password = request.json.get('password', None)
    print(username, password)
    if username is None or password is None:
        data = {
            "object": None,
            "msg": "用户名或密码错误",
            "code": 9999,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')
    # 查询用户是否存在
    s = pymysql.SQLMysql()
    sql = "select u_name, u_password, u_salt, is_active, is_delete, u_id from user_info where u_name = %s"
    is_null = s.query_one(sql, [username, ])
    if is_null is None:
        data = {
            "object": None,
            "msg": "用户名或密码错误",
            "code": 9998,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')
    if is_null[3] == 0:
        data = {
            "object": None,
            "msg": "账户已禁用，禁止登录！",
            "code": 9997,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')
    if is_null[4] == 1:
        data = {
            "object": None,
            "msg": "账户已注销，禁止登录！",
            "code": 9996,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')
    # 加密用户密码
    password = hashlib.sha256((password + is_null[2]).encode('utf-8')).hexdigest()
    # 比对用户密码
    if password == is_null[1]:
        data = {
            "object": None,
            "msg": "账号登录成功！",
            "code": 9000,
            "result": True,
            "status": "success"
        }
        response = Response(json.dumps(data), content_type='application/json')
        # 处理uuid，加密
        uuid = hashlib.md5((str(is_null[5]) + is_null[2]).encode('utf-8')).hexdigest()
        response.set_cookie('uuid', uuid, max_age=86400, domain='127.0.0.1')
        response.set_cookie('username', is_null[0])
        return response
    else:
        data = {
            "object": None,
            "msg": "账号或密码错误！",
            "code": 9995,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')


@user.route('/resigter', methods=["POST"])
def res_user():
    # 只支持注册普通用户
    username = request.json.get('username', "").lower()
    password = request.json.get('password', "")
    phone = request.json.get('phone', "")
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$')
    username = pattern.search(username)
    pattern = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z]).{6,15}$')
    password = pattern.search(password)
    pattern = re.compile(r'^(13|14|15|17|18|19)[0-9]{9}$')
    phone = pattern.search(phone)
    if username is None or password is None or phone is None:
        data = {
            "object": None,
            "msg": "填写的用户信息校验不通过",
            "code": 9994,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')
    # 查询用户是否存在
    s = pymysql.SQLMysql()
    sql = "select u_name, u_password, u_salt, is_delete from user_info where u_name = %s"
    is_null = s.query_one(sql, [username[0], ])
    if is_null:
        if is_null[3] == 1:
            data = {
                "object": None,
                "msg": "当前用户已注销，不支持重新注册",
                "code": 9993,
                "result": False,
                "status": "success"
            }
            return Response(json.dumps(data), content_type='application/json')
        data = {
            "object": None,
            "msg": "当前用户已注册",
            "code": 9992,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')
    # 注册
    # 加密密码
    # 生成随机密码盐
    salt = logic.hash_salt()
    password = hashlib.sha256((password[0] + salt).encode('utf-8')).hexdigest()
    sql = "insert into user_info (u_name, u_password, u_salt, u_phone, create_time) values (%s, %s, %s, %s, %s)"
    is_ok = s.create_one(sql, [(username[0]), password, salt, (phone[0]), datetime.now(), ])
    if is_ok:
        data = {
            "object": None,
            "msg": "账户注册成功",
            "code": 9991,
            "result": True,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')
    else:
        data = {
            "object": None,
            "msg": "未知异常",
            "code": 9990,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')
