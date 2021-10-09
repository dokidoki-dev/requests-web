from flask import Blueprint, request, Response
import json
import re
from mysql.pymysql import SQLMysql

env_variable = Blueprint('env_variable', __name__)


@env_variable.route('/env', methods=['GET', 'POST'])
def env_var():
    if request.method == "GET":
        page = request.args.get('page', 1)
        limit = request.args.get('limit', 10)
        variable = request.args.get('variable', None)
        context = request.args.get('context', None)
        # 处理
        pattern = re.compile(r'^[\d]{1,3}$')
        page = pattern.search(str(page))
        limit = pattern.search(str(limit))
        if page is None or limit is None:
            data = {
                "object": None,
                "msg": "参数非法",
                "code": 7998,
                "result": False,
                "status": "success"
            }
            return Response(json.dumps(data), content_type='application/json')
        else:
            s = SQLMysql()
            s_sql = "select group_id from jk_vgroups where group_name=%s"
            s_all = "select group_id from jk_vgroups"
            sql = "select v_id, v_name, v_data, group_id from jk_variable where is_delete=0 and group_id=%s and v_data like %s"
            if variable is None:
                group_ids = s.query_all(s_all)
                if not group_ids:
                    data = {
                        "object": None,
                        "msg": "暂无数据",
                        "code": 7994,
                        "result": True,
                        "status": "success"
                    }
                    return Response(json.dumps(data), content_type='application/json')
                else:
                    sql = "select v.v_id, v.v_name, v.v_data, g.group_name from jk_vgroups g, jk_variable v WHERE v.group_id=g.group_id"
                    l_n = s.query_all(sql)
                    if not l_n:
                        data = {
                            "object": None,
                            "msg": "暂无数据",
                            "code": 7993,
                            "result": True,
                            "status": "success"
                        }
                        return Response(json.dumps(data), content_type='application/json')
                    else:
                        lists_all = []
                        for i in range(len(l_n)):
                            v_id, v_name, v_data, group_name = l_n[i]
                            lists_all.append({
                                "id": v_id,
                                "name": v_name,
                                "data": v_data,
                                "group_name": group_name
                            })
                        data = {
                            "object": lists_all,
                            "msg": "查询成功",
                            "code": 7992,
                            "result": True,
                            "status": "success"
                        }
                        return Response(json.dumps(data), content_type='application/json')
            else:
                group_id = s.query_one(s_sql, [str(variable), ])
                if group_id is None:
                    data = {
                        "object": None,
                        "msg": "无相关结果",
                        "code": 7997,
                        "result": False,
                        "status": "success"
                    }
                    return Response(json.dumps(data), content_type='application/json')
                li = s.query_all(sql, [group_id, ('%' + context + '%'), ])
                if not li:
                    data = {
                        "object": None,
                        "msg": "暂无数据",
                        "code": 7996,
                        "result": True,
                        "status": "success"
                    }
                    return Response(json.dumps(data), content_type='application/json')
                else:
                    list_s = []
                    for i in range(len(li)):
                        v_id, v_name, v_data, group_id = li[i]
                        list_s.append({
                            "id": v_id,
                            "name": v_name,
                            "data": v_data,
                            "group_name": variable
                        })
                    data = {
                        "object": list_s,
                        "msg": "查询成功",
                        "code": 7995,
                        "result": True,
                        "status": "success"
                    }
                    return Response(json.dumps(data), content_type='application/json')
    elif request.method == "POST":
        variable = request.json.get('variable', "testing_env")
        status = request.json.get('status', 0)
        context = request.json.get('context', None)
        if context is None:
            data = {
                "object": None,
                "msg": "内容校验不通过",
                "code": 7999,
                "result": False,
                "status": "success"
            }
            return Response(json.dumps(data), content_type='application/json')
