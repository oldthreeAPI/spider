"""
直接调用anti_ip对象的run（）方法
:return: proxies值，类型为字典。可以直接给requests代理IP作为参数使用
"""
import requests
from 反爬辅助 import ip_setting
import datetime
import random


class anti_ip(object):
    def __init__(self, ip, ip_class):
        self.ip = ip
        self.ip_class = ip_class

    def handle_str(self):
        """
        处理传入的ip字符串
        :return: ip字符串列表
        """
        return self.ip.split(";")

    def testing(self):
        """
        检查代理ip的可用性：
        1.服务器返回的状态值是否是200
        2.连接服务器的时间是否 <200 两个条件是否同时成立
        :return: 可用的ip列表
        """
        ip_list = list()
        ips = self.handle_str()
        for ip in ips:
            proxies = {self.ip_class: self.ip_class+"://"+ip}
            # 获取代理IP请求网站的时间
            start_time = datetime.datetime.now()
            response = requests.get(ip_setting.url, proxies=proxies)
            end_time = datetime.datetime.now()
            code = response.status_code
            result_time = end_time - start_time
            if code == "200" or result_time.seconds <= 1:
                ip_list.append(ip)
        return ip_list

    def extract_ip(self, ip_list):
        """
        随机抽取io
        :param ip_list: 可用的ip池
        :return: 从可用的ip池随机抽取一个
        """
        total_ip = len(ip_list)
        if total_ip == 0:
            return "所有代理ip都不符合筛选要求"
        num = random.randint(0, total_ip-1)
        result_ip = ip_list[num]
        return {self.ip_class: self.ip_class+"://"+result_ip}

    def run(self):
        """
        主要逻辑函式
        :return:
        """
        # 验证ip的可用性
        # 组成IP池，随机抽取IP地址
        ip_list = self.testing()
        proxies = self.extract_ip(ip_list)
        return proxies


if __name__ == "__main__":
    IP = anti_ip(ip_setting.ip, ip_setting.ip_class)
    IP.run()