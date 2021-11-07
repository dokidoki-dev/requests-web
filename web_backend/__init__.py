import hashlib
from flask import Flask, request, Response
import settings
from web_backend.env_variable.views import env_variable
from web_backend.user.views import user
from web_backend.t_cases.views import test_cases
import json
from mysql.pymysql import SQLMysql
from web_backend.logger_text.logger_text import log
from web_backend.error_text.error_text import APIException, ServerError, HTTPException

app = Flask(__name__)


lists = ['/login']
# 日志处理
logger = log()


@app.before_request
def interceptor():
    data = {
        "object": None,
        "msg": "用户未登录！",
        "code": 9200,
        "result": False,
        "status": "success"
    }
    url = request.path
    for i in range(len(lists)):
        if lists[i] == url:
            logger.info("处于拦截白名单，放行")
            return
    uuid = request.cookies.get('uuid', None)
    username = request.cookies.get('username', None)
    logger.debug("uuid: " + str(uuid) + " username: " + str(username))
    logger.debug("cookies: " + str(request.cookies))
    if uuid is None or username is None:
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 判断用户数据是否正确
    s = SQLMysql()
    # 此处查询限制不要轻易改动，用户以及其他模块，依赖此处用户的实时状态，改动后要注意用户模块和其他模块查询结果的影响
    sql = "select u_id, u_password, u_salt from user_info where u_name=%s and is_active=1 and is_delete=0"
    logger.debug("select u_id, u_password, u_salt from user_info where u_name={} and is_active=1 and is_delete=0".format(username))
    is_null = s.query_one(sql, [username, ])
    logger.debug("查询信息：" + str(is_null))
    if is_null is None:
        data["code"] = 9201
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    user_uuid = hashlib.md5((str(is_null[0]) + is_null[2]).encode('utf-8')).hexdigest()
    logger.debug("拦截器信息比对：" + "user_uuid：" + user_uuid + " uuid：" + uuid + " 比对结果：" + user_uuid != uuid)
    if user_uuid != uuid:
        data["code"] = 9202
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')


# 全局错误AOP处理
@app.errorhandler(Exception)
def framework_error(e):
    # 判断异常是不是HTTPException
    if isinstance(e, HTTPException):
        logger.error(e)
        code = e.code
        # 获取具体的响应错误信息
        msg = str(e.code) + " " + e.name
        error_code = 9999
        return APIException(code=code, msg=msg, error_code=error_code)
    # 异常肯定是Exception
    else:
        # 如果是调试模式,则返回e的具体异常信息
        # 将异常信息写入日志
        if app.config["DEBUG"]:
            logger.error(e)
            return e
        else:
            logger.error(e)
            return ServerError()


def create_app():
    # 导入配置文件
    app.config.from_object(settings.Development)
    # 注册蓝图
    app.register_blueprint(user)
    app.register_blueprint(env_variable)
    app.register_blueprint(test_cases)
    return app
