import datetime
import json
import os

import requests
from lxml import etree
from config import global_config

from log import logger
from utils import seatid_to_json,get_seatId,seatId_to_json_file

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
        #图书馆教室名
        self.classroom = global_config.get('seat','classroom')
        #座位id
        self.seatId = global_config.get('seat','seat_num')

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
        url = self.url + '/map'
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "referer": "https://zuowei.hnuahe.edu.cn/",
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "Connection": "Keep-alive",
        }
        respones = self.session.get(url=url, headers=header, timeout=(5, 3),proxies=self._proxies)

        # 获取选座位的SYNCHRONIZER_TOKEN
        tree = etree.HTML(respones.text)
        map_token = tree.xpath('//*[@id="SYNCHRONIZER_TOKEN"]/@value')[0]
        return map_token
    
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


    #获取预约时间对应的时间id
    def get_appoinment_timeId(self):
        url = self._url+"/freeBook/ajaxGetTime"
        headers = {
            "user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
            "Connection": "Keep-alive",
            "Referer": "https://zuowei.hnuahe.edu.cn/map",
            "x-requested-with":"XMLHttpRequest"
        }

        params = {
            "id":get_seatId(self.classroom,self.seatId),
            "date":str(TODAY_DATE)
        }

        responses = self.session.get(url=url,headers=headers,params=params,proxies=self._proxies)

        with open('time.html','w',encoding='utf8') as f:
            f.write(responses.text)
        






    #预约座位
    def _appoinment_seat(self):
        url = self._url+'/selfRes'

    

if __name__ == '__main__':
    test = LibrarySeat()
    test.logins()
    test.requests_seat()
    test.get_appoinment_timeId()
