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
    if username is None or password is None:
        data = {
            "object": None,
            "msg": "用户名或密码错误",
            "code": 9999,
            "result": False
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
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    if is_null[3] == 0:
        data = {
            "object": None,
            "msg": "账户已禁用，禁止登录！",
            "code": 9997,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    if is_null[4] == 1:
        data = {
            "object": None,
            "msg": "账户已注销，禁止登录！",
            "code": 9996,
            "result": False
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
            "result": True
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
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')


@user.route('/user_list/resigter', methods=["POST"])
def res_user():
    # 只支持注册普通用户
    username = request.json.get('username', "").lower()
    password = request.json.get('password', "")
    phone = request.json.get('phone', "")
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$')
    username = pattern.search(str(username))
    pattern = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z]).{6,15}$')
    password = pattern.search(str(password))
    pattern = re.compile(r'^(13|14|15|17|18|19)[0-9]{9}$')
    phone = pattern.search(str(phone))
    if username is None or password is None or phone is None:
        data = {
            "object": None,
            "msg": "填写的用户信息校验不通过",
            "code": 9994,
            "result": False
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
                "result": False
            }
            return Response(json.dumps(data), content_type='application/json')
        data = {
            "object": None,
            "msg": "当前用户已注册",
            "code": 9992,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    # 注册
    # 加密密码
    # 生成随机密码盐
    salt = logic.hash_salt()
    password = hashlib.sha256((password[0] + salt).encode('utf-8')).hexdigest()
    sql = "insert into user_info (u_name, u_password, u_salt, u_phone, create_time) values (%s, %s, %s, %s, now())"
    is_ok = s.create_one(sql, [(username[0]), password, salt, (phone[0]), ])
    if is_ok:
        data = {
            "object": None,
            "msg": "账户注册成功",
            "code": 9991,
            "result": True
        }
        return Response(json.dumps(data), content_type='application/json')
    else:
        data = {
            "object": None,
            "msg": "未知异常",
            "code": 9990,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')


@user.route('/logout', methods=['POST'])
def logout():
    username = request.cookies.get('username', None)
    if username is None:
        data = {
            "object": None,
            "msg": "用户未登录，无需退出！",
            "code": 9899,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    data = {
        "object": None,
        "msg": "用户已退出！",
        "code": 9898,
        "result": True
    }
    response = Response(json.dumps(data), content_type='application/json')
    response.delete_cookie('uuid')
    response.delete_cookie('username')
    return response


@user.route('/user_list', methods=['GET'])
def user_list():
    page = request.args.get('page', 0)
    limit = request.args.get('limit', 10)
    is_active = request.args.get('is_active', 1)
    pattern = re.compile(r'^[0-9]{1,50}$')
    page = pattern.search(str(page))
    limit = pattern.search(str(limit))
    is_active = pattern.search(str(is_active))
    if page is None or limit is None or is_active is None:
        data = {
            "object": None,
            "msg": "参数非法",
            "code": 9399,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    # 判断是否管理员
    u_name = request.cookies.get('username')
    select = "select is_admin from user_info where u_name=%s and is_delete=0 and is_active=1"
    s = pymysql.SQLMysql()
    is_null = s.query_one(select, [u_name, ])
    if is_null is None:
        data = {
            "object": None,
            "msg": "参数非法",
            "code": 9398,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    if is_null[0] == 1:
        sql = "select u_name, u_phone, is_active from user_info where is_delete=0 limit %s, %s"
        list_n = s.query_all(sql, [int(page[0]), int(limit[0]), ])
        if not list_n:
            data = {
                "object": None,
                "is_admin": True,
                "msg": "查询成功",
                "code": 9199,
                "result": True
            }
            return Response(json.dumps(data), content_type='application/json')
        context = []
        for i in range(len(list_n)):
            username, phone, is_active = list_n[i]
            context.append({
                "username": username,
                "password": "********",
                "phone": phone,
                "active": True if is_active == 1 else False
            })
        data = {
            "object": context,
            "is_admin": True,
            "msg": "查询成功",
            "code": 9198,
            "result": True
        }
        return Response(json.dumps(data), content_type='application/json')
    elif is_null[0] == 0:
        sql = "select u_name, u_phone from user_info where is_delete=0 and is_active=1 and u_name=%s"
        list_p = s.query_one(sql, [u_name, ])
        if list_p is None:
            data = {
                "object": None,
                "is_admin": True,
                "msg": "查询成功",
                "code": 9199,
                "result": True
            }
            return Response(json.dumps(data), content_type='application/json')
        username, phone = list_p
        data = {
            "object": {
                "username": username,
                "password": "********",
                "phone": phone
            },
            "is_admin": False,
            "msg": "查询成功",
            "code": 9197,
            "result": True
        }
        return Response(json.dumps(data), content_type='application/json')


@user.route('/user_list/delete', methods=['POST'])
def user_delete():
    username = request.json.get('username', "")
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$')
    username = pattern.search(str(username))
    if username is None:
        data = {
            "object": None,
            "msg": "填写的信息校验不通过",
            "code": 9599,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    s = pymysql.SQLMysql()
    # 查询当前用户是否存在
    sl = "select username from user_info where u_name=%s and is_delete=0"
    is_null = s.query_one(sl, [username[0]])
    if is_null is None:
        data = {
            "object": None,
            "msg": "用户删除失败",
            "code": 9598,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    # 判断是否管理员
    user_name = request.cookies.get('username')
    select = "select is_admin from user_info where u_name=%s and is_delete=0"
    sql = "update user_info set is_delete=1, delete_time=now() where u_name=%s and is_delete=0"
    ok = s.query_one(select, [user_name, ])
    if ok is None:
        data = {
            "object": None,
            "msg": "参数非法",
            "code": 9597,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    if ok[0] == 1:
        # 说明是管理员
        nok = s.update_one(sql, [(username[0]), ])
        if nok:
            data = {
                "object": None,
                "msg": "用户删除成功!",
                "code": 9596,
                "result": True
            }
            return Response(json.dumps(data), content_type='application/json')
        else:
            data = {
                "object": None,
                "msg": "未知异常!",
                "code": 9595,
                "result": False
            }
            return Response(json.dumps(data), content_type='application/json')
    else:
        data = {
            "object": None,
            "msg": "权限不足",
            "code": 9594,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')


@user.route('/user_list/update', methods=['POST'])
def user_update():
    username = request.json.get('username', "")
    password = request.json.get('password', "")
    phone = request.json.get('phone', "")
    is_active = request.json.get('is_active', 1)
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$')
    username = pattern.search(str(username))
    pattern = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z]).{6,15}$')
    password = pattern.search(str(password))
    pattern = re.compile(r'^(13|14|15|17|18|19)[0-9]{9}$')
    phone = pattern.search(str(phone))
    pattern = re.compile(r'^[0-9]$')
    is_active = pattern.search(str(is_active))
    if username is None or password is None or phone is None or is_active is None:
        data = {
            "object": None,
            "msg": "填写的用户信息校验不通过",
            "code": 9699,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    # 处理密码
    salt = logic.hash_salt()
    password = hashlib.sha256((password[0] + salt).encode('utf-8')).hexdigest()
    s = pymysql.SQLMysql()
    sql_s = "update user_info set u_password=%s, u_phone=%s, is_active=%s, u_salt=%s, modfiy_time=now() where u_name=%s and is_delete=0"
    # 判断是否管理员
    user_name = request.cookies.get('username')
    select = "select is_admin from user_info where u_name=%s and is_delete=0"
    is_null = s.query_one(select, [user_name, ])
    if is_null is None:
        data = {
            "object": None,
            "msg": "参数非法",
            "code": 9099,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
    if is_null[0] == 1:
        # 说明是管理员
        ok = s.update_one(sql_s, [password, (phone[0]), (is_active[0]), salt, (username[0]), ])
        if ok:
            data = {
                "object": None,
                "msg": "修改成功",
                "code": 9697,
                "result": True
            }
            return Response(json.dumps(data), content_type='application/json')
        else:
            data = {
                "object": None,
                "msg": "未知异常",
                "code": 9696,
                "result": False
            }
            return Response(json.dumps(data), content_type='application/json')
    # 普通用户更新自己信息
    sql_p = "update user_info set u_password=%s, u_phone=%s, u_salt=%s, modfiy_time=now() where u_name=%s and is_delete=0 and is_active=1"
    ok = s.update_one(sql_p, [password, (phone[0]), salt, user_name, ])
    if ok:
        data = {
            "object": None,
            "msg": "修改成功",
            "code": 9695,
            "result": True
        }
        return Response(json.dumps(data), content_type='application/json')
    else:
        data = {
            "object": None,
            "msg": "未知异常",
            "code": 9694,
            "result": False
        }
        return Response(json.dumps(data), content_type='application/json')
