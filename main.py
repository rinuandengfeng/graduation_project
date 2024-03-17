from get_data import get_files_in_directory, read_csv,analysis_book_info
from utils.log import logger


def start(file_path):
    filenames = get_files_in_directory(file_path)
    print(filenames)
    for filename in filenames:
        if filename.endswith("_src.csv"):
            logger.info("开始获取" + filename + "的图书信息数据...")
            print(file_path + "/" + filename)
            read_csv(file_path + "/" + filename)
            logger.info("开始获取" + filename + "的图书信息数据...")


if __name__ == "__main__":
    start("./data/2023/new_book")
