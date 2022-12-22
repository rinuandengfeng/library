import datetime

import requests
from lxml import etree
from config import global_config

from log import logger

from exception import SeatException

#图书馆预约脚本
class LibrarySeat(object):

    def __init__(self) -> None:
        self.session = requests.session()
        self._url = global_config.get('account', 'url')
        self._synchronizer_token = self.__get_login_index()
        self._proixes = {"http":None,"https":None}
        self.username = global_config.get('account', 'username')
        self.passwd = global_config.get('account', 'password')
        self.isLogin = False


    #登录
    def logins(self):
        self.__login()
        if self.isLogin:
            print("登录成功")
        else:
            raise SeatException("登录失败")

    
    #获取登录页面
    def __get_login_index(self)->str:
        headers = {
            "user-agent": "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        }
        url_index = self._url + '/login'

        params ={
            "targetUri":'/'
        }

        try:
            response = self.session.get(url_index,headers=headers,params=params,timeout=(5,3))
            tree = etree.HTML(response.txt)
            synchronizer_token = tree.xpath('//*[@id="SYNCHRONIZER_TOKEN"]/@value')[0]
            return synchronizer_token
        except Exception as e:
            logger.error(e)


    # 登录账号
    def __login(self):
        url = self._url + '/auth/signIn'
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "user-agent": "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
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


if __name__ == '__main__':
    test = LibrarySeat()
    test.logins()

    
