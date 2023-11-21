from utils.get_book_info import get_book_info

# 获取图书畅销榜中的
book_info_list = []
count = 1
for page in range(1, 26):

    get_book_info(page, book_info_list)

# 写入到json文件中
with open("./data/book_info.json", "w", encoding="utf-8") as f:
    f.write(str(book_info_list))
