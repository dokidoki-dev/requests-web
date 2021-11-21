import json
from mysql.pymysql import SQLMysql
from web_backend.logger_text.logger_text import log
import requests

logger = log()


def auto_assert(item, num, a_mode, a_data_list, a_result_data) -> bool:
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


def request_auto(item):
    case_id, method, path, url, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, header, request_data = item
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
            r = requests.get(url=(url + "/" + path), headers=header, params=request_data, timeout=10)
            li = json.loads(r.text)
            status_code = 200 if r.status_code == 200 else 201
            if status_code != 200:
                logger.error("接口返回状态码非200，无法断言")
                sql_i = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s where case_id=%s"
                logger.debug("update jk_testcase set status=0, sub_status=2, result_code={}, a_status=0, result_data={} where case_id={}".format(status_code, li, case_id))
                ok = s.update_one(sql_i, [0, 2, status_code, 0, li, case_id, ])
                if not ok:
                    logger.error("数据库更新数据未知异常")
                return False
            # 处理断言
            a_data_list = a_data.split(".")[1:]
            num = len(a_data_list)
            result = auto_assert(li, num, a_mode, a_data_list, a_result_data)
            a_status = 1 if result else 0
            sql_p = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_status=%s, result_data=%s where case_id=%s"
            logger.debug("update jk_testcase set status=0, sub_status=2, result_code={}, a_status={}, result_data={} where case_id={}".format(status_code, a_status, li, case_id))
            ok = s.update_one(sql_p, [0, 2, status_code, a_status, li, case_id, ])
            if ok:
                return True
            else:
                return False
        # 判断是否存在依赖
        if is_rely_on == 1:
            pass
        r = requests.get(url=(url + "/" + path), headers=header, params=request_data)
        li = json.loads(r.text)
        status_code = 200 if r.status_code == 200 else 201
        sql_u = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, result_data=%s where case_id=%s"
        logger.debug("update jk_testcase set status=0, sub_status=2, result_code={}, result_data={} where case_id={}".format(status_code, li))
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

