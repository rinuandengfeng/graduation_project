import logging
import logging.handlers
from time import strftime
import os

# 创建记录器对象
logger = logging.getLogger()

# 日志文件名
basePath = os.path.abspath(os.path.dirname(__file__))

LOG_INFOFILENAME = strftime('logs\\all_%Y_%m_%d.log')


# 处理函数
def set_logger():
    path = os.path.dirname(basePath + '\\logs\\')

    if not os.path.exists(path):
        # 创建目录
        os.makedirs(path)

    # 设置日志隔离级别
    logger.setLevel(logging.INFO)
    # 创建时间切割的格式化对象
    time_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s  %(message)s')
    # 创建处理器对象
    file_handler = logging.handlers.TimedRotatingFileHandler(
        LOG_INFOFILENAME, when='midnight', interval=1, backupCount=7, encoding='utf-8')
    # 给按照时间进行日志切割处理器对象应用格式化对象
    file_handler.setFormatter(time_formatter)
    # 记录器增加处理器
    logger.addHandler(file_handler)

    # 终端处理器对象
    ter_handler = logging.StreamHandler()
    ter_formatter = logging.Formatter(
        '%(asctime)s %(levelname)s  %(message)s')

    # 记录器增加处理器
    logger.addHandler(ter_handler)

    # # 将日志文件写入磁盘记录错误
    # error_handler = logging.FileHandler(LOG_ERRORFILENAME)
    # # 设置格式化器
    # error_formatter = logging.Formatter(
    #     '%(asctime)s %(levelname)s %(filename)s[:%(lineno)d] %(message)s')
    # error_handler.setFormatter(error_handler)
    # # 设置隔离级别
    # error_handler.setLevel(logging.ERROR)

    # # 在记录器中添加处理器
    # logger.addHandler(error_handler)
    return


set_logger()
