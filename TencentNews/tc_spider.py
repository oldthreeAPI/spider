"""
爬取腾讯新闻首页所有的新闻信息（标题，概要，url地址，出版社等）
翻页规律一样
"""

import requests
import json


class tencen_spider():
    def __init__(self, page_num):
        self.page_num = page_num

    def structrue_url(self, url):
        """
        # 构造url，每新增20条新信息
        :param url: 需要爬取网页的url地址
        :return: url
        """
        url_date = url.format(self.page_num)
        self.page_num += 20
        return url_date

    def parse_url(self, url_date, params, headers):
        """
        发送请求
        :param url_date: url地址
        :param params: 携带的请求参数
        :param headers: 请求头信息
        :return: 整理后的网页信息（原始信息是json数据）
        """
        response = requests.get(url_date, params=params, headers=headers)
        json_date = json.loads(response.text)
        date = json_date["data"]["list"]
        for ret_date in date:
            item = {}
            item["titlle"] = ret_date["title"]
            item["url"] = ret_date["url"]
            item["media_name"] = ret_date["media_name"]
            print(item)

    def save(self):
        # 预留保存数据的方法
        pass

    def run(self):
        # 请求参数
        url = 'https://i.news.qq.com/trpc.qqnews_web.kv_srv.kv_srv_http_proxy/list?limit={}'
        params = {
            "sub_srv_id": "24hours",
            "srv_id": "pc",
            "offset": "0",
            "strategy": "1",
            "ext": '{"pool": ["top"], "is_filter": 7, "check_type": true}'
        }
        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36"
        }

        while True:
            url_date = self.structrue_url(url)
            try:
                self.parse_url(url_date, params, headers)
            except Exception as e:
                print("数据全部爬取完成")
                break

if __name__ == "__main__":
    tencen = tencen_spider(20)
    tencen.run()