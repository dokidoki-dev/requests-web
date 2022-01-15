import json
from mysql.pymysql import SQLMysql
from web_backend.logger_text.logger_text import log
import requests
import ast

logger = log()


# 不推荐使用
# 断言处理函数
def auto_assert(item, num, a_mode, a_data_list, a_result_data) -> bool:
    """
    使用此函数，需要提前将a_data_list中的值处理好，比如将其中字符串类型的数字，转换为int类型，否则会出错
    """
    result = False
    if num == 1 and a_mode == ">":
        result = True if item[a_data_list] > a_result_data else False
    elif num == 1 and a_mode == "<":
        result = True if item[a_data_list] < a_result_data else False
    elif num == 1 and a_mode == "=":
        result = True if item[a_data_list] == a_result_data else False
    elif num == 1 and a_mode == ">=":
        result = True if item[a_data_list] >= a_result_data else False
    elif num == 1 and a_mode == "<=":
        result = True if item[a_data_list] <= a_result_data else False
    elif num == 2 and a_mode == ">":
        num1, num2 = a_data_list
        result = True if item[num1][num2] <= a_result_data else False
    elif num == 2 and a_mode == "<":
        num1, num2 = a_data_list
        result = True if item[num1][num2] < a_result_data else False
    elif num == 2 and a_mode == "=":
        num1, num2 = a_data_list
        result = True if item[num1][num2] == a_result_data else False
    elif num == 2 and a_mode == ">=":
        num1, num2 = a_data_list
        result = True if item[num1][num2] >= a_result_data else False
    elif num == 2 and a_mode == "<=":
        num1, num2 = a_data_list
        result = True if item[num1][num2] <= a_result_data else False
    elif num == 3 and a_mode == ">":
        num1, num2, num3 = a_data_list
        result = True if item[num1][num2][num3] <= a_result_data else False
    elif num == 3 and a_mode == "<":
        num1, num2, num3 = a_data_list
        result = True if item[num1][num2][num3] < a_result_data else False
    elif num == 3 and a_mode == "=":
        num1, num2, num3 = a_data_list
        result = True if item[num1][num2][num3] == a_result_data else False
    elif num == 3 and a_mode == ">=":
        num1, num2, num3 = a_data_list
        result = True if item[num1][num2][num3] >= a_result_data else False
    elif num == 3 and a_mode == "<=":
        num1, num2, num3 = a_data_list
        result = True if item[num1][num2][num3] <= a_result_data else False
    elif num == 4 and a_mode == ">":
        num1, num2, num3, num4 = a_data_list
        result = True if item[num1][num2][num3][num4] <= a_result_data else False
    elif num == 4 and a_mode == "<":
        num1, num2, num3, num4 = a_data_list
        result = True if item[num1][num2][num3][num4] < a_result_data else False
    elif num == 4 and a_mode == "=":
        num1, num2, num3, num4 = a_data_list
        result = True if item[num1][num2][num3][num4] == a_result_data else False
    elif num == 4 and a_mode == ">=":
        num1, num2, num3, num4 = a_data_list
        result = True if item[num1][num2][num3][num4] >= a_result_data else False
    elif num == 4 and a_mode == "<=":
        num1, num2, num3, num4 = a_data_list
        result = True if item[num1][num2][num3][num4] <= a_result_data else False
    elif num == 5 and a_mode == ">":
        num1, num2, num3, num4, num5 = a_data_list
        result = True if item[num1][num2][num3][num4][num5] <= a_result_data else False
    elif num == 5 and a_mode == "<":
        num1, num2, num3, num4, num5 = a_data_list
        result = True if item[num1][num2][num3][num4][num5] < a_result_data else False
    elif num == 5 and a_mode == "=":
        num1, num2, num3, num4, num5 = a_data_list
        result = True if item[num1][num2][num3][num4][num5] == a_result_data else False
    elif num == 5 and a_mode == ">=":
        num1, num2, num3, num4, num5 = a_data_list
        result = True if item[num1][num2][num3][num4][num5] >= a_result_data else False
    elif num == 5 and a_mode == "<=":
        num1, num2, num3, num4, num5 = a_data_list
        result = True if item[num1][num2][num3][num4][num5] <= a_result_data else False
    elif num == 6 and a_mode == ">":
        num1, num2, num3, num4, num5, num6 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6] <= a_result_data else False
    elif num == 6 and a_mode == "<":
        num1, num2, num3, num4, num5, num6 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6] < a_result_data else False
    elif num == 6 and a_mode == "=":
        num1, num2, num3, num4, num5, num6 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6] == a_result_data else False
    elif num == 6 and a_mode == ">=":
        num1, num2, num3, num4, num5, num6 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6] >= a_result_data else False
    elif num == 6 and a_mode == "<=":
        num1, num2, num3, num4, num5, num6 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6] <= a_result_data else False
    elif num == 7 and a_mode == ">":
        num1, num2, num3, num4, num5, num6, num7 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7] <= a_result_data else False
    elif num == 7 and a_mode == "<":
        num1, num2, num3, num4, num5, num6, num7 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7] < a_result_data else False
    elif num == 7 and a_mode == "=":
        num1, num2, num3, num4, num5, num6, num7 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7] == a_result_data else False
    elif num == 7 and a_mode == ">=":
        num1, num2, num3, num4, num5, num6, num7 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7] >= a_result_data else False
    elif num == 7 and a_mode == "<=":
        num1, num2, num3, num4, num5, num6, num7 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7] <= a_result_data else False
    elif num == 8 and a_mode == ">":
        num1, num2, num3, num4, num5, num6, num7, num8 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8] <= a_result_data else False
    elif num == 8 and a_mode == "<":
        num1, num2, num3, num4, num5, num6, num7, num8 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8] < a_result_data else False
    elif num == 8 and a_mode == "=":
        num1, num2, num3, num4, num5, num6, num7, num8 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8] == a_result_data else False
    elif num == 8 and a_mode == ">=":
        num1, num2, num3, num4, num5, num6, num7, num8 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8] >= a_result_data else False
    elif num == 8 and a_mode == "<=":
        num1, num2, num3, num4, num5, num6, num7, num8 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8] <= a_result_data else False
    elif num == 9 and a_mode == ">":
        num1, num2, num3, num4, num5, num6, num7, num8, num9 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8][num9] <= a_result_data else False
    elif num == 9 and a_mode == "<":
        num1, num2, num3, num4, num5, num6, num7, num8, num9 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8][num9] < a_result_data else False
    elif num == 9 and a_mode == "=":
        num1, num2, num3, num4, num5, num6, num7, num8, num9 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8][num9] == a_result_data else False
    elif num == 9 and a_mode == ">=":
        num1, num2, num3, num4, num5, num6, num7, num8, num9 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8][num9] >= a_result_data else False
    elif num == 9 and a_mode == "<=":
        num1, num2, num3, num4, num5, num6, num7, num8, num9 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8][num9] <= a_result_data else False
    elif num == 10 and a_mode == ">":
        num1, num2, num3, num4, num5, num6, num7, num8, num9, num10 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8][num9][num10] <= a_result_data else False
    elif num == 10 and a_mode == "<":
        num1, num2, num3, num4, num5, num6, num7, num8, num9, num10 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8][num9][num10] < a_result_data else False
    elif num == 10 and a_mode == "=":
        num1, num2, num3, num4, num5, num6, num7, num8, num9, num10 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8][num9][num10] == a_result_data else False
    elif num == 10 and a_mode == ">=":
        num1, num2, num3, num4, num5, num6, num7, num8, num9, num10 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8][num9][num10] >= a_result_data else False
    elif num == 10 and a_mode == "<=":
        num1, num2, num3, num4, num5, num6, num7, num8, num9, num10 = a_data_list
        result = True if item[num1][num2][num3][num4][num5][num6][num7][num8][num9][num10] <= a_result_data else False
    return result


# 第二种方案：使用eval()函数
# 将读取到的断言数据，分割成列表后，读取列表长度，然后通过循环凭借字符串格式的读取变量，然后放入eval()函数处理
# 例如    item = "data["msg"][0]["num"]"   ->  eval(item)   此时 eval(item) 经过处理就等同于 data["msg"][0]["num"]
# 也可以将eval(item)赋值   p = eval(item)  此时变量p就等同于 data["msg"][0]["num"]   然后即可进行断言操作

# 断言处理函数
def eval_assert(item: object, num: int, a_mode, a_data_list, a_result_data) -> bool:
    """
    item参数虽然未使用，但是不能删除，因为eval()函数需要使用
    a_data_list: 用户填写的读取断言的值 a_data
    item: 接口返回数据
    """
    result = False
    items = "item"
    # 处理数组里的数字类型格式
    for i in range(num):
        a_data_list[i] = int(a_data_list[i]) if a_data_list[i].isdigit() else a_data_list[i]
    # 拼接字符串 通过循环处理
    for i in range(num):
        string = '[{}]'.format(a_data_list[i]) if isinstance(a_data_list[i], int) else '["{}"]'.format(a_data_list[i])
        items = items + string
    # 处理完成，使用eval()函数处理即可转换
    if a_mode == ">":
        result = True if eval(items) > a_result_data else False
    elif a_mode == "<":
        result = True if eval(items) < a_result_data else False
    elif a_mode == "=":
        result = True if eval(items) == a_result_data else False
    elif a_mode == ">=":
        result = True if eval(items) >= a_result_data else False
    elif a_mode == "<=":
        result = True if eval(items) <= a_result_data else False
    return result


def request_get(url, header, params, request_data):
    '''
    封装get请求
    :return: request对象
    '''
    try:
        r = requests.get(url=url, headers=header, params=params, data=request_data, timeout=10)
    except Exception as e:
        logger.info("请求参数错误：" + str(e))
        return None
    else:
        logger.info("接口返回数据：" + str(r.json()))
        return r


def request_post(url, header, params, request_data):
    '''
    封装post请求
    :return: request对象
    '''
    try:
        r = requests.post(url=url, headers=header, params=params, data=request_data, timeout=10)
    except Exception as e:
        logger.info("请求参数错误：" + str(e))
        return None
    else:
        logger.info("接口返回数据：" + str(r.json()))
        return r


def request_auto(item: list):
    """
    依赖只支持去读依赖接口返回值
    """
    case_id, method, path, url, params, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, rely_id, rely_mode, rely_key, rely_data, header, request_data = item
    # 数据处理 转换为字典   params    request_data
    if params is None:
        logger.info("params: None")
    else:
        params = ast.literal_eval(params)
    if request_data is None:
        logger.info("request_data: None")
    else:
        request_data = ast.literal_eval(request_data)
    sql = "update jk_testcase set sub_status=1, modfiy_time=now() where case_id=%s"
    # 更新用例状态
    s = SQLMysql()
    logger.debug("update jk_testcase set sub_status=1 where case_id={}".format(case_id))
    ok = s.update_one(sql, [case_id, ])
    if not ok:
        logger.error("更新用例子状态失败")
        return False
    # 处理请求链接
    if not path:
        url = url
    else:
        url = url + path
    # 判断请求方式
    if method == "GET":
        # 判断当前是否是否需要断言
        if is_assert == 1:
            # 判断是否存在依赖
            if is_rely_on == 1:
                sql_rely = "select result_data from jk_testcase where case_id =%s"
                ok = s.query_one(sql_rely, [rely_id, ])
                if ok is None:
                    logger.info("依赖用例没有回复结果")
                    return False
                # 处理读取依赖用例返回数据的value
                rely_result_value = rely_data.split(".")[1:] if rely_data else None
                if rely_result_value is None:
                    return False
                ok = ok[0]
                item = "ok"
                for i in range(len(rely_result_value)):
                    string = '[{}]'.format(rely_result_value[i]) if isinstance(rely_result_value[i], int) else '["{}"]'.format(rely_result_value[i])
                    item = item + string
                try:
                    if rely_mode == 1:
                        params[rely_key] = eval(item)
                    if rely_mode == 2:
                        header[rely_key] = eval(item)
                    if rely_mode == 3:
                        request_data[rely_key] = eval(item)
                except Exception as e:
                    logger.error(e)
                    return False
                r = request_get(url, header, params, request_data)
                if r is None:
                    sql_f = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, modfiy_time=now() where case_id=%s"
                    s.update_one(sql_f, [0, 0, 201, case_id, ])
                    return False
                li = json.loads(r.text)
                status_code = 200 if r.status_code == 200 else 201
                if status_code != 200:
                    logger.error("接口返回状态码非200，无法断言")
                    sql_i = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s, modfiy_time=now() where case_id=%s"
                    logger.debug(
                        "update jk_testcase set status=0, sub_status=0, result_code={}, a_status=0, result_data={} where case_id={}".format(
                            status_code, li, case_id))
                    ok = s.update_one(sql_i, [0, 0, status_code, 0, str(li), case_id, ])
                    if not ok:
                        logger.error("数据库更新数据未知异常")
                    return False
                # 处理断言
                a_data_list = a_data.split(".")[1:]
                num = len(a_data_list)
                result = eval_assert(li, num, a_mode, a_data_list, a_result_data)
                a_status = 1 if result else 0
                sql_p = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s, modfiy_time=now() where case_id=%s"
                logger.debug(
                    "update jk_testcase set status=0, sub_status=0, result_code={}, a_status={}, result_data={} where case_id={}".format(
                        status_code, a_status, li, case_id))
                ok = s.update_one(sql_p, [0, 0, status_code, a_status, str(li), case_id, ])
                if ok:
                    return True
                else:
                    return False
            # 不依赖 但是需要断言
            sql = "select result_data from jk_testcase where rely_id=%s"
            da = s.query_one(sql, [rely_id, ])
            if not da:
                logger.error(request_auto.__name__ + "：依赖数据不存在返回数据")
                return False
            r = request_get(url, header, params, request_data)
            if r is None:
                sql_f = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, modfiy_time=now() where case_id=%s"
                s.update_one(sql_f, [0, 0, 201, case_id, ])
                return False
            li = json.loads(r.text)
            status_code = 200 if r.status_code == 200 else 201
            if status_code != 200:
                logger.error("接口返回状态码非200，无法断言")
                sql_i = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s, modfiy_time=now() where case_id=%s"
                logger.debug(
                    "update jk_testcase set status=0, sub_status=0, result_code={}, a_status=0, result_data={} where case_id={}".format(
                        status_code, li, case_id))
                ok = s.update_one(sql_i, [0, 0, status_code, 0, str(li), case_id, ])
                if not ok:
                    logger.error("数据库更新数据未知异常")
                return False
            # 处理断言
            a_data_list = a_data.split(".")[1:]
            num = len(a_data_list)
            result = eval_assert(li, num, a_mode, a_data_list, a_result_data)
            a_status = 1 if result else 0
            sql_p = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s, modfiy_time=now() where case_id=%s"
            logger.debug(
                "update jk_testcase set status=0, sub_status=0, result_code={}, a_status={}, result_data={} where case_id={}".format(
                    status_code, a_status, li, case_id))
            ok = s.update_one(sql_p, [0, 0, status_code, a_status, str(li), case_id, ])
            if ok:
                return True
            else:
                return False
        # 不需要断言
        # 判断是否存在依赖，存在依赖
        if is_rely_on == 1:
            sql_rely = "select result_data from jk_testcase where case_id =%s"
            ok = s.query_one(sql_rely, [rely_id, ])
            if ok is None:
                logger.info("依赖用例没有回复结果")
                return False
            # 处理读取依赖用例返回数据的value
            rely_result_value = rely_data.split(".")[1:] if rely_data else None
            if rely_result_value is None:
                return False
            ok = ok[0]
            item = "ok"
            for i in range(len(rely_result_value)):
                string = '[{}]'.format(rely_result_value[i]) if isinstance(rely_result_value[i],
                                                                           int) else '["{}"]'.format(
                    rely_result_value[i])
                item = item + string
            try:
                if rely_mode == 1:
                    params[rely_key] = eval(item)
                if rely_mode == 2:
                    header[rely_key] = eval(item)
                if rely_mode == 3:
                    request_data[rely_key] = eval(item)
            except Exception as e:
                logger.error(e)
                return False
            r = request_get(url, header, params, request_data)
            if r is None:
                sql_f = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, modfiy_time=now() where case_id=%s"
                s.update_one(sql_f, [0, 0, 201, case_id, ])
                return False
            li = json.loads(r.text)
            status_code = 200 if r.status_code == 200 else 201
            sql_p = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, result_data=%s, modfiy_time=now() where case_id=%s"
            logger.debug(
                "update jk_testcase set status=0, sub_status=0, result_code={}, result_data={} where case_id={}".format(
                    status_code, li, case_id))
            ok = s.update_one(sql_p, [0, 0, status_code, str(li), case_id, ])
            if ok:
                return True
            else:
                return False
        # 不需要断言，不存在依赖
        r = request_get(url, header, params, request_data)
        if r is None:
            sql_f = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, modfiy_time=now() where case_id=%s"
            s.update_one(sql_f, [0, 0, 201, case_id, ])
            return False
        logger.debug(r.text)
        li = json.loads(r.text)
        status_code = 200 if r.status_code == 200 else 201
        sql_u = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, result_data=%s, modfiy_time=now() where case_id=%s"
        logger.debug(
            "update jk_testcase set status=0, sub_status=0, result_code={}, result_data={} where case_id={}".format(
                status_code, li, case_id))
        ok = s.update_one(sql_u, [0, 0, status_code, str(li), case_id, ])
        if not ok:
            logger.error("更新用例结果失败")
            return False
        else:
            return True
    elif method == "POST":
        # 判断当前是否是否需要断言
        if is_assert == 1:
            # 判断是否存在依赖
            if is_rely_on == 1:
                sql_rely = "select result_data from jk_testcase where case_id =%s"
                ok = s.query_one(sql_rely, [rely_id, ])
                if ok is None:
                    logger.info("依赖用例没有回复结果")
                    return False
                # 处理读取依赖用例返回数据的value
                rely_result_value = rely_data.split(".")[1:] if rely_data else None
                if rely_result_value is None:
                    return False
                ok = ok[0]
                item = "ok"
                for i in range(len(rely_result_value)):
                    string = '[{}]'.format(rely_result_value[i]) if isinstance(rely_result_value[i],
                                                                               int) else '["{}"]'.format(
                        rely_result_value[i])
                    item = item + string
                try:
                    if rely_mode == 1:
                        params[rely_key] = eval(item)
                    if rely_mode == 2:
                        header[rely_key] = eval(item)
                    if rely_mode == 3:
                        request_data[rely_key] = eval(item)
                except Exception as e:
                    logger.error(e)
                    return False
                r = request_post(url, header, params, request_data)
                if r is None:
                    sql_f = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, modfiy_time=now() where case_id=%s"
                    s.update_one(sql_f, [0, 0, 201, case_id, ])
                    return False
                li = json.loads(r.text)
                status_code = 200 if r.status_code == 200 else 201
                if status_code != 200:
                    logger.error("接口返回状态码非200，无法断言")
                    sql_i = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s, modfiy_time=now() where case_id=%s"
                    logger.debug(
                        "update jk_testcase set status=0, sub_status=0, result_code={}, a_status=0, result_data={} where case_id={}".format(
                            status_code, li, case_id))
                    ok = s.update_one(sql_i, [0, 0, status_code, 0, str(li), case_id, ])
                    if not ok:
                        logger.error("数据库更新数据未知异常")
                    return False
                # 处理断言
                a_data_list = a_data.split(".")[1:]
                num = len(a_data_list)
                result = eval_assert(li, num, a_mode, a_data_list, a_result_data)
                a_status = 1 if result else 0
                sql_p = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s, modfiy_time=now() where case_id=%s"
                logger.debug(
                    "update jk_testcase set status=0, sub_status=0, result_code={}, a_status={}, result_data={} where case_id={}".format(
                        status_code, a_status, li, case_id))
                ok = s.update_one(sql_p, [0, 0, status_code, a_status, str(li), case_id, ])
                if ok:
                    return True
                else:
                    return False
            # 不依赖 但是需要断言
            sql = "select result_data from jk_testcase where rely_id=%s"
            da = s.query_one(sql, [rely_id, ])
            if not da:
                logger.error(request_auto.__name__ + "：依赖数据不存在返回数据")
                return False
            r = request_post(url, header, params, request_data)
            if r is None:
                sql_f = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, modfiy_time=now() where case_id=%s"
                s.update_one(sql_f, [0, 0, 201, case_id, ])
                return False
            li = json.loads(r.text)
            status_code = 200 if r.status_code == 200 else 201
            if status_code != 200:
                logger.error("接口返回状态码非200，无法断言")
                sql_i = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s, modfiy_time=now() where case_id=%s"
                logger.debug(
                    "update jk_testcase set status=0, sub_status=0, result_code={}, a_status=0, result_data={} where case_id={}".format(
                        status_code, li, case_id))
                ok = s.update_one(sql_i, [0, 0, status_code, 0, str(li), case_id, ])
                if not ok:
                    logger.error("数据库更新数据未知异常")
                return False
            # 处理断言
            a_data_list = a_data.split(".")[1:]
            num = len(a_data_list)
            result = eval_assert(li, num, a_mode, a_data_list, a_result_data)
            a_status = 1 if result else 0
            sql_p = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s, modfiy_time=now() where case_id=%s"
            logger.debug(
                "update jk_testcase set status=0, sub_status=0, result_code={}, a_status={}, result_data={} where case_id={}".format(
                    status_code, a_status, li, case_id))
            ok = s.update_one(sql_p, [0, 0, status_code, a_status, str(li), case_id, ])
            if ok:
                return True
            else:
                return False
        # 不需要断言
        # 判断是否存在依赖，存在依赖
        if is_rely_on == 1:
            sql_rely = "select result_data from jk_testcase where case_id =%s"
            ok = s.query_one(sql_rely, [rely_id, ])
            if ok is None:
                logger.info("依赖用例没有回复结果")
                return False
            # 处理读取依赖用例返回数据的value
            rely_result_value = rely_data.split(".")[1:] if rely_data else None
            if rely_result_value is None:
                return False
            ok = ok[0]
            item = "ok"
            for i in range(len(rely_result_value)):
                string = '[{}]'.format(rely_result_value[i]) if isinstance(rely_result_value[i],
                                                                           int) else '["{}"]'.format(
                    rely_result_value[i])
                item = item + string
            try:
                if rely_mode == 1:
                    params[rely_key] = eval(item)
                if rely_mode == 2:
                    header[rely_key] = eval(item)
                if rely_mode == 3:
                    request_data[rely_key] = eval(item)
            except Exception as e:
                logger.error(e)
                return False
            r = request_post(url, header, params, request_data)
            if r is None:
                sql_f = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, modfiy_time=now() where case_id=%s"
                s.update_one(sql_f, [0, 0, 201, case_id, ])
                return False
            li = json.loads(r.text)
            status_code = 200 if r.status_code == 200 else 201
            sql_p = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, result_data=%s, modfiy_time=now() where case_id=%s"
            logger.debug(
                "update jk_testcase set status=0, sub_status=0, result_code={}, result_data={} where case_id={}".format(
                    status_code, li, case_id))
            ok = s.update_one(sql_p, [0, 0, status_code, str(li), case_id, ])
            if ok:
                return True
            else:
                return False
        # 不需要断言，不存在依赖
        r = request_post(url, header, params, request_data)
        if r is None:
            sql_f = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, modfiy_time=now() where case_id=%s"
            s.update_one(sql_f, [0, 0, 201, case_id, ])
            return False
        li = json.loads(r.text)
        status_code = 200 if r.status_code == 200 else 201
        sql_u = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, result_data=%s, modfiy_time=now() where case_id=%s"
        logger.debug(
            "update jk_testcase set status=0, sub_status=0, result_code={}, result_data={} where case_id={}".format(
                status_code, li, case_id))
        ok = s.update_one(sql_u, [0, 0, status_code, str(li), case_id, ])
        if not ok:
            logger.error("更新用例结果失败")
            return False
        else:
            return True
