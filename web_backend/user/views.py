import time
import base64
import ast
from flask import Blueprint, request, Response
import json
import mysql.pymysql as pymysql
import re
import hashlib
import settings
from web_backend.user import logic
from web_backend.logger_text.logger_text import log
from web_backend.jwt_token.jwt_token import JWT_USER

user = Blueprint('user', __name__, url_prefix="/api/v1/user")

# 日志处理
logger = log()


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
        logger.debug("request.json:" + str(request.json))
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    username = str(request.json.get('username', None)).lower()
    password = request.json.get('password', None)
    if username is None or password is None:
        logger.debug("request.json:" + str(request.json))
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 查询用户是否存在
    s = pymysql.SQLMysql()
    sql = "select u_id, u_name, u_password, u_salt, is_active, is_delete from user_info where u_name = %s"
    logger.debug("select u_id, u_name, u_password, u_salt, is_active, is_delete from user_info where u_name={}".format(username))
    is_null = s.query_one(sql, [username, ])
    logger.debug("查询用户信息：" + str(is_null))
    if is_null is None:
        data["code"] = 9998
        data["msg"] = "用户名或密码错误"
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    if is_null[4] == 0:
        data["code"] = 9997
        data["msg"] = "账户已禁用，禁止登录！"
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    if is_null[5] == 1:
        data["code"] = 9996
        data["msg"] = "账户已注销，禁止登录！"
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 加密用户密码
    password = hashlib.sha256((password + is_null[3]).encode('utf-8')).hexdigest()
    logger.debug("密码比对：" + "用户输入密码：" + str(password) + " 用户保存的密码：" + str(is_null[2]) + " 比对结果：" + str(password == is_null[2]))
    # 比对用户密码
    if password == is_null[2]:
        data["code"] = 9000
        data["msg"] = "账号登录成功！"
        data["result"] = True
        # header = {
        #     "Access-Control-Allow-Origin": "*",
        #     "Access-Control-Allow-Credentials": "true"
        # }
        response = Response(json.dumps(data), content_type='application/json')
        # 处理uuid，加密
        uuid = hashlib.md5((is_null[1] + is_null[2] + str(is_null[0]) + is_null[3]).encode('utf-8')).hexdigest()
        response.set_cookie('uuid', uuid, max_age=settings.Config.cookies_timeout, domain='dev-web.com')
        response.set_cookie('username', is_null[1], max_age=settings.Config.cookies_timeout, domain='dev-web.com')
        logger.debug("uuid:" + str(uuid))
        logger.info("返回信息" + str(data))
        # 如果开启jwt，使用jwt方式，生成token，并且返回
        if settings.Config.jwt_on == 1:
            token = JWT_USER.create_token({
                "uuid": uuid,
                "username": is_null[1],
                "tmp": int(round(time.time() * 1000))  # 当前token生成时间
            })
            response.set_cookie('token', token, max_age=settings.Config.cookies_timeout, domain='dev-web.com')
        return response
    else:
        data["code"] = 9995
        data["msg"] = "账号或密码错误！"
        logger.info("返回信息" + str(data))
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
        logger.debug("request.json: " + str(request.json))
        logger.info("返回信息" + str(data))
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
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 查询用户是否存在
    s = pymysql.SQLMysql()
    sql = "select u_name, u_password, u_salt, is_delete from user_info where u_name = %s"
    logger.debug("select u_name, u_password, u_salt, is_delete from user_info where u_name = {}".format(username[0]))
    is_null = s.query_one(sql, [username[0], ])
    logger.debug("查询信息：" + str(is_null))
    if is_null:
        if is_null[3] == 1:
            data["msg"] = "当前用户已注销，不支持重新注册"
            data["code"] = 9993
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        data["msg"] = "当前用户已注册"
        data["code"] = 9992
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 注册
    # 加密密码
    # 生成随机密码盐
    salt = logic.hash_salt()
    password = hashlib.sha256((password[0] + salt).encode('utf-8')).hexdigest()
    sql = "insert into user_info (u_name, u_password, u_salt, u_phone, create_time) values (%s, %s, %s, %s, now())"
    logger.debug("insert into user_info (u_name, u_password, u_salt, u_phone, create_time) values ({}, {}, {}, {}, now())".format(username[0], password, salt, phone[0]))
    is_ok = s.create_one(sql, [(username[0]), password, salt, (phone[0]), ])
    if is_ok:
        data["msg"] = "账户注册成功"
        data["code"] = 9991
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "未知异常"
        data["code"] = 9990
        logger.info("返回信息" + str(data))
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
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    data["code"] = 9898
    data["msg"] = "用户已退出！"
    data["result"] = True
    response = Response(json.dumps(data), content_type='application/json')
    response.delete_cookie('uuid')
    response.delete_cookie('username')
    response.delete_cookie('token')
    logger.info("返回信息" + str(data))
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
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 10, type=int)
    # 根据jwt开启方式，判断走哪种方式读取用户信息
    u_name = None
    if settings.Config.jwt_on == 1:
        # 判断是否管理员
        # token此处一定不会为空
        token = request.cookies.get("token", None)
        token_payload = base64.b64decode(token.split(".")[1]).decode()
        token_payload = ast.literal_eval(token_payload)
        u_name = token_payload["username"]
    else:
        u_name = request.cookies.get('username')
    select = "select is_admin from user_info where u_name=%s and is_delete=0 and is_active=1"
    logger.debug("select is_admin from user_info where u_name={} and is_delete=0 and is_active=1".format(u_name))
    s = pymysql.SQLMysql()
    is_null = s.query_one(select, [u_name, ])
    logger.debug("查询结果：" + str(is_null))
    if is_null is None:
        data["code"] = 9398
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    if is_null[0] == 1:
        sql = "select u_name, u_phone, is_active from user_info where is_delete=0 limit %s, %s"
        logger.debug("select u_name, u_phone, is_active from user_info where is_delete=0 limit {}, {}".format((page-1), limit))
        list_n = s.query_all(sql, [(page - 1), limit, ])
        logger.debug("查询信息：" + str(list_n))
        if not list_n:
            # 理论上不会出现此种情况
            data["is_admin"] = True
            data["code"] = 9199
            data["msg"] = "查询成功"
            data["result"] = True
            logger.info("返回信息" + str(data))
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
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    elif is_null[0] == 0:
        sql = "select u_name, u_phone, is_active from user_info where is_delete=0 and is_active=1 and u_name=%s"
        logger.debug("select u_name, u_phone, is_active from user_info where is_delete=0 and is_active=1 and u_name={}".format(u_name))
        list_p = s.query_one(sql, [u_name, ])
        logger.debug("查询信息：" + str(list_p))
        if list_p is None:
            # 理论上不会出现此种情况
            data["is_admin"] = False
            data["msg"] = "查询成功"
            data["code"] = 9199
            data["result"] = True
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        username, phone, is_active = list_p
        data = {
            "object": {
                "username": username,
                "password": "********",
                "phone": phone,
                "active": True if is_active == 1 else False
            },
            "is_admin": False,
            "msg": "查询成功",
            "code": 9197,
            "result": True
        }
        logger.info("返回信息" + str(data))
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
        logger.debug("request.json: " + str(request.json))
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    username = request.json.get('username', "")
    pattern = re.compile(r'^[a-zA-Z][a-zA-Z0-9_]{4,15}$')
    username = pattern.search(str(username))
    if username is None:
        data["msg"] = "填写的信息校验不通过"
        data["code"] = 9599
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = pymysql.SQLMysql()
    # 查询当前用户是否存在
    sl = "select username from user_info where u_name=%s and is_delete=0"
    logger.debug("select username from user_info where u_name={} and is_delete=0".format(username[0]))
    is_null = s.query_one(sl, [username[0], ])
    logger.debug("查询信息：" + str(is_null))
    if is_null is None:
        data["msg"] = "用户删除失败"
        data["code"] = 9598
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 根据jwt开启方式，判断走哪种方式读取用户信息
    user_name = None
    if settings.Config.jwt_on == 1:
        # 判断是否管理员
        # token此处一定不会为空
        token = request.cookies.get("token", None)
        token_payload = base64.b64decode(token.split(".")[1]).decode()
        token_payload = ast.literal_eval(token_payload)
        user_name = token_payload["username"]
    else:
        user_name = request.cookies.get('username')
    select = "select is_admin from user_info where u_name=%s and is_delete=0"
    sql = "update user_info set is_delete=1, delete_time=now() where u_name=%s and is_delete=0"
    logger.debug("select is_admin from user_info where u_name={} and is_delete=0".format(user_name))
    ok = s.query_one(select, [user_name, ])
    logger.debug("查询信息：" + str(ok))
    if ok is None:
        data["msg"] = "参数非法"
        data["code"] = 9597
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    if ok[0] == 1:
        # 说明是管理员
        logger.debug("update user_info set is_delete=1, delete_time=now() where u_name={} and is_delete=0".format(username[0]))
        nok = s.update_one(sql, [(username[0]), ])
        if nok:
            data["msg"] = "用户删除成功!"
            data["code"] = 9596
            data["result"] = True
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常!"
            data["code"] = 9595
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "权限不足"
        data["code"] = 9594
        logger.info("返回信息" + str(data))
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
        logger.debug("request.json: " + str(request.json))
        logger.info("返回信息" + str(data))
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
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 处理密码
    salt = logic.hash_salt()
    password = hashlib.sha256((password[0] + salt).encode('utf-8')).hexdigest()
    s = pymysql.SQLMysql()
    sql_s = "update user_info set u_password=%s, u_phone=%s, is_active=%s, u_salt=%s, modfiy_time=now() where u_name=%s and is_delete=0"
    # 根据jwt开启方式，判断走哪种方式读取用户信息
    user_name = None
    if settings.Config.jwt_on == 1:
        # 判断是否管理员
        # token此处一定不会为空
        token = request.cookies.get("token", None)
        token_payload = base64.b64decode(token.split(".")[1]).decode()
        token_payload = ast.literal_eval(token_payload)
        user_name = token_payload["username"]
    else:
        user_name = request.cookies.get('username')
    select = "select is_admin from user_info where u_name=%s and is_delete=0"
    logger.debug("select is_admin from user_info where u_name={} and is_delete=0".format(user_name))
    is_null = s.query_one(select, [user_name, ])
    logger.debug("查询信息：" + str(is_null))
    if is_null is None:
        data["msg"] = "参数非法"
        data["code"] = 9099
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    if is_null[0] == 1:
        # 说明是管理员
        logger.debug("update user_info set u_password={}, u_phone={}, is_active={}, u_salt={}, modfiy_time=now() where u_name={} and is_delete=0".format(password, phone[0], is_active[0], salt, username[0]))
        ok = s.update_one(sql_s, [password, (phone[0]), (is_active[0]), salt, (username[0]), ])
        if ok:
            data["msg"] = "修改成功"
            data["code"] = 9697
            data["result"] = True
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 9696
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    # 普通用户更新自己信息
    sql_p = "update user_info set u_password=%s, u_phone=%s, u_salt=%s, modfiy_time=now() where u_name=%s and is_delete=0 and is_active=1"
    logger.debug("update user_info set u_password=%s, u_phone=%s, u_salt=%s, modfiy_time=now() where u_name=%s and is_delete=0 and is_active=1".format(password, phone[0], salt, user_name))
    ok = s.update_one(sql_p, [password, (phone[0]), salt, user_name, ])
    if ok:
        data["msg"] = "修改成功"
        data["code"] = 9695
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "未知异常"
        data["code"] = 9694
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')


@user.route('/updatepd', methods=['POST'])
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
        logger.debug("request.json: " + str(request.json))
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    password_old = request.json.get('password_old', "")
    password_new = request.json.get('password_new', "")
    # 根据认证方式，读取用户名
    username = None
    if settings.Config.jwt_on == 1:
        token = request.cookies.get("token", None)
        token_payload = base64.b64decode(token.split(".")[1]).decode()
        token_payload = ast.literal_eval(token_payload)
        username = token_payload["username"]
    else:
        username = request.cookies.get('username', None)
    pattern = re.compile(r'^(?=.*\d)(?=.*[a-zA-Z]).{6,15}$')
    password_old = pattern.search(str(password_old))
    password_new = pattern.search(str(password_new))
    if password_old is None or password_new is None or not username:
        data["msg"] = "参数非法"
        data["code"] = 5999
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = pymysql.SQLMysql()
    sql_old = "select u_password, u_salt  from user_info where u_name=%s"
    logger.debug("select u_password, u_salt  from user_info where u_name={}".format(username))
    is_null = s.query_one(sql_old, [username, ])
    logger.debug("查询信息：" + str(is_null))
    # 比对密码
    password_old = hashlib.sha256(password_old[0] + is_null[1]).hexdigest()
    logger.debug("校验密码：" + "用户输入的旧密码：" + str(password_old) + " 数据库中的旧密码：" + str(is_null[0]) + " 校验结果：" + password_old == is_null[0])
    if password_old == is_null[0]:
        # 处理新密码
        salt = logic.hash_salt()
        password_new = hashlib.sha256(password_new[0] + salt).hexdigest()
        sql_new = "update user_info set u_password=%s, u_salt=%s where u_name=%s"
        logger.debug("update user_info set u_password={}, u_salt={} where u_name={}".format(password_new, salt, username))
        ok = s.update_one(sql_new, [password_new, salt, username, ])
        if ok:
            data["msg"] = "修改成功"
            data["code"] = 5998
            data["result"] = True
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 5997
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "密码错误"
        data["code"] = 5996
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')