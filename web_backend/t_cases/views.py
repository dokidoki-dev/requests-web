import ast
import json
import re
from flask import Blueprint, request, Response
from mysql.pymysql import SQLMysql
from web_backend.logger_text.logger_text import log

test_cases = Blueprint('test_cases', __name__, url_prefix="/api/v1/cases")

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
        rely_data 传入格式同上断言格式  $context开头
    依赖只支持读取依赖接口的返回值：result_data 暂不支持其他值读取，写入方式类似于断言写法 $context.lists.0.msg
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
    params = request.json.get("params", None)
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
    rely_id = request.json.get("rely_id", None) if is_rely == 1 else None
    rely_data = request.json.get("rely_data", None)
    rely_mode = request.json.get("rely_mode", None)
    rely_key = request.json.get("rely_key", None)
    sort = request.json.get("sort", None)
    # 处理params参数合规
    if params is None:
        logger.info("params: None")
    else:
        if not isinstance(params, dict):
            data["msg"] = "参数非法"
            data["code"] = 20001
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    sort = sort if isinstance(sort, int) else None  # int
    request_data = request.json.get("request_data", None)
    # 处理path
    if path:
        pattern = re.compile(r'^[/]')
        is_path = pattern.search(str(path))
        if not is_path:
            data["msg"] = "参数非法"
            data["code"] = 20001
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
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
    else:
        # 不使用环境变量
        s = SQLMysql()
        sql_nn = "select group_id from jk_cgroups from where group_name=%s"
        li_nn = s.query_one(sql_nn, [group_name, ])
        if not li_nn:
            data["msg"] = "参数非法"
            data["code"] = 20018
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
    # 校验断言格式以及依赖数据格式
    if assert_data:
        pattern = re.compile(r"^(\$context)")
        is_null_a = pattern.search(assert_data)
        if is_null_a is None:
            data["msg"] = "参数非法"
            data["code"] = 20011
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    if rely_data:
        pattern = re.compile(r"^(\$context)")
        is_null_r = pattern.search(rely_data)
        if is_null_r is None:
            data["msg"] = "参数非法"
            data["code"] = 20011
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    # 校验request_data格式
    if request_data and not isinstance(request_data, dict):
        data["msg"] = "参数非法"
        data["code"] = 20012
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    sql_na = "insert into jk_testcase (sort, case_name, method, path, url, params, is_assert, is_rely_on, rely_id, rely_data, rely_mode, rely_key, header, request_data, group_id, create_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
    sql_ya = "insert into jk_testcase (sort, case_name, method, path, url, params, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, rely_id, rely_data, rely_mode, rely_key, header, request_data, group_id, create_time) values (%s, %s, %s,%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
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
    # 校验依赖关系id是否存在
    if rely_id:
        sql_i = "select count(*) from jk_testcase where rely_id=%s and group_id=%s"
        logger.debug("select count(*) from jk_testcase where rely_id={} and group_id={}".format(rely_id, group_id))
        is_id = s.query_one(sql_i, [rely_id, group_id, ])
        if is_id is None:
            data["msg"] = "依赖用例不存在或者不在同一分组"
            data["code"] = 20020
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    # 查询当前添加的用例排序是否存在重复
    sql_sort = "select count(*) from jk_testcase where group_id=%s and sort=%s"
    is_sort_null = s.query_one(sql_sort, [group_id, sort])
    if is_sort_null:
        data["msg"] = "组内排序不允许重复"
        data["code"] = 20019
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
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
        logger.debug("insert into jk_testcase (sort, case_name, method, path, url, params, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, rely_id, rely_data, rely_mode, rely_key, header, request_data, group_id, create_time) values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, now())".format(sort, case_name, method.upper(), path, str(url), str(params), is_assert, assert_data, assert_mode, assert_type, a_result_data,
                           is_rely, rely_id, rely_data, rely_mode, rely_key,
                           str(header),
                           str(request_data), group_id))
        ok = s.create_one(sql_ya,
                          [sort, case_name, method.upper(), path, str(url), str(params), is_assert, assert_data, assert_mode, assert_type, a_result_data,
                           is_rely,
                           rely_id, rely_data, rely_mode, rely_key,
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
        logger.debug("insert into jk_testcase (sort, case_name, method, path, url, params, is_assert, is_rely_on, rely_id, rely_data, rely_mode, rely_key, header, request_data, group_id, create_time) values ({}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, {}, now())".format(sort, case_name, method.upper(), path, str(url), str(params), is_assert, is_rely, rely_id, rely_data, rely_mode, rely_key, str(header),
                                   str(request_data), group_id))
        ok = s.create_one(sql_na, [sort, case_name, method.upper(), path, str(url), str(params), is_assert, is_rely, rely_id, rely_data, rely_mode, rely_key, str(header),
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
    params = request.json.get("params", None)
    # 获取断言参数
    is_assert = 1 if request.json.get("is_assert", 0) == 1 else 0  # 默认不需要断言
    assert_mode = request.json.get("assert_mode", None)
    assert_data = request.json.get("assert_data", None)
    assert_type = request.json.get("assert_type", None)
    a_result_data = request.json.get("a_result_data", None)
    is_rely = 1 if request.json.get("is_rely_on", 0) == 1 else 0
    rely_id = request.json.get("rely_id", None) if is_rely == 1 else None
    rely_data = request.json.get("rely_data", None)
    rely_mode = request.json.get("rely_mode", None)
    rely_key = request.json.get("rely_key", None)
    sort = request.json.get("sort", None)
    sort = sort if isinstance(sort, int) else None  # int
    request_data = request.json.get("request_data", None)
    # 处理params参数合规
    if params is None:
        logger.info("params: None")
    else:
        if not isinstance(params, dict):
            data["msg"] = "参数非法"
            data["code"] = 20001
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    # 处理path
    if path:
        pattern = re.compile(r'^[/]')
        is_path = pattern.search(str(path))
        if not is_path:
            data["msg"] = "参数非法"
            data["code"] = 20001
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
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
    # 校验断言格式以及依赖数据格式
    if assert_data:
        pattern = re.compile(r"^(\$context)")
        is_null_a = pattern.search(assert_data)
        if is_null_a is None:
            data["msg"] = "参数非法"
            data["code"] = 20011
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    if rely_data:
        pattern = re.compile(r"^(\$context)")
        is_null_r = pattern.search(rely_data)
        if is_null_r is None:
            data["msg"] = "参数非法"
            data["code"] = 20011
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    # 校验request_data格式
    if request_data and not isinstance(request_data, dict):
        data["msg"] = "参数非法"
        data["code"] = 20112
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    sql_q = "select status from jk_testcase where case_id=%s"
    sql_na = "update jk_testcase set sort=%s, case_name=%s, method=%s, path=%s, url=%s, params=%s, is_assert=%s, is_rely_on=%s, rely_id=%s, rely_data=%s, rely_mode=%s, rely_key=%s, header=%s, request_data=%s, group_id=%s, modfiy_time=now() where case_id=%s"
    sql_ya = "update jk_testcase set sort=%s, case_name=%s, method=%s, path=%s, url=%s, params=%s, is_assert=%s, a_data=%s, a_mode=%s, a_type=%s, a_result_data=%s, is_rely_on=%s, rely_id=%s, rely_data=%s, rely_mode=%s, rely_key=%s, header=%s, request_data=%s, group_id=%s, modfiy_time=now() where case_id=%s"
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
    # 校验依赖关系id是否存在
    if rely_id:
        sql_i = "select count(*) from jk_testcase where rely_id=%s and group_id=%s"
        logger.debug("select count(*) from jk_testcase where rely_id={} and group_id={}".format(rely_id, group_id))
        is_id = s.query_one(sql_i, [rely_id, group_id, ])
        if is_id is None:
            data["msg"] = "依赖用例不存在或者不在同一分组"
            data["code"] = 20020
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
    # 查询当前添加的用例排序是否存在重复
    sql_sort = "select count(*) from jk_testcase where group_id=%s and sort=%s"
    logger.debug("select count(*) from jk_testcase where group_id={} and sort={}".format(group_id, sort))
    is_sort_null = s.query_one(sql_sort, [group_id, sort, ])
    if is_sort_null:
        data["msg"] = "组内排序不允许重复"
        data["code"] = 20019
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
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
        logger.debug("update jk_testcase set sort={}, case_name={}, method={}, path={}, url={}, params={}, is_assert={}, a_data={}, a_mode={}, a_type={}, a_result_data={}, is_rely_on={}, rely_id={}, rely_data={}, rely_mode={}, rely_key={}, header={}, request_data={}, group_id={}, modfiy_time=now() where case_id={}".format(sort, case_name, method.upper(), path, str(url), str(params), is_assert, assert_data, assert_mode, assert_type, a_result_data,
                           is_rely, rely_id, rely_data, rely_mode, rely_key, str(header), str(request_data), group_id, case_id[0]))
        ok = s.update_one(sql_ya,
                          [sort, case_name, method.upper(), path, str(url), str(params), is_assert, assert_data, assert_mode, assert_type, a_result_data,
                           is_rely, rely_id, rely_data, rely_mode, rely_key, str(header), str(request_data), group_id, case_id[0], ])
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
        logger.debug("update jk_testcase set sort={} case_name={}, method={}, path={}, url={}, params={}, is_assert={}, is_rely_on={}, rely_id={}, rely_data={}, rely_mode={}, rely_key={}, header={}, request_data={}, group_id={}, modfiy_time=now() where case_id={}".format(sort, case_name, method.upper(), path, str(url), str(params), is_assert, is_rely, rely_id, rely_data, rely_mode, rely_key, str(header),
                                   str(request_data), group_id, case_id[0]))
        ok = s.update_one(sql_na, [sort, case_name, method.upper(), path, str(url), str(params), is_assert, is_rely, rely_id, rely_data, rely_mode, rely_key, str(header),
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
        "object": [],
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
    sql = "select t.sort, t.case_id, t.case_name, t.method, t.path, t.url, t.params, t.status, t.is_assert, t.is_rely_on, t.rely_id, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.group_id=%s or t.case_id=%s or t.case_name like %s limit %s, %s"
    logger.debug("select t.sort, t.case_id, t.case_name, t.method, t.path, t.url, t.params, t.status, t.is_assert, t.is_rely_on, t.rely_id, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.group_id={} or t.case_id={} or t.case_name like {} limit {}, {}".format(group_name, case_id, ('%' + str(case_name) + '%'), (page - 1), limit))
    queryp = [group_name, case_id, ('%' + str(case_name) + '%'), (page - 1), limit, ]
    if case_id is None:
        if case_name is None:
            sql = "select t.sort, t.case_id, t.case_name, t.method, t.path, t.url, t.params, t.status, t.is_assert, t.is_rely_on, t.rely_id, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.group_id=%s  limit %s, %s"
            logger.debug("select t.sort, t.case_id, t.case_name, t.method, t.path, t.url, t.params, t.status, t.is_assert, t.is_rely_on, t.rely_id, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.group_id={}  limit {}, {}".format(group_name, (page - 1), limit))
            queryp = [group_name, (page - 1), limit, ]
        else:
            sql = "select t.sort, t.case_id, t.case_name, t.method, t.path, t.url, t.params, t.status, t.is_assert, t.is_rely_on, t.rely_id, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.group_id=%s or t.case_name like %s limit %s, %s"
            logger.debug("select t.sort, t.case_id, t.case_name, t.method, t.path, t.url, t.params, t.status, t.is_assert, t.is_rely_on, t.rely_id, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.group_id={} or t.case_name like {} limit {}, {}".format(group_name, ('%' + str(case_name) + '%'), (page - 1), limit))
            queryp = [group_name, ('%' + str(case_name) + '%'), (page - 1), limit, ]
    li = s.query_all(sql, queryp)
    logger.debug("查询信息：" + str(li))
    if not li:
        data["msg"] = "暂无数据"
        data["code"] = 20301
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    list_all =[]
    for i in range(len(li)):
        sort, case_id, case_name, method, path, url, params, status, is_assert, is_rely_on, rely_id, header, request_data, group_name = li[i]
        # 处理header url
        if header:
            header = ast.literal_eval(header)
        if url:
            url = ast.literal_eval(url)
        # 处理环境变量的问题
        if url and url["mode"] == "env":
            sql_un = "select v_data from jk_variable from where v_name=%s"
            url = s.query_one(sql_un, [url["data"], ])[0]
        elif url and url["mode"] == "un_env":
            url = url["data"]
        if header and header["mode"] == "env":
            sql_un = "select v_data from jk_variable from where v_name=%s"
            header = s.query_one(sql_un, [header["data"], ])[0]
        elif header and header["mode"] == "un_env":
            header = header["data"]
        list_all.append({
            "case_id": case_id,
            "sort": sort,
            "case_name": case_name,
            "method": method,
            "path": path,
            "url": url,
            "params": params,
            "status": status,
            "is_assert": is_assert,
            "is_rely_on": is_rely_on,
            "rely_id": rely_id,
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
    sql = "select t.sort, t.case_id, t.case_name, t.method, t.path, t.url, t.params, t.is_assert, t.a_data, t.a_mode, t.a_type, t.a_result_data, t.is_rely_on, t.rely_id, t.rely_data, t.rely_mode, t.rely_key, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.case_id=%s"
    s = SQLMysql()
    logger.debug("select t.sort, t.case_id, t.case_name, t.method, t.path, t.url, t.params, t.is_assert, t.a_data, t.a_mode, t.a_type, t.a_result_data, t.is_rely_on, t.rely_id, t.rely_data, t.rely_mode, t.rely_key, t.header, t.request_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.case_id={}".format(case_id))
    li = s.query_one(sql, [case_id, ])
    logger.debug("查询信息：" + str(li))
    if li is None:
        data["msg"] = "用例信息不存在"
        data["code"] = 20401
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 解构数据
    sort, case_id, case_name, method, path, url, params, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, rely_id, rely_data, rely_mode, rely_key, header, request_data, group_name = li
    list_one = {
        "case_id": case_id,
        "sort": sort,
        "case_name": case_name,
        "method": method,
        "path": path,
        "url": url,
        "params": params,
        "is_assert": is_assert,
        "a_data": a_data,
        "a_mode": a_mode,
        "a_type": a_type,
        "a_result_data": a_result_data,
        "is_rely_on": is_rely_on,
        "rely_id": rely_id,
        "rely_data": rely_data,
        "rely_mode": rely_mode,
        "rely_key": rely_key,
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
    sql = "select t.sort, t.case_id, t.case_name, t.status, t.sub_status, t.a_status, t.request_data, t.result_code, t.is_assert, t.a_data, t.a_mode, t.a_type, t.a_result_data, t.a_status, t.result_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.case_id=%s"
    s = SQLMysql()
    logger.debug("select t.sort, t.case_id, t.case_name, t.status, t.sub_status, t.a_status t.request_data, t.result_code, t.result_data, c.group_name from jk_testcase as t INNER JOIN jk_cgroups as c ON t.group_id = c.group_id  where t.case_id={}".format(case_id))
    li = s.query_one(sql, [case_id, ])
    logger.debug("查询信息：" + str(li))
    if li is None:
        data["msg"] = "用例数据不存在"
        data["code"] = 20501
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 解构
    sort, case_id, case_name, status, sub_status, a_status, request_data, result_code, result_data, group_name = li
    list_one = {
        "case_id": case_id,
        "sort": sort,
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


@test_cases.route('/add_group', methods=['POST'])
def env_add_group():
    '''
    添加测试用例分组
    :return:
    '''
    data = {
        "object": None,
        "msg": "缺少参数",
        "code": 10000,
        "result": False,
    }
    # 处理缺少参数问题
    if not request.json:
        logger.debug("request.json: " + str(request.json))
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    group_name = request.json.get('group_name', None)
    if not group_name:
        data["msg"] = "缺少参数"
        data["code"] = 7899
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    sql = "select group_id from jk_cgroups where group_name=%s"
    logger.debug("select group_id from jk_cgroups where group_name={}".format(group_name))
    # 判断当前是否已经存在分组
    is_null = s.query_one(sql, [group_name, ])
    logger.debug("查询结果：" + str(is_null))
    if is_null:
        data["msg"] = "当前分组已存在，请勿重复添加"
        data["code"] = 7898
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    sql_add = "insert into jk_cgroups (group_name, create_time) values (%s, now())"
    logger.debug("insert into jk_cgroups (group_name, create_time) values ({}, now())".format(group_name))
    ok = s.create_one(sql_add, [group_name, ])
    if ok:
        data["msg"] = "添加成功"
        data["code"] = 7897
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "未知异常"
        data["code"] = 7896
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')


@test_cases.route('/g_lists', methods=['GET'])
def env_g_lists():
    """
    查询测试用例分组接口
    :return:
    """
    data = {
        "object": [],
        "msg": "缺少参数",
        "code": 10000,
        "result": False
    }
    # 处理没有传参的问题
    if not request.args:
        logger.debug("request.args: " + str(request.args))
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    page = request.args.get("page", 1, type=int)
    limit = request.args.get("limit", 20, type=int)
    s = SQLMysql()
    sql = "select group_name from jk_cgroups limit %s, %s"
    logger.debug("select group_name from jk_cgroups limit {}, {}".format((page-1), limit))
    li = s.query_all(sql, [(page - 1), limit, ])
    logger.debug("查询结果：" + str(li))
    if not li:
        data["msg"] = "暂无数据"
        data["code"] = 7594
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    list_n = []
    for i in range(len(li)):
        group_name = li[i][0]
        list_n.append({
            "group_name": group_name
        })
    data["object"] = list_n
    data["msg"] = "查询成功"
    data["code"] = 7593
    data["result"] = True
    logger.info("返回信息" + str(data))
    return Response(json.dumps(data), content_type='application/json')


@test_cases.route('/update_g', methods=['POST'])
def env_update_g():
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
    group_id = request.json.get('group_id', None)
    group_name = request.json.get('group_name', None)
    if not group_id or not group_name:
        data["msg"] = "参数非法"
        data["code"] = 7699
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    # 判断修改的分组是否存在
    sql_y = "select group_id from jk_cgroups where group_name=%s"
    logger.debug("select group_id from jk_cgroups where group_name={}".format(group_name))
    is_null = s.query_one(sql_y, [group_name, ])
    logger.debug("查询结果：" + str(is_null))
    if not is_null:
        data["msg"] = "分组不存在"
        data["code"] = 7698
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    if is_null[0] != group_id:
        data["msg"] = "参数非法"
        data["code"] = 7698
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    sql = "update jk_cgroups set group_name=%s, modfiy_time=now() where group_id=%s"
    ok = s.update_one(sql, [group_name, group_id, ])
    if ok:
        data["msg"] = "修改成功"
        data["code"] = 7696
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "未知异常"
        data["code"] = 7795
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')


@test_cases.route('/delete_g', methods=['POST'])
def env_delete_g():
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
    group_id = request.json.get('group_id', None)
    if not group_id:
        data["msg"] = "参数非法"
        data["code"] = 7599
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    # 判断当前分组是否存在
    sql_s = "select group_id from jk_cgroups where group_id=%s"
    logger.debug("select group_id from jk_cgroups where group_id={}".format(group_id))
    is_null = s.query_one(sql_s, [group_id, ])
    logger.debug("查询结果：" + str(is_null))
    if not is_null:
        data["msg"] = "分组数据不存在，删除失败"
        data["code"] = 7598
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 判断该分组下，是否还有测试用例，如果有的话，不允许删除分组 保证数据完整性
    sql_y = "select case_id from jk_testcase where group_id=%s"
    logger.debug("select case_id from jk_testcase where group_id={}".format(is_null[0]))
    is_n = s.query_one(sql_y, [(is_null[0]), ])
    logger.debug("查询结果：" + str(is_n))
    if is_n:
        data["msg"] = "当前分组下存在关联测试用例，无法删除，请先删除该分组下的所有测试用例"
        data["code"] = 7597
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    # 如果不存在测试用例，则可以直接删除
    sql_del = "delete from jk_cgroups where group_id=%s"
    logger.debug("delete from jk_cgroups where group_id={}".format(is_null[0]))
    ok = s.update_one(sql_del, [(is_null[0]), ])
    if ok:
        data["msg"] = "删除成功"
        data["code"] = 7596
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    else:
        data["msg"] = "未知异常"
        data["code"] = 7595
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
