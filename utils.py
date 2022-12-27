from log import logger
import json
import datetime
from config import global_config

from lxml import etree
#当天日期
TODAY_DATE = datetime.date.today()

# 分割座位号
def seatid_to_json(raw_seat_id, raw_seat_num):
    seat_dict = {}
    for i in range(0, len(raw_seat_id)):
        seat_id = raw_seat_id[i].split("_")[1]
        seat_dict[raw_seat_num[i]] = seat_id
    return seat_dict

# 获取座位id和座位号
def seatId_to_json_file(library,classroom):
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
        url=seat_url, headers=headers,params=seat_data, timeout=(5, 3), proxies=library._proxies)
    tree = etree.HTML(seat_response.text)
    seat_id = tree.xpath('//ul/li/@id')
    seat_num = tree.xpath('//ul//li/div/code/text()')
    seat_dict = seatid_to_json(seat_id, seat_num)
    classroom["seat_dict"] = seat_dict
    with open(library._seat_file_path + classroom["name"] + ".json", 'w', encoding="utf-8") as f:
        json.dump(classroom, f, indent=4,
                ensure_ascii=False)
    logger.info(classroom["name"]+"座位ID获取成功。")


#根据classroom和座位号获取座位id
def get_seatId(classroom,seat_num):

    with open('seat/'+str(classroom)+'.json','r',encoding='utf8') as f:
        all_seatId = json.loads(f.read())['seat_dict']
        seatId = all_seatId.get(seat_num)
        return seatId


#获取时间id
def get_timeId(time):
    with open('time.json','r',encoding='utf-8') as f:
        timeId = json.loads(f.read())[str(time)]
        return timeId







if __name__ == '__main__':
    timeId = get_timeId('08:00')
    