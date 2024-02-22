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

time.sleep(5)
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
        # list_num = browser.find_elements(By.CSS_SELECTOR, '<div class="list_num red">1.</div>') # 编号
        # 排行榜
        li = browser.find_elements(By.CSS_SELECTOR, 'body > div.bang_list_box > ul > li')
        print(li)
        list_num = browser.find_elements(By.CSS_SELECTOR, "div.list_num")  # 编号
        book_info_list.append(list_num)
        print(list_num)

        # 书名
        pic_row = browser.find_elements(By.CSS_SELECTOR, "div.pic > a")
        book_info_list.append(pic_row.get_attribute("alt"))
        # 作者
        author = browser.find_elements(By.CSS_SELECTOR, "")

        # 封面
        book_info_list.append(pic_row.get_attribute("src"))  # 封面图

    # 写入到csv文件中
    logger.info("开始获取2023年" + month + "月的图书信息到文件中...")
    with open(filename, "a", encoding="utf-8", newline="") as f:
        print(book_info_list)
        writer = csv.writer(f)
        writer.writerows(book_info_list)
    logger.info("写入2023年" + month + "月的图书信息到文件中结束")

    return


def get_num_src(year, month):
    # 遍历前12个月

    filename = "./data/" + year + "/book_info_" + month + "_month_src.csv"
    row_url = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-month-2023-" + \
              month + "-1-"
    num_src = ('排名,图书地址')
    # 写入csv文件的头
    with open(filename, "a", encoding="utf-8", newline="") as f:
        f.write(num_src + "\n")
    for page in range(1, 26):
        url = row_url + str(page)
        browser.get(url)

        logger.info("开始获取" + year + "年" + month + "月第" + str(
            page) + "页的图书编号和图书地址写入到" + filename + "文件中...")
        # 获取排行和图书的地址
        list_li = browser.find_elements(By.XPATH,
                                        "/html/body/div[3]/div[3]/div[2]/ul/li")

        for li in list_li:
            info = []
            list_num = li.find_element(By.CSS_SELECTOR, 'div.list_num').text.replace(".", "")

            info.append(list_num)

            book_src = li.find_element(By.CSS_SELECTOR,
                                       'div.name > a')
            info.append(book_src.get_attribute("href"))
            # 写入到csv文件中

            with open(filename, "a", encoding="utf-8", newline="") as f:
                print(info)
                writer = csv.writer(f)
                writer.writerow(info)
        logger.info("写入" + year + "年" + month + "月第" + str(page) + "页的图书信息到" + filename + "文件中结束")


if __name__ == "__main__":
    time.sleep(3)
    # get_book_info("2023", "2")

    get_num_src("2023", "6")
