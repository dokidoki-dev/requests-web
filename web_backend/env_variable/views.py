from flask import Blueprint, request, Response
import json

env_variable = Blueprint('env_variable', __name__)


@env_variable.route('/env', methods=['GET', 'POST'])
def env_variable():
    if request.method == "GET":
        page = request.json.get('page', 1)
        limit = request.json.get('limit', 10)
        variable = request.json.get('variable', None)
        context = request.json.get('context', None)
        # 处理
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