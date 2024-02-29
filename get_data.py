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
    "排名, 书名, 作者, 翻译者, 封面, 出版社时间, 出版社, 推荐率, 现价, 定价,折扣, 大类型, 子类型, 开本, 纸张, 包装, 是否套装,ISBN , 评论数量, 评论标签, 编辑推荐")


# 获取2023 年所有月份的图书信息
def get_book_info(url, csv_name=None, year=None, list_num=1):
    """
    获取图书信息并解析，写入到文件中
    :param url: string 地址
    :return:
    """
    # 遍历前12个月
    book_info_list = []
    # csv_name.replace("src", "")
    # filename = "./data/" + year + "/book_info" + month + "month.csv"
    #
    # # 写入csv文件的头
    # with open(filename, "a", encoding="utf-8", newline="") as f:
    #     f.write(HEADINFO + "\n")

    # 读取csv文件的url

    browser.get(url)

    # 解析要获取的数据
    # list_num = browser.find_elements(By.CSS_SELECTOR, '<div class="list_num red">1.</div>') # 编号
    # 排行榜
    book_info_list.append(list_num)
    # 书名
    book_name = browser.find_element(By.XPATH, '//*[@id="product_info"]/div[1]/h1')
    print("书名：", book_name.get_attribute("title"))
    book_info_list.append(book_name.get_attribute("title"))
    # 作者
    author = browser.find_element(By.XPATH, '//*[@id="author"]')
    author = author.text.replace("作者:", "")
    print("作者信息：", author)
    book_info_list.append(author)
    # 翻译者

    # 封面图
    pic = browser.find_element(By.XPATH, '//*[@id="largePic"]')
    print("封面图：", pic.get_attribute("src"))
    book_info_list.append(pic.get_attribute("src"))
    # 出版社时间
    publication_time = browser.find_element(By.XPATH, '//*[@id="product_info"]/div[2]/span[3]')
    publication_time = publication_time.text.replace("出版时间:", "")
    print("出版时间：", publication_time)
    book_info_list.append(publication_time)

    # 出版社
    press = browser.find_element(By.XPATH, '//*[@id="product_info"]/div[2]/span[2]/a')
    book_info_list.append(press.text)

    # 推荐率

    # 现价
    current_price = browser.find_element(By.XPATH, '//*[@id="dd-price"]')
    current_price = current_price.text.replace("¥", "")
    print("现价：", current_price)
    book_info_list.append(current_price)
    # 定价
    pricing = browser.find_element(By.XPATH, '//*[@id="original-price"]')
    pricing = pricing.text.replace("¥", "")
    print("定价", pricing)
    book_info_list.append(pricing)
    # 折扣
    discount = browser.find_element(By.XPATH, '//*[@id="dd-zhe"]')
    discount = discount.text.replace("折)", "")
    discount = discount.replace("(", "")

    print("折扣:", discount)
    book_info_list.append(discount)
    # 大类型
    type_list = browser.find_elements(By.XPATH, '//*[@id="detail-category-path"]/span/a[2]')
    for i in type_list:
        print("大类型：", i.text)
        book_info_list.append(i.text)
    # 子类型
    subtype = browser.find_element(By.XPATH, '//*[@id="detail-category-path"]/span/a[3]')
    print("子类型：", subtype.text)
    book_info_list.append(subtype.text)
    # 开本
    book_size = browser.find_element(By.XPATH, '//*[@id="detail_describe"]/ul/li[1]')
    book_size = book_size.text.replace("开 本：", "")
    print("开本：", book_size)
    book_info_list.append(book_size)
    # 纸张
    paper = browser.find_element(By.XPATH, '//*[@id="detail_describe"]/ul/li[2]')
    paper = paper.text.replace("纸 张：", "")
    print("纸张：", paper)
    book_info_list.append(paper)
    # 包装
    packaging = browser.find_element(By.XPATH, '//*[@id="detail_describe"]/ul/li[3]')
    packaging = packaging.text.replace("包 装：", "")
    print("包装：", packaging)
    book_info_list.append(packaging)
    # 是否套装
    suit = browser.find_element(By.XPATH, '//*[@id="detail_describe"]/ul/li[4]')
    suit = suit.text.replace("是否套装：", "")
    print("是否套装：", suit)
    book_info_list.append(suit)
    # 国际标准书号ISBN
    isbn = browser.find_element(By.XPATH, '//*[@id="detail_describe"]/ul/li[5]')
    isbn = isbn.text.replace("国际标准书号ISBN：", "")
    print("国际标准书号ISBN：", isbn)
    book_info_list.append(isbn)
    # 评论数量
    comment_num = browser.find_element(By.XPATH, '//*[@id="comm_num_down"]')
    print(comment_num.text)
    print("评论数量：", comment_num.text)
    book_info_list.append(comment_num.text)
    # 评论标签
    comment_tag = browser.find_elements(By.XPATH, '//*[@id="comment_tags_div"]/div[2]/span')
    print("评论标签：", comment_tag)
    for i in comment_tag:
        comment_tag_list = []
        info = i.find_element(By.XPATH, 'a').text
        comment_tag_list.append(info)
        print("评论标签：", comment_tag_list)
        book_info_list.append(comment_tag_list)

    # 编辑推荐
    editor_recommend = browser.find_element(By.XPATH, '//*[@id="abstract"]/div[2]')
    print("编辑推荐：", editor_recommend.text)
    book_info_list.append(editor_recommend.text)

    print(book_info_list)
    # 写入到csv文件中
    # logger.info("开始获取2023年" + month + "月的图书信息到文件中...")
    # with open(filename, "a", encoding="utf-8", newline="") as f:
    #     print(book_info_list)
    #     writer = csv.writer(f)
    #     writer.writerows(book_info_list)
    # logger.info("写入2023年" + month + "月的图书信息到文件中结束")

    return


def get_num_src(year, month):
    # 遍历前12个月

    filename = "./data/" + year + "/bests_sellers_" + month + "_month_src.csv"
    row_url = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-year-" + year + "-" + \
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
    get_book_info("http://product.dangdang.com/29311943.html")

    # for i in range(2020, 2024):
    #     get_num_src(str(i), "0")
