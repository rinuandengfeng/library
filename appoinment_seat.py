import datetime
import json
import os

import requests
from lxml import etree
from config import global_config

from log import logger
from utils import get_seatId,seatId_to_json_file,get_timeId

from exception import SeatException




TODAY_DATE = datetime.date.today()
# 图书馆预约脚本
class LibrarySeat(object):

    def __init__(self) -> None:
        self.session = requests.session()
        self._url = global_config.get('account', 'url')
        self._synchronizer_token = self.__get_login_index()
        self._proxies = {"http": None, "https": None}
        self.username = global_config.get('account', 'username')
        self.passwd = global_config.get('account', 'password')
        self.isLogin = False
        self._seat_file_path = os.path.join(os.getcwd(),global_config.get('account','seat_file_path'))
        if not os.path.exists(self._seat_file_path):
            os.makedirs(self._seat_file_path)
        self.classroom = global_config.get('seat','classroom')
        self.seat_num = global_config.get('seat','seat_num')
        self.start_time = get_timeId(global_config.get('seat','start_time'))
        self.end_time = get_timeId(global_config.get('seat','end_time'))
        


    def start(self):
        self.logins()
        if self.isLogin:
            classroom_path = self._seat_file_path+self.classroom+".json"
            if not os.path.exists(classroom_path):
                self.requests_seat()
                content = self.__appoinment_seat()
                if content[1] == '预约失败! ':
                    logger.error(content[1])
                    logger.error(content[3])
                elif content[1] =='系统已经为您预定好了':
                    logger.info(content[1])
                    result = content[7]+content[8]+content[10]+content[11]+content[13]+content[14]
                    logger.info(result)
                else:
                    logger.error("系统错误，预约失败")
            else:
                content = self.__appoinment_seat()
                if content[1] == '预约失败! ':
                    logger.error[content[1]]
                    logger.error(content[3])
                elif content[1] =='系统已经为您预定好了':
                    logger.info(content[1])
                    result = content[7]+content[8]+content[10]+content[11]+content[13]+content[14]
                    logger.info(result)
                else:
                    logger.error("系统错误，预约失败")


    # 登录
    def logins(self):
        self.__login()
        if self.isLogin:
            print("登录成功。")
        else:
            raise SeatException("登录失败。")
    
    # 获取房间和座位
   
    def get_seatid_file(self):
        try:
            self.logins()
            self.requests_seat()
        except Exception as e:
            logger.error("登录失败，请重新登录。")



    # 获取登录页面
    def __get_login_index(self) -> str:
        headers = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "Connection": "Keep-alive",
        }
        url_index = self._url + '/login'

        params = {
            "targetUri": '/'
        }

        try:
            response = self.session.get(
                url_index, headers=headers, params=params, timeout=(5, 3))
            tree = etree.HTML(response.text)
            synchronizer_token = tree.xpath(
                '//*[@id="SYNCHRONIZER_TOKEN"]/@value')[0]
            return synchronizer_token
        except Exception as e:
            logger.error(e)

    # 登录账号
    def __login(self) -> None:
        url = self._url + '/auth/signIn'
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "Connection": "Keep-alive",
            "referer": "https://zuowei.hnuahe.edu.cn/login?targetUri=%2F",
        }
        data = {
            "SYNCHRONIZER_URI": "/login",
            "authid": "-1",
            "username": self.username,
            "password": self.passwd,
            "SYNCHRONIZER_TOKEN": self._synchronizer_token,
        }
        try:
            respones = self.session.post(
                url=url, data=data, headers=header, timeout=(5, 3))
            self.isLogin = True
            logger.info("登录成功！")
        except Exception as e:
            logger.error("登录失败:", e)

    # 获取预约座位页面
    def get_map(self):
        url = self._url + '/map'
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "referer": "https://zuowei.hnuahe.edu.cn/",
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "Connection": "Keep-alive",
        }
        respones = self.session.get(url=url, headers=header, timeout=(5, 3),proxies=self._proxies)

        # 获取选座位的SYNCHRONIZER_TOKEN
        tree = etree.HTML(respones.text)
        try:
            map_token = tree.xpath('//*[@id="SYNCHRONIZER_TOKEN"]/@value')[0]
            return map_token
        except Exception as e:
            logger.error("获取map页面中的SYNCHRONIZER_TOKEN失败"+str(e))    
        
    
    # 获取教室号、座位id、座位号，并存入对应的教室的json文件
    #其他学校带更新
    def requests_seat(self):
        
        url = self._url + '/mapBook/ajaxGetRooms'
        headers = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "Connection": "Keep-alive",
            "Referer": "https://zuowei.hnuahe.edu.cn/map"
        }

        # 将三个校区每层每个教室写成一个json文件
        for i in range(1, 4):
            if i == 3:
                for j in [0, 2, 3]:
                    data = {
                        "building": i,
                        "floor": j,
                        "onDate": str(TODAY_DATE)
                    }
                    response = self.session.get(
                        url=url, params=data, headers=headers, timeout=(5, 3), proxies=self._proxies)
                    content = json.loads(response.text)["rooms"]
                    if content:
                        for classroom in content:
                            # 获取座位id和座位号，并转化为json
                            seatId_to_json_file(self,classroom=classroom)
            else:
                for j in range(0, 6):
                    data = {
                        "building": i,
                        "floor": j,
                        "onDate": str(TODAY_DATE)
                    }
                    response = self.session.get(
                        url=url, params=data, headers=headers, timeout=(5, 3), proxies=self._proxies)
                    content = json.loads(response.text)["rooms"]
                    if content:
                        for classroom in content:
                            # 获取座位id和座位号，并转化为json
                            seatId_to_json_file(self,classroom=classroom)


    # #获取预约时间对应的时间id
    #响应对象中没有时间和相对应的时间ID
    # def get_appoinment_timeId(self):
    #     url = self._url+"/freeBook/ajaxGetTime"
    #     headers = {
    #         "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
    #         "Connection": "Keep-alive",
    #         "Referer": "https://zuowei.hnuahe.edu.cn/map",
    #         "x-requested-with":"XMLHttpRequest"
    #     }

    #     params = {
    #         "id":get_seatId(self.classroom,self.seatId),
    #         "date":str(TODAY_DATE)
    #     }

    #     responses = self.session.get(url=url,headers=headers,params=params,proxies=self._proxies)







    #预约座位
    def __appoinment_seat(self):
        tomorrow = TODAY_DATE+datetime.timedelta(days=1)
        url = self._url+'/selfRes'
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "referer": "https://zuowei.hnuahe.edu.cn/map",
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "Connection": "Keep-alive"
        }
        data ={
            "SYNCHRONIZER_TOKEN": self.get_map(),
            "SYNCHRONIZER_URI": "/map",
            "authid": "-1",
            "start": self.start_time,  
            "end": self.end_time,  
            "date": str(tomorrow),
            # "date":str(TODAY_DATE),
            "seat":get_seatId(self.classroom,self.seat_num)  
        }
        try:
            respones = self.session.post(url=url, headers=header, data=data, timeout=(5, 3),proxies=self._proxies)
            tree = etree.HTML(respones.text)
            content = tree.xpath('/html/body/div[3]/div[3]/div/div/dl//text()')
            return content
        except Exception as e:
            logger.error("预约失败"+str(e))

if __name__ == '__main__':
    test = LibrarySeat()
    # test.requests_seat()
    test.start()
    
    