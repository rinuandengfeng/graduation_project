import os

basePath = os.path.abspath(os.path.dirname(__file__))
path = os.path.dirname(basePath + '\\logs\\')

filename = "./data/" + "2023" + "/" + "bests_sellers_0_month.csv"

HEADINFO = (
    "排名, 书名, 作者, 翻译者, 封面, 出版社时间, 出版社, 推荐率, 现价, 定价,折扣, 大类型, 子类型, 开本, 纸张, 包装, 是否套装,ISBN , 编辑推荐")


csv_name = "bests_sellers_0_month_src.csv"
csv_name = csv_name.replace("_src", "")
print(csv_name)


def get_files_in_directory(directory_path):
    return os.listdir(directory_path)


