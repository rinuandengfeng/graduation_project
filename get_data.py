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


def read_csv(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == "排名":
                continue
            analysis_book_info(row[1], file_path, "2023", row[0])
    time.sleep(3)


# 获取2023 年所有月份的图书信息
def analysis_book_info(url, csv_name, year, list_num):
    """
    获取图书信息并解析，写入到文件中
    :param url:  图书的地址
    :param csv_name: url文件名
    :param year: 年份
    :param list_num: 排行榜
    :return:
    """
    # 遍历前12个月
    book_info_list = []

    # 在新文件中写入csv文件的头
    head_info = (
        "排名, 书名, 作者, 翻译者, 封面, 出版社时间, 出版社, 现价, 定价,折扣, 大类型, 子类型, 开本, 纸张, 包装, 是否套装,ISBN , 编辑推荐 ,评论数量 , 评论标签")

    csv_name = csv_name.replace("_src", "")
    filename = "./data/" + year + "/" + csv_name
    try:
        with open(filename, "r", encoding="utf-8", newline="") as f:
            logger.info("文件" + filename + "已经存在，不需要创建文件")
    except Exception as e:
        with open(filename, "a", encoding="utf-8", newline="") as f:
            logger.info("创建文件" + filename + "并将头信息写入到文件中")
            f.write(head_info + "\n")

    # 读取csv文件的url
    browser.get(url)
    # 解析要获取的数据
    # 排行榜
    book_info_list.append(list_num)
    logger.info("开始解析" + year + "年" + url + "的图书信息...")
    # 书名
    book_name = browser.find_element(By.XPATH, '//*[@id="product_info"]/div[1]/h1')
    book_info_list.append(book_name.get_attribute("title"))
    # 作者
    author = browser.find_element(By.XPATH, '//*[@id="author"]')
    author = author.text.replace("作者:", "")
    author = author.split("著")
    book_info_list.append(author)
    # 翻译者
    try:
        author = author[1].split("译")
        if len(author) > 1:
            book_info_list.append(author[0])
        else:
            book_info_list.append("None")
    except Exception as e:
        book_info_list.append("None")

    # 封面图
    pic = browser.find_element(By.XPATH, '//*[@id="largePic"]')
    book_info_list.append(pic.get_attribute("src"))
    # 出版社时间
    publication_time = browser.find_element(By.XPATH, '//*[@id="product_info"]/div[2]/span[3]')
    publication_time = publication_time.text.replace("出版时间:", "")
    book_info_list.append(publication_time)

    # 出版社
    press = browser.find_element(By.XPATH, '//*[@id="product_info"]/div[2]/span[2]/a')
    book_info_list.append(press.text)
    # 现价
    current_price = browser.find_element(By.XPATH, '//*[@id="dd-price"]')
    current_price = current_price.text.replace("¥", "")
    book_info_list.append(current_price)
    # 定价
    pricing = browser.find_element(By.XPATH, '//*[@id="original-price"]')
    pricing = pricing.text.replace("¥", "")
    book_info_list.append(pricing)
    # 折扣
    discount = browser.find_element(By.XPATH, '//*[@id="dd-zhe"]')
    discount = discount.text.replace("折)", "")
    discount = discount.replace("(", "")
    if discount == "":
        discount = "None"
    book_info_list.append(discount)
    # 大类型
    type_list = browser.find_elements(By.XPATH, '//*[@id="detail-category-path"]/span/a[2]')
    for i in type_list:
        book_info_list.append(i.text)
    # 子类型
    subtype = browser.find_element(By.XPATH, '//*[@id="detail-category-path"]/span/a[3]')
    book_info_list.append(subtype.text)
    # 开本
    book_size = browser.find_element(By.XPATH, '//*[@id="detail_describe"]/ul/li[1]')
    book_size = book_size.text.replace("开 本：", "")
    book_info_list.append(book_size)
    # 纸张
    paper = browser.find_element(By.XPATH, '//*[@id="detail_describe"]/ul/li[2]')
    paper = paper.text.replace("纸 张：", "")
    book_info_list.append(paper)
    # 包装
    packaging = browser.find_element(By.XPATH, '//*[@id="detail_describe"]/ul/li[3]')
    packaging = packaging.text.replace("包 装：", "")
    book_info_list.append(packaging)
    # 是否套装
    suit = browser.find_element(By.XPATH, '//*[@id="detail_describe"]/ul/li[4]')
    suit = suit.text.replace("是否套装：", "")
    book_info_list.append(suit)
    # 国际标准书号ISBN
    isbn = browser.find_element(By.XPATH, '//*[@id="detail_describe"]/ul/li[5]')
    isbn = isbn.text.replace("国际标准书号ISBN：", "")
    book_info_list.append(isbn)

    # 编辑推荐
    editor_recommend = browser.find_element(By.XPATH, '//*[@id="abstract"]/div[2]')
    book_info_list.append(editor_recommend.text)

    # 评论数量
    browser.get(url + "?point=comment_point")
    time.sleep(3)
    comment_num = browser.find_element(By.XPATH, '//*[@id="comment_num_tab"]/span[1]')
    comment_num = comment_num.text.replace("全部（", "")
    comment_num = comment_num.replace("）", "")
    print("评论数量：", comment_num)
    book_info_list.append(comment_num)
    # 评论标签
    comment_tag = browser.find_elements(By.XPATH, '//*[@id="comment_tags_div"]/div[2]/span')
    comment_tag_list = []
    for i in comment_tag:
        info = i.find_element(By.XPATH, 'a').text
        comment_tag_list.append(info)
    book_info_list.append(comment_tag_list)
    logger.info(year + "年" + url + "的图书信息解析完成...")


    # 写入到csv文件中
    logger.info("开始将" + year + "年的图书信息写入到文件中...")
    with open(filename, "a", encoding="utf-8", newline="") as f:
        print(book_info_list)
        writer = csv.writer(f)
        writer.writerow(book_info_list)
    logger.info(year + "年的图书信息写入到文件完成...")

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


# 关闭浏览器
# browser.close()
if __name__ == "__main__":
    time.sleep(3)
    analysis_book_info("http://product.dangdang.com/21055821.html", "bests_sellers_0_month_src.csv", "2023", "1")

    # for i in range(2020, 2024):
    #     get_num_src(str(i), "0")
