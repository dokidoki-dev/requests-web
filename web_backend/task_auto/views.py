import json
import time
from web_backend.logger_text.logger_text import log
from flask import Blueprint, request, Response
from mysql.pymysql import SQLMysql
from web_backend.auto_queue.t_queue import auto_queue

q = auto_queue()
task_auto = Blueprint('task_auto', __name__)
logger = log()


# 任务
def task(taskId, consuming):
    # print('工人【】正在处理任务【%d】：do something...' % taskId)
    # 模拟任务耗时(秒)
    time.sleep(consuming)
    print('任务：done', taskId)


@task_auto.route("/task_add", methods=["POST"])
def task_add():
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
    case_group = request.json.get("case_group", None)
    case_type = 0 if request.json.get("case_type", 1) == 0 else 1  # 1表示单个用例 0表示用例组
    if not case_group and not case_id:
        data["code"] = 30001
        data["msg"] = "参数非法"
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    s = SQLMysql()
    # 查询当前是否存在用例或者用例组
    if case_type == 1:
        # 单个用例  单个用例不存在依赖，所以is_rely_on一定为0
        sql = "select method, path, url, status, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, header, request_data from jk_testcase where case_id=%s"
        logger.debug("select method, path, url, status, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, header, request_data from jk_testcase where case_id={}".format(case_id))
        li = s.query_one(sql, [case_id, ])
        logger.debug(li)
        if li is None:
            data["code"] = 30002
            data["msg"] = "当前用例不存在"
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        method, path, url, status, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, header, request_data = li
        # 判断当前用例是否处于正在执行队列中，处于执行中时，不允许再次执行此用例
        if status == 1:
            data["code"] = 39999
            data["msg"] = "当前用例已经处于执行队列中"
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        lists = {
            "case_id": case_id,
            "method": method,
            "path": path,
            "url": url,
            "is_assert": is_assert,
            "a_data": a_data,
            "a_mode": a_mode,
            "a_type": a_type,
            "a_result_data": a_result_data,
            "is_rely_on": 0,
            "header": header,
            "request_data": request_data
        }
        # 处理环境变量的问题
        url = eval(lists["url"])
        header = eval(lists["header"])
        if url["mode"] == "env":
            sql_s = "select v_data from jk_variable from where v_name=%s"
            logger.debug("select v_data from jk_variable from where v_name={}".format(url["data"]))
            ok = s.query_one(sql_s, [url["data"], ])
            logger.debug(ok)
            if ok is None:
                data["code"] = 30003
                data["msg"] = "未知错误"
                logger.info("返回信息" + str(data))
                return Response(json.dumps(data), content_type='application/json')
            lists["url"] = ok[0]
        elif url["mode"] == "un_env":
            lists["url"] = url["data"]
        if header["mode"] == "env":
            sql_s = "select v_data from jk_variable from where v_name=%s"
            logger.debug("select v_data from jk_variable from where v_name={}".format(header["data"]))
            ok = s.query_one(sql_s, [header["data"], ])
            logger.debug(ok)
            if ok is None:
                data["code"] = 30004
                data["msg"] = "未知错误"
                logger.info("返回信息" + str(data))
                return Response(json.dumps(data), content_type='application/json')
            lists["header"] = ok[0]
        elif header["mode"] == "un_env":
            lists["header"] = header["data"]
        sql_status = "update jk_testcase set status=1 where case_id=%s"
        logger.debug("update jk_testcase set status=1 where case_id={}".format(case_id))
        ok = s.update_one(sql_status, [case_id, ])
        if not ok:
            data["code"] = 99999
            data["msg"] = "未知错误"
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        # 放入队列
        q.put((task, lists))
        data["code"] = 30009
        data["msg"] = "添加成功"
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
    elif case_type == 0:
        # 用例组
        sql = "select group_id from jk_cgroups where group_name=%s"
        logger.debug("select group_id from jk_cgroups where group_name={}".format(case_group))
        li = s.query_one(sql, [case_group, ])
        if li is None:
            data["code"] = 30005
            data["msg"] = "当前分组不存在"
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        # 查询用例组下的所有用例
        sql_s = "select case_id, method, path, url, status, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, header, request_data from jk_testcase where group_id=%s"
        logger.debug("select case_id, method, path, url, status, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, header, request_data from jk_testcase where group_id={}".format(li[0]))
        lists = s.query_all(sql_s, [li[0], ])
        logger.debug(lists)
        if not lists:
            data["code"] = 30006
            data["msg"] = "当前分组没有用例"
            logger.info("返回信息" + str(data))
            return Response(json.dumps(data), content_type='application/json')
        all = []
        for i in range(len(lists)):
            case_id, method, path, url, status, is_assert, a_data, a_mode, a_type, a_result_data, is_rely_on, header, request_data = lists[i]
            list_all = {
                "case_id": case_id,
                "method": method,
                "path": path,
                "url": url,
                "is_assert": is_assert,
                "a_data": a_data,
                "a_mode": a_mode,
                "a_type": a_type,
                "a_result_data": a_result_data,
                "is_rely_on": 0,
                "header": header,
                "request_data": request_data
            }
            # 判断当前用例是否处于正在执行队列中，处于执行中时，不允许用例组执行
            if status == 1:
                data["code"] = 39999
                data["msg"] = "部分用例已经处于执行队列中"
                logger.info("返回信息" + str(data))
                return Response(json.dumps(data), content_type='application/json')
            # 处理环境变量的问题
            url = eval(list_all["url"])
            header = eval(list_all["header"])
            if url["mode"] == "env":
                sql_s = "select v_data from jk_variable from where v_name=%s"
                logger.debug("select v_data from jk_variable from where v_name={}".format(url["data"]))
                ok = s.query_one(sql_s, [url["data"], ])
                logger.debug(ok)
                if ok is None:
                    data["code"] = 30007
                    data["msg"] = "未知错误"
                    logger.info("返回信息" + str(data))
                    return Response(json.dumps(data), content_type='application/json')
                list_all["url"] = ok[0]
            elif url["mode"] == "un_env":
                list_all["url"] = url["data"]
            if header["mode"] == "env":
                sql_s = "select v_data from jk_variable from where v_name=%s"
                logger.debug("select v_data from jk_variable from where v_name={}".format(header["data"]))
                ok = s.query_one(sql_s, [header["data"], ])
                logger.debug(ok)
                if ok is None:
                    data["code"] = 30008
                    data["msg"] = "未知错误"
                    logger.info("返回信息" + str(data))
                    return Response(json.dumps(data), content_type='application/json')
                list_all["header"] = ok[0]
            elif header["mode"] == "un_env":
                list_all["header"] = header["data"]
            sql_status = "update jk_testcase set status=1 where case_id=%s"
            logger.debug("update jk_testcase set status=1 where case_id={}".format(case_id))
            ok = s.update_one(sql_status, [case_id, ])
            if not ok:
                data["code"] = 99999
                data["msg"] = "未知错误"
                logger.info("返回信息" + str(data))
                return Response(json.dumps(data), content_type='application/json')
            all.append((task, list_all))
        #  放入队列
        for i in range(len(all)):
            q.put((all[i]))
        data["code"] = 30009
        data["msg"] = "添加成功"
        data["result"] = True
        logger.info("返回信息" + str(data))
        return Response(json.dumps(data), content_type='application/json')
