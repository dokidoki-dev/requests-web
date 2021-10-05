from flask import Flask
import settings
from web_backend.user.view import user


def create_app():
    app = Flask(__name__)
    # 导入配置文件
    app.config.from_object(settings.Development)
    # 注册蓝图
    app.register_blueprint(user)
    return app
