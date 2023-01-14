from appoinment_seat import LibrarySeat
from log import logger

seat = LibrarySeat()
def get_seat():  
    try:
        seat.logins()
        seat.get_seatid_file()
        logger.info("获取座位文件成功！")
    except Exception as e:
        logger.error("获取座位文件失败！")


if __name__ == "__main__":
    get_seat()