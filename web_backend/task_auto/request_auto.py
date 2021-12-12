import json
from mysql.pymysql import SQLMysql
from web_backend.logger_text.logger_text import log
import requests
import ast

logger = log()


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


# 第二种方案：使用eval()函数    不推荐，可能存在未知安全问题
# 将读取到的断言数据，分割成列表后，读取列表长度，然后通过循环凭借字符串格式的读取变量，然后放入eval()函数处理
# 例如    item = "data["msg"][0]["num"]"   ->  eval(item)   此时 eval(item) 经过处理就等同于 data["msg"][0]["num"]
# 也可以将eval(item)赋值   p = eval(item)  此时变量p就等同于 data["msg"][0]["num"]   然后即可进行断言操作

# 断言处理函数 可能存在不安全的问题
def eval_assert(item: object, num: int, a_mode, a_data_list, a_result_data) -> bool:
    """
    item参数虽然未使用，但是不能删除，因为eval()函数需要使用
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


def request_auto(item: object):
    """
    依赖只支持去读依赖接口返回值
    """
    case_id, method, path, url, params, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, rely_id, header, request_data = item
    # 数据处理 转换为字典   params    request_data
    if params is None:
        logger.info("params: None")
    else:
        params = ast.literal_eval(params)
    if request_data is None:
        logger.info("request_data: None")
    else:
        request_data = ast.literal_eval(request_data)
    sql = "update jk_testcase set sub_status=1 where case_id=%s"
    # 更新用例状态
    s = SQLMysql()
    logger.debug("update jk_testcase set sub_status=1 where case_id={}".format(case_id))
    ok = s.update_one(sql, [case_id, ])
    if not ok:
        logger.error("更新用例子状态失败")
        return False
    # 判断请求方式
    if method == "GET":
        # 判断当前是否是否需要断言
        if is_assert == 1:
            # 判断是否存在依赖
            if is_rely_on == 1:
                pass
            sql = "select result_data from jk_testcase where rely_id=%s"
            da = s.query_one(sql, [rely_id, ])
            if not da:
                logger.error(request_auto.__name__ + "：依赖数据不存在返回数据")
                return

            r = requests.get(url=(url + "/" + path), headers=header, params=params, data=request_data, timeout=10)
            li = json.loads(r.text)
            status_code = 200 if r.status_code == 200 else 201
            if status_code != 200:
                logger.error("接口返回状态码非200，无法断言")
                sql_i = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s where case_id=%s"
                logger.debug(
                    "update jk_testcase set status=0, sub_status=2, result_code={}, a_status=0, result_data={} where case_id={}".format(
                        status_code, li, case_id))
                ok = s.update_one(sql_i, [0, 2, status_code, 0, li, case_id, ])
                if not ok:
                    logger.error("数据库更新数据未知异常")
                return False
            # 处理断言
            a_data_list = a_data.split(".")[1:]
            num = len(a_data_list)
            result = eval_assert(li, num, a_mode, a_data_list, a_result_data)
            a_status = 1 if result else 0
            sql_p = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s where case_id=%s"
            logger.debug(
                "update jk_testcase set status=0, sub_status=2, result_code={}, a_status={}, result_data={} where case_id={}".format(
                    status_code, a_status, li, case_id))
            ok = s.update_one(sql_p, [0, 2, status_code, a_status, li, case_id, ])
            if ok:
                return True
            else:
                return False
        # 判断是否存在依赖
        if is_rely_on == 1:
            pass
        r = requests.get(url=(url + "/" + path), headers=header, params=params, data=request_data, timeout=10)
        li = json.loads(r.text)
        status_code = 200 if r.status_code == 200 else 201
        sql_u = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, result_data=%s where case_id=%s"
        logger.debug(
            "update jk_testcase set status=0, sub_status=2, result_code={}, result_data={} where case_id={}".format(
                status_code, li))
        ok = s.update_one(sql_u, [0, 2, status_code, li, ])
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
                pass
        # 判断是否存在依赖
        if is_rely_on == 1:
            pass
        requests.get()
