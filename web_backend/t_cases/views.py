import json
import re
from flask import Blueprint, request, Response
from mysql.pymysql import SQLMysql
from web_backend.logger_text.logger_text import log

test_cases = Blueprint('test_cases', __name__)

logger = log()


@test_cases.route('/t_addcase', methods=["POST"])
def t_addcases():
    '''
    断言只支持 等于 =  不等于 !=  大于 >   小于 <  状态码status_code  断言
    断言传入写法example：
        data = {
            “name”: "111",
            "num": 1,
            "lists": [
                {
                    "msg": "123"
                },
                {
                    "msg": "456"
                }
            ]
        }
        $context.name  代表 name 值 111
        $context.lists.0.msg  代表lists属性中的第一个对象中的msg的值
        传参的数值一定以 . 来区分  确定数组中的第几个值，直接写对应数字即可
        $context 固定参数,表示当前用例返回结果对象 固定单词 ,传参第一个单词必须是此单词
    :return:
    '''
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
    # 可以使用环境变量的参数
    # 判断使用环境变量还是不使用传参  header url 为null，使用用户所传环境变量 反之使用header url
    header = request.json.get("header", None)
    url = request.json.get("url", None)
    env_header = request.json.get("env_header", None)
    env_url = request.json.get("env_url", None)
    # 不支持环境变量的参数
    path = request.json.get("path", None)
    method = request.json.get("method", None)
    case_name = request.json.get("case_name", None)
    group_name = request.json.get("group_name", None)
    # 获取断言参数
    is_assert = 1 if request.json.get("is_assert", 0) == 1 else 0  # 默认不需要断言
    assert_mode = request.json.get("assert_mode", None)
    assert_data = request.json.get("assert_data", None)
    assert_type = request.json.get("assert_type", None)
    a_result_data = request.json.get("a_result_data", None)
    is_rely = 1 if request.json.get("is_rely_on", 0) == 1 else 0
    request_data = request.json.get("request_data", {})
    # 判断当前是否需要使用虚拟环境变量
    if not header or not url:
        if not env_url and not env_header:
            data["msg"] = "参数非法"
            data["code"] = 20001
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        elif url and env_header:
            # 查询当前虚拟环境变量是否存在
            s = SQLMysql()
            sql = "select v_id from jk_variable from where v_name=%s"
            logger.debug("select v_id from jk_variable from where v_name={}".format(env_header))
            is_null = s.query_one(sql, [env_header, ])
            logger.debug("查询信息：" + str(is_null))
            if is_null is None:
                data["msg"] = "参数非法"
                data["code"] = 20002
                logger.info("返回信息" + str(data))
                return Response(json.dumps(data), content_type='application/json')
        elif header and env_url:
            # 查询当前虚拟环境变量是否存在
            s = SQLMysql()
            sql = "select v_id from jk_variable from where v_name=%s"
            logger.debug("select v_id from jk_variable from where v_name={}".format(env_url))
            is_null = s.query_one(sql, [env_url, ])
            logger.debug("查询信息：" + str(is_null))
            if is_null is None:
                data["msg"] = "参数非法"
                data["code"] = 20003
                logger.info("返回信息" + str(data))
                return Response(json.dumps(data), content_type='application/json')
        elif not header and not url and env_url and env_header:
            # 查询当前虚拟环境变量是否存在
            s = SQLMysql()
            sql = "select v_id from jk_variable from where v_name=%s"
            logger.debug("select v_id from jk_variable from where v_name={}".format(env_header))
            logger.debug("select v_id from jk_variable from where v_name={}".format(env_url))
            is_null01 = s.query_one(sql, [env_header, ])
            is_null02 = s.query_one(sql, [env_url, ])
            logger.debug("查询信息：" + str(is_null01))
            logger.debug("查询信息：" + str(is_null02))
            if is_null01 is None or is_null02 is None:
                data["msg"] = "参数非法"
                data["code"] = 20004
                logger.info("返回信息" + str(data))
                return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "参数非法"
            data["code"] = 20005
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    if not method or not request_data or not group_name or not case_name:
        data["msg"] = "参数非法"
        data["code"] = 20006
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    if method.upper() != "GET" and method.upper() != "POST":
        data["msg"] = "参数非法"
        data["code"] = 20007
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 校验header格式
    if not isinstance(header, dict):
        data["msg"] = "参数非法"
        data["code"] = 20008
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 校验url格式
    pattern = re.compile(r"^(http)[s]?://[^\s]*")
    url = pattern.search(url)
    if url is None:
        data["msg"] = "参数非法"
        data["code"] = 20009
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 处理断言数据传参是否正确
    if is_assert == 1:
        if not assert_mode or not assert_data or not assert_type:
            data["msg"] = "参数非法"
            data["code"] = 20010
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        pattern = re.compile(r"^([><=]|(>=)|(<=))$")
        is_null = pattern.search(assert_mode)
        if is_null is None:
            data["msg"] = "参数非法"
            data["code"] = 20011
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    # 校验request_data格式
    if not isinstance(request_data, dict):
        data["msg"] = "参数非法"
        data["code"] = 20012
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    sql_na = "insert into jk_testcase (case_name, method, path, url, is_assert, is_rely_on, header, request_data, group_id, create_time) values (%s, %s, %s, %s, %s, %s, %s, %s, now())"
    sql_ya = "insert into jk_testcase (case_name, method, path, url, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, header, request_data, group_id, create_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
    sql_s = "select group_id from jk_cgroups where group_name=%s"
    logger.debug("select group_id from jk_cgroups where group_name={}".format(group_name))
    group_id = s.query_one(sql_s, [group_name, ])
    logger.debug("查询信息：" + str(group_id))
    if group_id is None:
        data["msg"] = "用例分组不存在"
        data["code"] = 20013
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    group_id = group_id[0]
    if not header:
        header = {
            "mode": "env",
            "data": env_header
        }
    else:
        header = {
            "mode": "un_env",
            "data": header
        }
    if not url[0]:
        url = {
            "mode": "env",
            "data": env_url
        }
    else:
        url = {
            "mode": "un_env",
            "data": url[0]
        }
    if is_assert == 1:
        logger.debug("insert into jk_testcase (case_name, method, path, url, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, header, request_data, group_id, create_time) values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, now())".format(case_name, method.upper(), path, str(url), is_assert, assert_data, assert_mode, assert_type, a_result_data,
                           is_rely,
                           str(header),
                           str(request_data), group_id))
        ok = s.create_one(sql_ya,
                          [case_name, method.upper(), path, str(url), is_assert, assert_data, assert_mode, assert_type, a_result_data,
                           is_rely,
                           str(header),
                           str(request_data), group_id, ])
        if ok:
            data["msg"] = "添加成功"
            data["code"] = 20014
            data["result"] = True
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 20015
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    elif is_assert == 0:
        logger.debug("insert into jk_testcase (case_name, method, path, url, is_assert, is_rely_on, header, request_data, group_id, create_time) values ({}, {}, {}, {}, {}, {}, {}, {}, now())".format(case_name, method.upper(), path, str(url), is_assert, is_rely, str(header),
                                   str(request_data), group_id))
        ok = s.create_one(sql_na, [case_name, method.upper(), path, str(url), is_assert, is_rely, str(header),
                                   str(request_data), group_id, ])
        if ok:
            data["msg"] = "添加成功"
            data["code"] = 20016
            data["result"] = True
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 20017
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    return "未知异常"


@test_cases.route('/t_update', methods=["POST"])
def t_updatecases():
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
    # 可以使用环境变量的参数
    # 判断使用环境变量还是不使用传参  header url 为null，使用用户所传环境变量 反之使用header url
    header = request.json.get("header", None)
    url = request.json.get("url", None)
    env_header = request.json.get("env_header", None)
    env_url = request.json.get("env_url", None)
    # 不支持环境变量的参数
    path = request.json.get("path", None)
    method = request.json.get("method", None)
    case_name = request.json.get("case_name", None)
    group_name = request.json.get("group_name", None)
    case_id = request.json.get("case_id", None)
    # 获取断言参数
    is_assert = 1 if request.json.get("is_assert", 0) == 1 else 0  # 默认不需要断言
    assert_mode = request.json.get("assert_mode", None)
    assert_data = request.json.get("assert_data", None)
    assert_type = request.json.get("assert_type", None)
    a_result_data = request.json.get("a_result_data", None)
    is_rely = 1 if request.json.get("is_rely_on", 0) == 1 else 0
    request_data = request.json.get("request_data", {})
    # 判断当前是否需要使用虚拟环境变量
    if not header or not url:
        if not env_url and not env_header:
            data["msg"] = "参数非法"
            data["code"] = 20101
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        elif url and env_header:
            # 查询当前虚拟环境变量是否存在
            s = SQLMysql()
            sql = "select v_id from jk_variable from where v_name=%s"
            logger.debug("select v_id from jk_variable from where v_name={}".format(env_header))
            is_null = s.query_one(sql, [env_header, ])
            logger.debug("查询信息：" + str(is_null))
            if is_null is None:
                data["msg"] = "参数非法"
                data["code"] = 20102
                logger.info("返回信息" + str(data))
                return Response(json.dumps(data), content_type='application/json')
        elif header and env_url:
            # 查询当前虚拟环境变量是否存在
            s = SQLMysql()
            sql = "select v_id from jk_variable from where v_name=%s"
            logger.debug("select v_id from jk_variable from where v_name={}".format(env_url))
            is_null = s.query_one(sql, [env_url, ])
            logger.debug("查询信息：" + str(is_null))
            if is_null is None:
                data["msg"] = "参数非法"
                data["code"] = 20103
                logger.info("返回信息" + str(data))
                return Response(json.dumps(data), content_type='application/json')
        elif not header and not url and env_url and env_header:
            # 查询当前虚拟环境变量是否存在
            s = SQLMysql()
            sql = "select v_id from jk_variable from where v_name=%s"
            logger.debug("select v_id from jk_variable from where v_name={}".format(env_header))
            logger.debug("select v_id from jk_variable from where v_name={}".format(env_url))
            is_null01 = s.query_one(sql, [env_header, ])
            is_null02 = s.query_one(sql, [env_url, ])
            logger.debug("查询信息：" + str(is_null01))
            logger.debug("查询信息：" + str(is_null02))
            if is_null01 is None or is_null02 is None:
                data["msg"] = "参数非法"
                data["code"] = 20104
                logger.info("返回信息" + str(data))
                return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "参数非法"
            data["code"] = 20105
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    if method is None or request_data is None or not group_name or not case_name or not case_id:
        data["msg"] = "参数非法"
        data["code"] = 20106
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    if method.upper() != "GET" and method.upper() != "POST":
        data["msg"] = "参数非法"
        data["code"] = 20107
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 校验header格式
    if not isinstance(header, dict):
        data["msg"] = "参数非法"
        data["code"] = 20108
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 校验url格式
    pattern = re.compile(r"^(http)[s]?://[^\s]*")
    url = pattern.search(url)
    if url is None:
        data["msg"] = "参数非法"
        data["code"] = 20109
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 处理断言数据传参是否正确
    if is_assert == 1:
        if not assert_mode or not assert_data or not assert_type:
            data["msg"] = "参数非法"
            data["code"] = 20110
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        pattern = re.compile(r"^([><=]|(>=)|(<=))$")
        is_null = pattern.search(assert_mode)
        if is_null is None:
            data["msg"] = "参数非法"
            data["code"] = 20111
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    # 校验request_data格式
    if not isinstance(request_data, dict):
        data["msg"] = "参数非法"
        data["code"] = 20112
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    sql_q = "select status from jk_testcase where case_id=%s"
    sql_na = "update jk_testcase set case_name=%s, method=%s, path=%s, url=%s, is_assert=%s, is_rely_on=%s, header=%s, request_data=%s, group_id=%s, modfiy_time=now() where case_id=%s"
    sql_ya = "update jk_testcase set case_name=%s, method=%s, path=%s, url=%s, is_assert=%s, a_data=%s, a_mode=%s, a_type=%s, a_result_data=%s, is_rely_on=%s, header=%s, request_data=%s, group_id=%s, modfiy_time=now() where case_id=%s"
    sql_s = "select group_id from jk_cgroups where group_name=%s"
    logger.debug("select status from jk_testcase where case_id={}".format(case_id))
    pd = s.query_one(sql_q, [case_id, ])
    logger.debug("查询信息：" + str(pd))
    if pd is None:
        data["msg"] = "参数非法"
        data["code"] = 20113
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 判断当前用例是否处于运行中，运行中的用例不允许更新
    if pd[0] == 1:
        data["msg"] = "用例正在执行中，不允许更新"
        data["code"] = 20114
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    logger.debug("select group_id from jk_cgroups where group_name={}".format(group_name))
    group_id = s.query_one(sql_s, [group_name, ])
    logger.debug("查询信息：" + str(group_id))
    if group_id is None:
        data["msg"] = "用例分组不存在"
        data["code"] = 20115
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    group_id = group_id[0]
    if not header:
        header = {
            "mode": "env",
            "data": env_header
        }
    else:
        header = {
            "mode": "un_env",
            "data": header
        }
    if not url[0]:
        url = {
            "mode": "env",
            "data": env_url
        }
    else:
        url = {
            "mode": "un_env",
            "data": url[0]
        }
    if is_assert == 1:
        logger.debug("update jk_testcase set case_name={}, method={}, path={}, url={}, is_assert={}, a_data={}, a_mode={}, a_type={}, a_result_data={}, is_rely_on={}, header={}, request_data={}, group_id={}, modfiy_time=now() where case_id={}".format(case_name, method.upper(), path, str(url), is_assert, assert_data, assert_mode, assert_type, a_result_data,
                           is_rely, str(header), str(request_data), group_id, case_id[0]))
        ok = s.update_one(sql_ya,
                          [case_name, method.upper(), path, str(url), is_assert, assert_data, assert_mode, assert_type, a_result_data,
                           is_rely, str(header), str(request_data), group_id, case_id[0], ])
        if ok:
            data["msg"] = "修改成功"
            data["code"] = 20116
            data["result"] = True
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 20117
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    elif is_assert == 0:
        logger.debug("update jk_testcase set case_name={}, method={}, path={}, url={}, is_assert={}, is_rely_on={}, header={}, request_data={}, group_id={}, modfiy_time=now() where case_id={}".format(case_name, method.upper(), path, str(url), is_assert, is_rely, str(header),
                                   str(request_data), group_id, case_id[0]))
        ok = s.update_one(sql_na, [case_name, method.upper(), path, str(url), is_assert, is_rely, str(header),
                                   str(request_data), group_id, case_id[0], ])
        if ok:
            data["msg"] = "修改成功"
            data["code"] = 20118
            data["result"] = True
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 20119
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    return "未知异常"


@test_cases.route("/t_delete", methods=["POST"])
def t_delete():
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
    case_id = request.json.get("case_id", None)
    if not case_id:
        data["msg"] = "参数非法"
        data["code"] = 20200
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    sql_s = "select status from jk_testcase where case_id=%s"
    logger.debug("select status from jk_testcase where case_id={}".format(case_id))
    num = s.query_one(sql_s, [case_id, ])
    logger.debug("查询信息：" + str(num))
    if num is None:
        data["msg"] = "数据不存在"
        data["code"] = 20201
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 检查当前用例是否处于运行队列中，用例正在处于运行中不允许删除
    if num[0] == 1:
        data["msg"] = "用例正在执行中，不允许删除"
        data["code"] = 20202
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    sql_d = "delete from jk_testcase where case_id=%s"
    logger.debug("delete from jk_testcase where case_id={}".format(case_id))
    ok = s.update_one(sql_d, [case_id, ])
    if ok:
        data["msg"] = "删除成功"
        data["code"] = 20203
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "未知异常"
        data["code"] = 20204
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')


@test_cases.route("/t_lists", methods=["GET"])
def t_lists():
    '''
    支持使用用例名字、用例id、用例分组查询列表
    :return:
    '''
    data = {
        "object": None,
        "msg": "缺少参数",
        "code": 10000,
        "result": False
    }
    # 处理没有传参的问题
    if not request.args:
        logger.debug("request.args:" + str(request.args))
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    case_name = None if request.args.get("case_name", None) == "" else request.args.get("case_name", None)
    group_name = None if request.args.get("group_name", None) == "" else request.args.get("group_name", None)
    case_id = request.args.get("case_id", None)
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 10, type=int)
    s = SQLMysql()
    if group_name:
        sql = "select group_id from jk_cgroups where group_name=%s"
        logger.debug("select group_id from jk_cgroups where group_name={}".format(group_name))
        group_id = s.query_one(sql, [group_name, ])
        logger.debug("查询信息：" + str(group_id))
        if group_id is None:
            data["msg"] = "用例分组不存在"
            data["code"] = 20300
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        else:
            group_name = group_id[0]
    sql = "select t.case_id, t.case_name, t.method, t.path, t.url, t.status, t.is_assert, t.is_rely_on, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.group_id=%s or t.case_id=%s or t.case_name like %s limit %s, %s"
    logger.debug("select t.case_id, t.case_name, t.method, t.path, t.url, t.status, t.is_assert, t.is_rely_on, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.group_id={} or t.case_id={} or t.case_name like {} limit {}, {}".format(group_name, case_id, ('%' + str(case_name) + '%'), (page - 1), limit))
    li = s.query_all(sql, [group_name, case_id, ('%' + str(case_name) + '%'), (page - 1), limit, ])
    logger.debug("查询信息：" + str(li))
    if not li:
        data["msg"] = "暂无数据"
        data["code"] = 20301
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    list_all =[]
    for i in range(len(li)):
        case_id, case_name, method, path, url, status, is_assert, is_rely_on, header, request_data, group_name = li[i]
        list_all.append({
            "case_id": case_id,
            "case_name": case_name,
            "method": method,
            "path": path,
            "url": url,
            "status": status,
            "is_assert": is_assert,
            "is_rely_on": is_rely_on,
            "header": header,
            "request_data": request_data,
            "group_name": group_name
        })
    data["object"] = list_all
    data["msg"] = "查询成功"
    data["code"] = 20302
    data["result"] = True
    logger.info("返回信息" + str(data))
    return Response(json.dumps(data), content_type='application/json')


@test_cases.route("/t_lists_one", methods=["POST"])
def t_lists_one():
    '''
        只支持用例cses_id来查询，本接口用来使用查看单个用例的所有信息，用来更新编辑时使用
        :return:
        '''
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
    case_id = request.json.get("case_id", None)
    if not case_id:
        data["msg"] = "参数非法"
        data["code"] = 20400
        return Response(json.dumps(data), content_type='application/json')
    sql = "select t.case_id, t.case_name, t.method, t.path, t.url, t.is_assert, t.a_data, t.a_mode, t.a_type, t.a_result_data, t.is_rely_on, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.case_id=%s"
    s = SQLMysql()
    logger.debug("select t.case_id, t.case_name, t.method, t.path, t.url, t.is_assert, t.a_data, t.a_mode, t.a_type, t.a_result_data, t.is_rely_on, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.case_id={}".format(case_id))
    li = s.query_one(sql, [case_id, ])
    logger.debug("查询信息：" + str(li))
    if li is None:
        data["msg"] = "用例信息不存在"
        data["code"] = 20401
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 解构数据
    case_id, case_name, method, path, url, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, header, request_data, group_name = li
    list_one = {
        "case_id": case_id,
        "case_name": case_name,
        "method": method,
        "path": path,
        "url": url,
        "is_assert": is_assert,
        "a_data": a_data,
        "a_mode": a_mode,
        "a_type": a_type,
        "a_result_data": a_result_data,
        "is_rely_on": is_rely_on,
        "header": header,
        "request_data": request_data,
        "group_name": group_name
    }
    data["object"] = list_one
    data["msg"] = "查询成功"
    data["code"] = 20402
    logger.info("返回信息" + str(data))
    return Response(json.dumps(data), content_type='application/json')


@test_cases.route("/t_result", methods=["POST"])
def t_result():
    '''
    用来查看单个用例执行结果
    :return:
    '''
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
    case_id = request.json.get("case_id", None)
    if not case_id:
        data["msg"] = "参数非法"
        data["code"] = 20500
        return Response(json.dumps(data), content_type='application/json')
    sql = "select t.case_id, t.case_name, t.status, t.sub_status, t.a_status, t.request_data, t.result_code, t.result_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.case_id=%s"
    s = SQLMysql()
    logger.debug("select t.case_id, t.case_name, t.status, t.sub_status, t.a_status t.request_data, t.result_code, t.result_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.case_id={}".format(case_id))
    li = s.query_one(sql, [case_id, ])
    logger.debug("查询信息：" + str(li))
    if li is None:
        data["msg"] = "用例数据不存在"
        data["code"] = 20501
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 解构
    case_id, case_name, status, sub_status, a_status, request_data, result_code, result_data, group_name = li
    list_one = {
        "case_id": case_id,
        "case_name": case_name,
        "status": status,
        "sub_status": sub_status,
        "a_status": a_status,
        "request_data": request_data,
        "result_code": result_code,
        "result_data": result_data,
        "group_name": group_name
    }
    data["object"] = list_one
    data["msg"] = "查询成功"
    data["code"] = 20502
    logger.info("返回信息" + str(data))
    return Response(json.dumps(data), content_type='application/json')
