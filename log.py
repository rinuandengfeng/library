import logging

import logging.handlers
import os

import datetime
from time import strftime

#日志文件名
LOG_FILENAME = strftime("logs\%Y-%m-%d.log")

#创建记录器对象
logger = logging.getLogger()

#日志函数
def set_log():
    #目录
    path = os.path.dirname(os.getcwd()+"\\logs\\")
    if not os.path.exists(path):
        os.makedirs(path)
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter('%(asctime)s %(levelname)s :%(message)s')
    #创建终端处理器
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    #创建文本处理器
    file_handler = logging.handlers.TimedRotatingFileHandler(LOG_FILENAME,interval=1,
            atTime = datetime.time(0,0,0,0),encoding='utf-8')
    file_handler.setFormatter(formatter)


    #添加处理器
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

set_log()

