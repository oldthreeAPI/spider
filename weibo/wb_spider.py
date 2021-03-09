"""
输入微博搜索关键字，爬取页面的所以内容，翻页的所有内容。
"""

import requests
from lxml import etree
import json


class WeiBo(object):
    """
    直接复制粘贴浏览器的cookie信息就可以爬取到所有翻页的数据
    微博网页展示只有前50页的数据
    """
    def __init__(self):
        pass

    def structure_url(self, work_key):
        """
        构造请求url方法
        :param work_key: 搜索关键词
        :return: 请求的url列表
        """
        url_list = ['https://s.weibo.com/weibo/{}?topnav=1&wvr=6&b=1&page={}'.format(word_key, i) for i in range(1,5)]
        return url_list

    def parse_url(self, url_list, headers):
        """
        发送请求方法
        :param url_list: url请求列表
        :param headers: 请求头信息
        :return: 需要爬取的内容
        """
        for url in url_list:
            item = {}
            print(url)
            response = requests.get(url, headers=headers)
            html = etree.HTML(response.text)
            div_list = html.xpath('//div[@class="m-con-l"]//div[@class="card-wrap"]//div[@class="card"]')
            for div in div_list:
                item["id"] = div.xpath('./div[@class="card-feed"]/div[2]//a[@class="name"]/text()')[0] if len(div.xpath('.//div[@class="card-feed"]/div[2]//a[@class="name"]/text()')) > 0 else None
                item["text"] = "".join(div.xpath('./div[@class="card-feed"]/div[2]//p[@class="txt"]/text()')).replace("\n", "").replace("\u200b", "").strip() if len(div.xpath('//div[@class="card-feed"]/div[2]//p[@class="txt"]/text()')) > 0 else None
                item["forward"] = div.xpath('./div[@class="card-act"]/ul/li[2]/a/text()')[0].replace("转发 ", "")
                item["comment"] = div.xpath('./div[@class="card-act"]/ul/li[3]/a/text()')[0].replace("评论 ", "")
                item["fabulous"] = div.xpath('./div[@class="card-act"]/ul/li[4]//em/text()') if len(div.xpath('./div[@class="card-act"]/ul/li[4]//em/text()')) == 0 else 0
                print(item)
                with open("weibo.html", "w", encoding="utf-8", )as f:
                    f.write(json.dumps(item, ensure_ascii=False, indent=2))

    def save_date(self):
        """
        保存爬取内容的方法
        :return:
        """
        pass

    def run(self, word_key):
        # 请求需要携带的请求头信息
        headers = {
            "Cookie": "SINAGLOBAL=8674935871052.438.1591373424549; SCF=AjQ7MDUi9W7jp3kNf9YgdoGamS1L7a1EmGwr06pIcqlnvSq6X1CuDB3AW8ZDb99g_cgGdA-jtvYPZN_BJt8upV4.; login_sid_t=e3096d43b32afa7e90c14618b6fbd96b; cross_origin_proto=SSL; _s_tentry=www.baidu.com; Apache=981632592097.5966.1613897975321; ULV=1613897975327:11:9:2:981632592097.5966.1613897975321:1613877842021; UOR=,,www.baidu.com; SUB=_2A25NNltVDeRhGeRI7VAW8C7KzTuIHXVuQsudrDV8PUNbmtAKLWXmkW9NUop3bl4CGlmFjuhzJXgdeDVVDR-Cr7zO; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WF74ei-WrobB4Izwy7HOJwQ5JpX5KzhUgL.FozcSozNeh5cSoM2dJLoIpjLxKqL12zLB.eLxKqLB-eLBK2LxK-L1hnL1h5t; ALF=1645436549; SSOLoginState=1613900549; wvr=6; webim_unReadCount=%7B%22time%22%3A1613900995981%2C%22dm_pub_total%22%3A7%2C%22chat_group_client%22%3A0%2C%22chat_group_notice%22%3A0%2C%22allcountNum%22%3A33%2C%22msgbox%22%3A0%7D; WBStorage=8daec78e6a891122|undefined",
            "Upgrade-Insecure-Requests": "1",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.182 Safari/537.36",
            "Host": "s.weibo.com",
            "Sec-Fetch-User": "?1",
            "Sec-Fetch-Dest": "document",
            "Sec-Fetch-Mode": "navigate",
            "Sec-Fetch-Site": "none",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Connection": "keep-alive"
            }

        url_list = self.structure_url(word_key)
        self.parse_url(url_list, headers)


if __name__ == "__main__":
    word_key = "科比"
    weibo_spider = WeiBo()
    weibo_spider.run(word_key)


