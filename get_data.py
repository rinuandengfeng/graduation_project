import json
import re
import time

from selenium.webdriver import Chrome, ChromeOptions

from selenium.webdriver.common.by import By
import csv
from subprocess import Popen
from utils.log import logger

# 命令开启远程调用
Popen(r"C:\Program Files\Google\Chrome\Application\chrome --remote-debugging-port=9876")

# 设置浏览器 并关闭左上角chrome正受到自动测试软件的控制提示
op = ChromeOptions()
op.add_experimental_option("debuggerAddress", "127.0.0.1:9876")
# op.add_experimental_option('useAutomationExtension', False)


browser = Chrome(options=op)

# 进入当当网首页
browser.get("https://www.dangdang.com/")

time.sleep(10)
HEADINFO = (
    "排名, 书名, 作者, 封面, 出版社时间, 出版社, 翻译者, 推荐率, 现价, 原价,折扣, 大类型, 子类型, 开本, 纸张, 包装, 是否套装, 评论数量, 评论标签, 编辑推荐")


# 获取2023 年所有月份的图书信息
def get_book_info(year, month):
    """
    获取每年各个月份的图书数据
    :param year: string 年份
    :param month: string 年份
    :return:
    """
    # 遍历前12个月
    book_info_list = []
    filename = "./data/" + year + "/book_info" + month + "month.csv"
    row_url = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-month-2023-" + \
              month + "-1-"

    # 写入csv文件的头
    with open(filename, "a", encoding="utf-8", newline="") as f:
        f.write(HEADINFO + "\n")

    for page in range(1, 2):
        url = row_url + str(page)
        browser.get(url)

        # 解析要获取的数据

    # 写入到csv文件中
    logger.info("开始获取2023年" + month + "月的图书信息到文件中...")
    with open(filename, "a", encoding="utf-8", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(book_info_list)
    logger.info("写入2023年" + month + "月的图书信息到文件中结束")

    return


if __name__ == "__main__":
    time.sleep(5)
    get_book_info("2023", "2")
    # 结束关闭9876端口
    # time.sleep(10)
    # Popen("taskkill  -F -PID 9876")
