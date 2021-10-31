from flask import Blueprint, request, Response
import json, re
from mysql.pymysql import SQLMysql

test_cases = Blueprint('test_cases', __name__)


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
    is_rely = 1 if request.json.get("is_rely_on", 0) == 1 else 0
    request_data = request.json.get("request_data", {})
    if header is None or url is None:
        if not env_url or not env_header:
            data["msg"] = "参数非法"
            data["code"] = 20001
            return Response(json.dumps(data), content_type='application/json')
        elif env_url and env_header:
            s = SQLMysql()
            sql = "select v_id from jk_variable from where v_name=%s"
            is_null01 = s.query_one(sql, [env_url, ])
            is_null02 = s.query_one(sql, [env_header, ])
            if is_null01 is None or is_null02 is None:
                data["msg"] = "参数非法"
                data["code"] = 20001
                return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "参数非法"
            data["code"] = 20001
            return Response(json.dumps(data), content_type='application/json')
    if method is None or request_data is None or not group_name or not case_name:
        data["msg"] = "参数非法"
        data["code"] = 20001
        return Response(json.dumps(data), content_type='application/json')
    if method.upper() != "GET" and method.upper() != "POST":
        data["msg"] = "参数非法"
        data["code"] = 20002
        return Response(json.dumps(data), content_type='application/json')
    # 校验header格式
    if not isinstance(header, dict):
        data["msg"] = "参数非法"
        data["code"] = 20003
        return Response(json.dumps(data), content_type='application/json')
    # 校验url格式
    pattern = re.compile(r"^(http)[s]?://[^\s]*")
    url = pattern.search(url)
    if url is None:
        data["msg"] = "参数非法"
        data["code"] = 20004
        return Response(json.dumps(data), content_type='application/json')
    # 处理断言数据传参是否正确
    if is_assert == 1:
        if not assert_mode or not assert_data or not assert_type:
            data["msg"] = "参数非法"
            data["code"] = 20006
            return Response(json.dumps(data), content_type='application/json')
        pattern = re.compile(r"^([><=]|(>=)|(<=))$")
        is_null = pattern.search(assert_mode)
        if is_null is None:
            data["msg"] = "参数非法"
            data["code"] = 20007
            return Response(json.dumps(data), content_type='application/json')
    # 校验request_data格式
    if not isinstance(request_data, dict):
        data["msg"] = "参数非法"
        data["code"] = 20008
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    sql_na = "insert into jk_testcase (case_name, method, path, url, is_assert, is_rely_on, header, request_data, group_id, create_time) values (%s, %s, %s, %s, %s, %s, %s, %s, now())"
    sql_ya = "insert into jk_testcase (case_name, method, path, url, is_assert, a_data, a_mode, a_type, is_rely_on, header, request_data, group_id, create_time) values (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, now())"
    sql_s = "select group_id from jk_cgroups where group_name=%s"
    group_id = s.query_one(sql_s, [group_name, ])
    if group_id is None:
        data["msg"] = "用例分组不存在"
        data["code"] = 20009
        return Response(json.dumps(data), content_type='application/json')
    group_id = group_id[0]
    if not header or not url[0]:
        header = {
            "mode": "env",
            "data": env_header
        }
        url = {
            "mode": "env",
            "data": env_url
        }
    else:
        header = {
            "mode": "un_env",
            "data": header
        }
        url = {
            "mode": "un_env",
            "data": url[0]
        }
    if is_assert == 1:
        ok = s.create_one(sql_ya,
                          [case_name, method.upper(), path, str(url), is_assert, assert_data, assert_mode, assert_type, is_rely,
                           str(header),
                           str(request_data), group_id, ])
        if ok:
            data["msg"] = "添加成功"
            data["code"] = 20010
            data["result"] = True
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 20011
            return Response(json.dumps(data), content_type='application/json')
    elif is_assert == 0:
        ok = s.create_one(sql_na, [case_name, method.upper(), path, str(url), is_assert, is_rely, str(header), str(request_data), group_id, ])
        if ok:
            data["msg"] = "添加成功"
            data["code"] = 20010
            data["result"] = True
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 20011
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
    is_rely = 1 if request.json.get("is_rely_on", 0) == 1 else 0
    request_data = request.json.get("request_data", {})
    if header is None or url is None:
        if not env_url or not env_header:
            data["msg"] = "参数非法"
            data["code"] = 20101
            return Response(json.dumps(data), content_type='application/json')
        elif env_url and env_header:
            s = SQLMysql()
            sql = "select v_id from jk_variable from where v_name=%s"
            is_null01 = s.query_one(sql, [env_url, ])
            is_null02 = s.query_one(sql, [env_header, ])
            if is_null01 is None or is_null02 is None:
                data["msg"] = "参数非法"
                data["code"] = 20101
                return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "参数非法"
            data["code"] = 20101
            return Response(json.dumps(data), content_type='application/json')
    if method is None or request_data is None or not group_name or not case_name or not case_id:
        data["msg"] = "参数非法"
        data["code"] = 20101
        return Response(json.dumps(data), content_type='application/json')
    if method.upper() != "GET" and method.upper() != "POST":
        data["msg"] = "参数非法"
        data["code"] = 20102
        return Response(json.dumps(data), content_type='application/json')
    # 校验header格式
    if not isinstance(header, dict):
        data["msg"] = "参数非法"
        data["code"] = 20103
        return Response(json.dumps(data), content_type='application/json')
    # 校验url格式
    pattern = re.compile(r"^(http)[s]?://[^\s]*")
    url = pattern.search(url)
    if url is None:
        data["msg"] = "参数非法"
        data["code"] = 20104
        return Response(json.dumps(data), content_type='application/json')
    # 处理断言数据传参是否正确
    if is_assert == 1:
        if not assert_mode or not assert_data or not assert_type:
            data["msg"] = "参数非法"
            data["code"] = 20106
            return Response(json.dumps(data), content_type='application/json')
        pattern = re.compile(r"^([><=]|(>=)|(<=))$")
        is_null = pattern.search(assert_mode)
        if is_null is None:
            data["msg"] = "参数非法"
            data["code"] = 20107
            return Response(json.dumps(data), content_type='application/json')
    # 校验request_data格式
    if not isinstance(request_data, dict):
        data["msg"] = "参数非法"
        data["code"] = 20108
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    sql_q = "select case_id from jk_testcase where case_id=%s"
    sql_na = "update jk_testcase set case_name=%s, method=%s, path=%s, url=%s, is_assert=%s, is_rely_on=%s, header=%s, request_data=%s, group_id=%s, modfiy_time=now() where case_id=%s"
    sql_ya = "update jk_testcase set case_name=%s, method=%s, path=%s, url=%s, is_assert=%s, a_data=%s, a_mode=%s, a_type=%s, is_rely_on=%s, header=%s, request_data=%s, group_id=%s, modfiy_time=now() where case_id=%s"
    sql_s = "select group_id from jk_cgroups where group_name=%s"
    case_id = s.query_one(sql_q, [case_id, ])
    if case_id is None:
        data["msg"] = "参数非法"
        data["code"] = 20109
        return Response(json.dumps(data), content_type='application/json')
    group_id = s.query_one(sql_s, [group_name, ])
    if group_id is None:
        data["msg"] = "用例分组不存在"
        data["code"] = 20110
        return Response(json.dumps(data), content_type='application/json')
    group_id = group_id[0]
    if not header or not url[0]:
        header = {
            "mode": "env",
            "data": env_header
        }
        url = {
            "mode": "env",
            "data": env_url
        }
    else:
        header = {
            "mode": "un_env",
            "data": header
        }
        url = {
            "mode": "un_env",
            "data": url[0]
        }
    if is_assert == 1:
        ok = s.update_one(sql_ya, [case_name, method.upper(), path, str(url), is_assert, assert_data, assert_mode, assert_type, is_rely, str(header), str(request_data), group_id, case_id[0], ])
        if ok:
            data["msg"] = "修改成功"
            data["code"] = 20010
            data["result"] = True
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 20011
            return Response(json.dumps(data), content_type='application/json')
    elif is_assert == 0:
        ok = s.update_one(sql_na, [case_name, method.upper(), path, str(url), is_assert, is_rely, str(header), str(request_data), group_id, case_id[0], ])
        if ok:
            data["msg"] = "修改成功"
            data["code"] = 20010
            data["result"] = True
            return Response(json.dumps(data), content_type='application/json')
        else:
            data["msg"] = "未知异常"
            data["code"] = 20011
            return Response(json.dumps(data), content_type='application/json')
    return "未知异常"

