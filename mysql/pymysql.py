import pymysql
from web_backend.logger_text.logger_text import log

logger = log()

mysql_config = {
    "host": "127.0.0.1",
    "post": 3306,
    "user": "root",
    "passwd": "shenyongfu",
    "db": "request_web"
}

pymysql.connections.DEBUG = False  # 开启DEBUG


class SQLMysql(object):
    def __init__(self):
        self.conn = pymysql.connect(host=mysql_config['host'],
                                    port=mysql_config['post'],
                                    user=mysql_config['user'],
                                    passwd=mysql_config['passwd'],
                                    db=mysql_config['db'])
        self.cur = self.conn.cursor()

    def __del__(self):
        self.cur.close()
        self.conn.close()

    def query_one(self, sql, args=None):
        self.cur.execute(sql, args)
        return self.cur.fetchone()

    def query_all(self, sql, args=None):
        self.cur.execute(sql, args)
        return self.cur.fetchall()

    def create_one(self, sql, args=None):
        try:
            # 防止SQL注入
            self.cur.execute(sql, args)
            self.conn.commit()
            return True
        except Exception as e:
            # 异常回滚
            self.conn.rollback()
            logger.error(e)
            return False

    def update_one(self, sql, args=None):
        try:
            self.cur.execute(sql, args)
            self.conn.commit()
            return True
        except Exception as e:
            self.conn.rollback()
            logger.error(e)
            return False
