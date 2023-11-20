import requests
# from bs4 import BeautifulSoup
from lxml import etree
from fake_useragent import UserAgent
# 最近24小时
# url = "https://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-24hours-0-0-1-1"

ua = UserAgent()
# headers = {
#     # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
#     "User-Agent": "Mozilla/5.0 (Linux; Android 4.0.4; Galaxy Nexus Build/IMM76B) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.133 Mobile Safari/535.19"

# }

proxies = {
    "https": "https://1.15.47.213:443",
    "http": "http://27.192.173.108:9000",
    # "http": "182.34.18.189:9999"
}
book_info_list = []


# 获取总排行榜的书的信息
def get_book_info(page, book_info_list):
    count = 1
    url = "https://bang.dangdang.com/books/bestsellers/01.00.00.00.00.00-recent7-0-0-1-" + \
        str(page)
    response = requests.get(url=url, headers={"User-Agent": ua.random})
    tree = etree.HTML(response.text)
    book_div = tree.xpath("/html/body/div[2]/div[3]/div[2]/ul/li")

    print("开始爬取....")
    for i in book_div:
        book_info = {}
        if count <= 3 and page == 1:
            num = i.xpath(
                './/div[@class="list_num red"]/text()')[0].replace(".", "")
            book_info["top_num"] = num
            count += 1
        else:
            num = i.xpath(
                './/div[@class="list_num "]/text()')[0].replace(".", "")
            book_info["top_num"] = num
            count += 1
        book_info["book_src"] = i.xpath(".//div[@class='pic']/a/@href")[0]
        book_info["book_name"] = i.xpath(
            './/div[@class="pic"]/a/img/@title')[0]
        author_and_press = i.xpath(
            './/div[@class="publisher_info"]/a/text()')
        book_info["book_author"] = author_and_press[0]
        book_info["book_press"] = author_and_press[-1]
        # 获取图书的类型
        print("开始获取图书类型....")
        get_book_type(book_info["book_src"], book_info)
        book_info_list.append(book_info)

    # # 写入到json文件中
    # with open("book_info1.json", "w", encoding="utf-8") as f:
    #     f.write(str(book_info_list))

    return


# 获取图书的类型
def get_book_type(url, book_info):
    response = requests.get(url, headers={"User-Agent": ua.random})
    tree = etree.HTML(response.text)
    info = tree.xpath(
        "/html/body/section[7]/a[4]/div/span[2]/text()")
    if info != []:
        info = info[0].split(">")
        print(info)
        book_info["book_type1"] = info[1]
        book_info["book_type2"] = info[2]
    else:
        book_info["book_type1"] = ""
        book_info["book_type2"] = ""
    return


if __name__ == "__main__":
    get_book_info()
