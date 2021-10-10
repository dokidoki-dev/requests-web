import hashlib
from flask import Flask, request, Response
import settings
from web_backend.env_variable.views import env_variable
from web_backend.user.view import user
import json
from mysql.pymysql import SQLMysql

app = Flask(__name__)


lists = ['/login', '/env']


@app.before_request
def interceptor():
    url = request.path
    for i in range(len(lists)):
        if lists[i] == url:
            return
    uuid = request.cookies.get('uuid', None)
    username = request.cookies.get('username', None)
    if uuid is None or username is None:
        data = {
            "object": None,
            "msg": "用户未登录！",
            "code": 9200,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')
    # 判断用户数据是否正确
    s = SQLMysql()
    sql = "select u_id, u_password, u_salt from user_info where u_name=%s"
    is_null = s.query_one(sql, [username, ])
    if is_null is None:
        data = {
            "object": None,
            "msg": "用户未登录！",
            "code": 9201,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')
    user_uuid = hashlib.md5((str(is_null[0]) + is_null[2]).encode('utf-8')).hexdigest()
    if user_uuid != uuid:
        data = {
            "object": None,
            "msg": "用户未登录！",
            "code": 9202,
            "result": False,
            "status": "success"
        }
        return Response(json.dumps(data), content_type='application/json')


def create_app():
    # 导入配置文件
    app.config.from_object(settings.Development)
    # 注册蓝图
    app.register_blueprint(user)
    app.register_blueprint(env_variable)
    return app
