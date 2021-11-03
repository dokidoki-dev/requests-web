from flask import Blueprint, request, Response
import json
import mysql.pymysql as pymysql
import re
import hashlib
from web_backend.user import logic

user = Blueprint('user', __name__)


@user.route('/login', methods=['POST'])
def login():
    data = {
        "object": None,
        "msg": "缺少参数",
        "code": 10000,
        "result": False
    }
    # 处理没有传参的问题
    if not request.json:
        return Response(json.dumps(data), content_type='application/json')
    username = str(request.json.get('username', None)).lower()
    password = request.json.get('password', None)
    if username is None or password is None:
        return Response(json.dumps(data), content_type='application/json')
    # 查询用户是否存在
    s = pymysql.SQLMysql()
    sql = "select u_name, u_password, u_salt, is_active, is_delete, u_id from user_info where u_name = %s"
    is_null = s.query_one(sql, [username, ])
    if is_null is None:
        data["code"] = 9998
        data["msg"] = "用户名或密码错误"
        return Response(json.dumps(data), content_type='application/json')
    if is_null[3] == 0:
        data["code"] = 9997
        data["msg"] = "账户已禁用，禁止登录！"
        return Response(json.dumps(data), content_type='application/json')
    if is_null[4] == 1:
        data["code"] = 9996
        data["msg"] = "账户已注销，禁止登录！"
        return Response(json.dumps(data), content_type='application/json')
    # 加密用户密码
    password = hashlib.sha256((password + is_null[2]).encode('utf-8')).hexdigest()
    # 比对用户密码
    if password == is_null[1]:
        data["code"] = 9000
        data["msg"] = "账号登录成功！"
        data["result"] = True
        response = Response(json.dumps(data), content_type='application/json')
        # 处理uuid，加密
        uuid = hashlib.md5((str(is_null[5]) + is_null[2]).encode('utf-8')).hexdigest()
        response.set_cookie('uuid', uuid, max_age=86400, domain='127.0.0.1')
        response.set_cookie('username', is_null[0])
        return response
    else:
        data["code"] = 9995
        data["msg"] = "账号或密码错误！"
        return Response(json.dumps(data), content_type='application/json')


@user.route('/user_list/resigter', methods=["POST"])
def res_user():
    data = {
        "object": None,
        "msg": "缺少参数",
        "code": 10000,
        "result": False
    }
    # 处理没有传参的问题
    if not request.json:
        return Response(json.dumps(data), content_type='application/json')
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
        data["code"] = 9994
        data["msg"] = "填写的用户信息校验不通过"
        return Response(json.dumps(data), content_type='application/json')
    # 查询用户是否存在
    s = pymysql.SQLMysql()
    sql = "select u_name, u_password, u_salt, is_delete from user_info where u_name = %s"
    is_null = s.query_one(sql, [username[0], ])
    if is_null:
        if is_null[3] == 1:
            data["msg"] = "当前用户已注销，不支持重新注册"
            data["code"] = 9993
            return Response(json.dumps(data), content_type='application/json')
        data["msg"] = "当前用户已注册"
        data["code"] = 9992
        return Response(json.dumps(data), content_type='application/json')
    # 注册
    # 加密密码
    # 生成随机密码盐
    salt = logic.hash_salt()
    password = hashlib.sha256((password[0] + salt).encode('utf-8')).hexdigest()
    sql = "insert into user_info (u_name, u_password, u_salt, u_phone, create_time) values (%s, %s, %s, %s, now())"
    is_ok = s.create_one(sql, [(username[0]), password, salt, (phone[0]), ])
    if is_ok:
        data["msg"] = "账户注册成功"
        data["code"] = 9991
        data["result"] = True
        return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "未知异常"
        data["code"] = 9990
        return Response(json.dumps(data), content_type='application/json')


@user.route('/logout', methods=['POST'])
def logout():
    data = {
        "object": None,
        "msg": "用户未登录，无需退出！",
        "code": 9899,
        "result": False
    }
    username = request.cookies.get('username', None)
    if username is None:
        return Response(json.dumps(data), content_type='application/json')
    data["code"] = 9898
    data["msg"] = "用户已退出！"
    data["result"] = True
    response = Response(json.dumps(data), content_type='application/json')
    response.delete_cookie('uuid')
    response.delete_cookie('username')
    return response


@user.route('/user_list', methods=['GET'])
def user_list():
    data = {
        "object": None,
        "is_admin": False,
        "msg": "参数非法",
        "code": 9399,
        "result": False
    }
    page = request.args.get('page', 0)
    limit = request.args.get('limit', 10)
    is_active = request.args.get('is_active', 1)
    pattern = re.compile(r'^[0-9]{1,50}$')
    page = pattern.search(str(page))
    limit = pattern.search(str(limit))
    is_active = pattern.search(str(is_active))
    if page is None or limit is None or is_active is None:
        return Response(json.dumps(data), content_type='application/json')
    # 判断是否管理员
    u_name = request.cookies.get('username')
    select = "select is_admin from user_info where u_name=%s and is_delete=0 and is_active=1"
    s = pymysql.SQLMysql()
    is_null = s.query_one(select, [u_name, ])
    if is_null is None:
        data["code"] = 9398
        return Response(json.dumps(data), content_type='application/json')
    if is_null[0] == 1:
        sql = "select u_name, u_phone, is_active from user_info where is_delete=0 limit %s, %s"
        list_n = s.query_all(sql, [int(page[0]), int(limit[0]), ])
        if not list_n:
            data["is_admin"] = True
            data["code"] = 9199
            data["msg"] = "查询成功"
            data["result"] = True
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
        data["object"] = context
        data["is_admin"] = True
        data["msg"] = "查询成功"
        data["code"] = 9198
        data["result"] = True
        return Response(json.dumps(data), content_type='application/json')
    elif is_null[0] == 0:
        sql = "select u_name, u_phone from user_info where is_delete=0 and is_active=1 and u_name=%s"
        list_p = s.query_one(sql, [u_name, ])
        if list_p is None:
            data["is_admin"] = True
            data["msg"] = "查询成功"
            data["code"] = 9199
            data["result"] = True
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
    data = {
        "object": None,
        "msg": "缺少参数",
        "code": 10000,
        "result": False
    }
    # 处理没有传参的问题
    if not request.json:
        return Response(json.dumps(data), content_type='application/json')
    username = request.json.get('username', "")
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$')
    username = pattern.search(str(username))
    if username is None:
        data["msg"] = "填写的信息校验不通过"
        data["code"] = 9599
        return Response(json.dumps(data), content_type='application/json')
    s = pymysql.SQLMysql()
    # 查询当前用户是否存在
    sl = "select username from user_info where u_name=%s and is_delete=0"
    is_null = s.query_one(sl, [username[0]])
    if is_null is None:
        data["msg"] = "用户删除失败"
        data["code"] = 9598
        return Response(json.dumps(data), content_type='application/json')
    # 判断是否管理员
    user_name = request.cookies.get('username')
    select = "select is_admin from user_info where u_name=%s and is_delete=0"
    sql = "update user_info set is_delete=1, delete_time=now() where u_name=%s and is_delete=0"
    ok = s.query_one(select, [user_name, ])
    if ok is None:
        data["msg"] = "参数非法"
        data["code"] = 9597
        return Response(json.dumps(data), content_type='application/json')
    if ok[0] == 1:
        # 说明是管理员
        nok = s.update_one(sql, [(username[0]), ])
        if nok:
            data["msg"] = "用户删除成功!"
            data["code"] = 9596
            data["result"] = True
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常!"
            data["code"] = 9595
            return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "权限不足"
        data["code"] = 9594
        return Response(json.dumps(data), content_type='application/json')


@user.route('/user_list/update', methods=['POST'])
def user_update():
    data = {
        "object": None,
        "msg": "缺少参数",
        "code": 10000,
        "result": False
    }
    # 处理没有传参的问题
    if not request.json:
        return Response(json.dumps(data), content_type='application/json')
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
        data["msg"] = "填写的用户信息校验不通过"
        data["code"] = 9699
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
        data["msg"] = "参数非法"
        data["code"] = 9099
        return Response(json.dumps(data), content_type='application/json')
    if is_null[0] == 1:
        # 说明是管理员
        ok = s.update_one(sql_s, [password, (phone[0]), (is_active[0]), salt, (username[0]), ])
        if ok:
            data["msg"] = "修改成功"
            data["code"] = 9697
            data["result"] = True
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 9696
            return Response(json.dumps(data), content_type='application/json')
    # 普通用户更新自己信息
    sql_p = "update user_info set u_password=%s, u_phone=%s, u_salt=%s, modfiy_time=now() where u_name=%s and is_delete=0 and is_active=1"
    ok = s.update_one(sql_p, [password, (phone[0]), salt, user_name, ])
    if ok:
        data["msg"] = "修改成功"
        data["code"] = 9695
        data["result"] = True
        return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "未知异常"
        data["code"] = 9694
        return Response(json.dumps(data), content_type='application/json')


@user.route('/user/updatepd', methods=['POST'])
def user_updatepd():
    # 处理传参
    data = {
        "object": None,
        "msg": "缺少参数",
        "code": 10000,
        "result": False
    }
    # 处理没有传参的问题
    if not request.json:
        return Response(json.dumps(data), content_type='application/json')
    password_old = request.json.get('password_old', "")
    password_new = request.json.get('password_new', "")
    username = request.cookies.get('username', None)
    pattern = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z]).{6,15}$')
    password_old = pattern.search(str(password_old))
    password_new = pattern.search(str(password_new))
    if password_old is None or password_new is None or not username:
        data["msg"] = "参数非法"
        data["code"] = 5999
        return Response(json.dumps(data), content_type='application/json')
    s = pymysql.SQLMysql()
    sql_old = "select u_password, u_salt  from user_info where u_name=%s"
    is_null = s.query_one(sql_old, [username, ])
    # 比对密码
    password_old = hashlib.sha256(password_old[0] + is_null[1]).hexdigest()
    if password_old == is_null[0]:
        # 处理新密码
        salt = logic.hash_salt()
        password_new = hashlib.sha256(password_new[0] + salt).hexdigest()
        sql_new = "update user_info set u_password=%s, u_salt=%s where u_name=%s"
        ok = s.update_one(sql_new, [password_new, salt, username, ])
        if ok:
            data["msg"] = "修改成功"
            data["code"] = 5998
            data["result"] = True
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 5997
            return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "密码错误"
        data["code"] = 5996
        return Response(json.dumps(data), content_type='application/json')