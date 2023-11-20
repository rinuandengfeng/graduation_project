import requests

from lxml import etree
from fake_useragent import UserAgent
from log import logger


ua = UserAgent()

proxies = {
    "https": "https://1.15.47.213:443",
    "http": "http://27.192.173.108:9000",
    # "http": "182.34.18.189:9999"
}


# 获取2023 年所有月份的图书信息
def get_book_info_2023():
    for i in range(1, 11):
        book_info_list = []
        url = "http://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-month-2023-" + \
            str(i)+"-1-"
        for page in range(1, 26):
            url = url+str(page)
            get_book_info(url, page, book_info_list)
        
        filename = "book_info"+str(i)+"month.json"
        logger.info("开始写入"+str(i)+"月的图书信息到文件中...")

        with open(filename, "w", encoding="utf-8") as f:
            f.write(str(book_info_list))
        logger.info("写入"+str(i)+"月的图书信息到文件中结束")

    return


# 获取总排行榜的书的信息
def get_book_info(url, page, book_info_list):
    count = 1
    # url = "https://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-" + \
    #     str(page)
    response = requests.get(url=url, headers={"User-Agent": ua.random})
    if response.status_code != 200:
        logger.error(str(page)+"页获取图书信息失败...")
        
    tree = etree.HTML(response.text)
    book_div = tree.xpath("/html/body/div[2]/div[3]/div[2]/ul/li")
    logger.info("开始获取第"+str(page)+"页图书信息")
    for i in book_div:
        book_info = {}
        # if count <= 3 and page == 1:
        # num = i.xpath(
        #     './/div[@class="list_num"]/text()')[0].replace(".", "")
        num = i.xpath(
            './/div[@class="list_num"]/text()')
        book_info["top_num"] = num
        #     count += 1
        # else:
        #     num = i.xpath(
        #         './/div[@class="list_num "]/text()')[0].replace(".", "")
        #     book_info["top_num"] = num
        #     count += 1
        book_info["book_src"] = i.xpath(".//div[@class='pic']/a/@href")[0]
        book_info["book_name"] = i.xpath(
            './/div[@class="pic"]/a/img/@title')[0]
        author_and_press = i.xpath(
            './/div[@class="publisher_info"]/a/text()')
        book_info["book_author"] = author_and_press[0]
        book_info["book_press"] = author_and_press[-1]
        # 获取图书的类型  目前这个功能没有用，因获取类型时需要登录自己的账号，好像是获取的频率快了自己的账号也会自动下线
        # logger.info("开始获取排名第"+str(book_info["top_num"])+"属于的类型...")
        # get_book_type(book_info["book_src"], book_info)
        book_info_list.append(book_info)

    # 写入到json文件中
    # logger.info("开始写入图书信息到book_info1.json文件中...")
    # with open("book_info1.json", "w", encoding="utf-8") as f:
    #     f.write(str(book_info_list))
    # logger.info("写入图书信息到book_info1.json文件中结束")

    # errorLogger.error("获取图书信息结束失败...")
    return


# 获取图书的类型
def get_book_type(url, book_info):
    response = requests.get(url, headers={"User-Agent": ua.random})
    tree = etree.HTML(response.text)
    info = tree.xpath(
        "/html/body/section[7]/a[4]/div/span[2]/text()")
    if info != []:
        info = info[0].split(">")
        logger.info("获取第"+str(book_info["top_num"])+"的类型成功")
        book_info["book_type1"] = info[1]
        book_info["book_type2"] = info[2]
    else:
        logger.info("获取第"+str(book_info["top_num"])+"的类型失败")
        book_info["book_type1"] = ""
        book_info["book_type2"] = ""
    return


if __name__ == "__main__":
    get_book_info_2023()
