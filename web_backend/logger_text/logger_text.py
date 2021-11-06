from loguru import logger
import os
import settings

logger.remove(handler_id=None)
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
Log_level = settings.Log_level
# ERROR日志
logger.add(
    "%s/logs/{time:YYYYMMDD}-error.log" % base_dir,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | file:{file.path} | line:{line} | function:{function} | 消息: {message}",
    filter=lambda x: True if x["level"].name == "ERROR" else False,
    rotation="00:00", retention=7, level='ERROR', encoding='utf-8',
    backtrace=True, diagnose=True
)
# INFO 日志
logger.add(
    "%s/logs/{time:YYYYMMDD}.log" % base_dir,
    format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {level} | file:{file} | line:{line} | function:{function} | 消息: {message}",
    filter=lambda x: False if x["level"].name == "ERROR" else True,
    rotation="00:00", retention=7, level=Log_level, encoding='utf-8',
    backtrace=True, diagnose=True
)


def log():
    return logger
