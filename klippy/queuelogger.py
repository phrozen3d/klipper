####################################
#项目名称：
#芯片类型: 
#功能: 
#研发人员：蓝才刚
#开发时间: 20230830
####################################


import logging, logging.handlers, threading, queue, time
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
# Class to forward all messages through a queue to a background thread
class QueueHandler(logging.Handler):
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, queue):
        logging.Handler.__init__(self)
        self.queue = queue
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def emit(self, record):
        try:
            self.format(record)
            record.msg = record.message
            record.args = None
            record.exc_info = None
            self.queue.put_nowait(record)
        except Exception:
            self.handleError(record)
####################################
#类名：
#功能描述：蓝才刚-20230830
####################################
# Class to poll a queue in a background thread and log each message
class QueueListener(logging.handlers.TimedRotatingFileHandler):
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def __init__(self, filename):
        logging.handlers.TimedRotatingFileHandler.__init__(
            self, filename, when='midnight', backupCount=5)
        self.bg_queue = queue.Queue()
        self.bg_thread = threading.Thread(target=self._bg_thread)
        self.bg_thread.start()
        self.rollover_info = {}
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def _bg_thread(self):
        while 1:
            record = self.bg_queue.get(True)
            if record is None:
                break
            self.handle(record)
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def stop(self):
        self.bg_queue.put_nowait(None)
        self.bg_thread.join()
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def set_rollover_info(self, name, info):
        if info is None:
            self.rollover_info.pop(name, None)
            return
        self.rollover_info[name] = info
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def clear_rollover_info(self):
        self.rollover_info.clear()
    ####################################
    #函数名称：
    #输入参数：
    #返 回 值:
    #功能描述：蓝才刚-20230830
    ####################################
    def doRollover(self):
        logging.handlers.TimedRotatingFileHandler.doRollover(self)
        lines = [self.rollover_info[name]
                 for name in sorted(self.rollover_info)]
        lines.append(
            "=============== Log rollover at %s ===============" % (
                time.asctime(),))
        self.emit(logging.makeLogRecord(
            {'msg': "\n".join(lines), 'level': logging.INFO}))

MainQueueHandler = None
####################################
#函数名称：
#输入参数：
#返 回 值:
#功能描述：蓝才刚-20230830
####################################
def setup_bg_logging(filename, debuglevel):
    global MainQueueHandler
    ql = QueueListener(filename)
    MainQueueHandler = QueueHandler(ql.bg_queue)
    root = logging.getLogger()
    root.addHandler(MainQueueHandler)
    root.setLevel(debuglevel)
    return ql
####################################
#函数名称：
#输入参数：
#返 回 值:
#功能描述：蓝才刚-20230830
####################################
def clear_bg_logging():
    global MainQueueHandler
    if MainQueueHandler is not None:
        root = logging.getLogger()
        root.removeHandler(MainQueueHandler)
        root.setLevel(logging.WARNING)
        MainQueueHandler = None
