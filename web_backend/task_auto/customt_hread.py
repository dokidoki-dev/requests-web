import threading
from web_backend.auto_queue.t_queue import auto_queue
from web_backend.logger_text.logger_text import log
from mysql.pymysql import SQLMysql

logger = log()
q = auto_queue()


# 自定义线程
class CustomThread(threading.Thread):
    def __init__(self, queue, **kwargs):
        self.sql = "update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_result_data=%s, a_status=%s, result_data=%s where case_id=%s"
        super(CustomThread, self).__init__(**kwargs)
        self.__queue = queue

    def run(self):
        while True:
            # (线程)获取任务
            item = self.__queue.get()
            print(item)
            # 执行任务
            # item[0](*item[1:])
            # 告诉队列，任务已完成
            self.__queue.task_done()

    def __update_status(self, case_id) -> bool:
        logger.debug("update jk_testcase set status=%s, sub_status=%s, result_code=%s, a_result_data=%s, a_status=%s, result_data=%s where case_id={}".format(case_id))
        s = SQLMysql()
        ok = s.update_one(self.sql, [case_id, ])
        if ok:
            return True
        else:
            return False


def start_thread() -> None:
    # (启动1个线程) 暂时不要使用多线程操作
    for i in range(1):
        t = CustomThread(q, daemon=True)
        # 开始启动线程
        t.start()
