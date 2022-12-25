from log import logger
import json
import datetime


from lxml import etree
#当天日期
TODAY_DATE = datetime.date.today()

# 分割座位号
def seatid_to_json(raw_seat_id, raw_seat_num):
    seat_dict = {}
    for i in range(0, len(raw_seat_id)):
        seat_id = raw_seat_id[i].split("_")[1]
        seat_dict[seat_id] = raw_seat_num[i]
    return seat_dict

# 获取座位id和座位号
def get_seatId(library,classroom):
    headers = {
        "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
        "Connection": "Keep-alive",
        "Referer": "https://zuowei.hnuahe.edu.cn/map"
    }

    seat_data = {
        "room": classroom["id"],
        "date": str(TODAY_DATE)
    }
    seat_url = "https://zuowei.hnuahe.edu.cn" + "/mapBook/getSeatsByRoom"

    seat_response = library.session.get(
        url=seat_url, params=seat_data, timeout=(5, 3), proxies=library._proxies)
    tree = etree.HTML(seat_response.text)
    seat_id = tree.xpath('//ul/li/@id')
    seat_num = tree.xpath('//ul//li/div/code/text()')
    seat_dict = seatid_to_json(seat_id, seat_num)
    classroom["seat_dict"] = seat_dict
    with open(library._seat_file_path + classroom["name"] + ".json", 'w', encoding="utf-8") as f:
        json.dump(classroom, f, indent=4,
                ensure_ascii=False)
    logger.info(classroom["name"]+"座位ID获取成功。")
