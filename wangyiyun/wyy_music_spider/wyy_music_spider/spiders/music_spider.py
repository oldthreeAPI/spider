"""
爬取网易云音乐所有榜单的所有歌曲信息。歌曲明，作者，普通评价，热评，歌词等。
"""

import scrapy
import time
import re
import cloudmusic


class MusicSpiderSpider(scrapy.Spider):
    name = 'music_spider'
    allowed_domains = ['music.163.com']
    start_urls = ['https://music.163.com/discover/toplist']

    def start_requests(self):
        headers = {
            "cookie": "_ntes_nnid=7311bc7ad6943f24af2ce44205e50d17,1591343527861; _ntes_nuid=7311bc7ad6943f24af2ce44205e50d17; mail_psc_fingerprint=73a1c7aa23de749d573dbc22b82496dd; nts_mail_user=13025592642@163.com:-1:1; NMTID=00OfrDvd4MGsJoHME6quZ7SnIho0QEAAAF1Xvp3qw; WM_TID=9IDa2WGcQQlFQFURAQdrPG10dXAiYcPr; P_INFO=m13025592642@163.com|1610640709|0|mail163|00&99|gud&1610555581&mail163#gud&440100#10#0#0|130642&1|mail163|13025592642@163.com; _iuqxldmzr_=32; WM_NI=VOV7%2FSYt%2Fw27lPc%2FReuKKE0KVIzLr6CQ%2BGqL2AAxpi43PzNfE%2BfmrJliREgOBkfVQxwArDpUTGMf9D9S8KSY6Xy6XLj1mCSQ0VPW0VT6rHpw5chk3nuppchQ8mfxyXToWUE%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee92c56e86ac98b6b169b08a8ba2c54b928f9baeb548e9b9e1bbe142fcb4f88ec82af0fea7c3b92a96919ad8ae599bace198b13db090add0d16fb79585a6b3419697b6adf13e818fe5a8f448f29f8f99f363f8eda09bcd6e87f5aa8ef142b0b79ea6e64582b5aab7d474b59fbea5f35f98998387bc50fb8df8acd253f688b7d7db48aaefa3a4d25bf48aa0b8b35e98eabea9f37df7bda88cb266b7b0c084eb5bfcb3aa99fc5498b199b6c837e2a3; JSESSIONID-WYYY=vm0D7CXxxBk3x05UAGNXQVl7Bh6Tv7XzwrMONnZ%2FxsM9AVJqdmVF36s0UyannWXrFUpds2JxWq2O1K1pezqRl%2B1xrux%2BjpIW8XWlqNutfgJh5at%5C5Y1ih9H3X293G8MCvyzoyZPu44%5CNyygnHpGwH4eWT%2FiPtT4SjUDIhxUEsofv91k3%3A1614500363017; WEVNSM=1.0.0; WNMCID=rxddgf.1614499165077.01.0"
        }
        yield scrapy.Request(
            self.start_urls[0],
            headers=headers
        )

    def parse(self, response):
        # 获取榜单id
        music_list = response.xpath('//ul[@class="f-cb"]/li')
        print(music_list)
        for li in music_list:
            url = li.xpath('.//div[@class="left"]/a/@href').extract_first()
            next_url = "https://music.163.com" + url
            print(next_url)
            # 跳转详情页
            yield scrapy.Request(
                next_url,
                callback=self.details_page,
            )

    def details_page(self, response):
        # 获取歌曲信息
        li_list = response.xpath('//ul[@class="f-hide"]/li')
        for li in li_list:
            item = {}
            item["title"] = li.xpath('./a/text()').extract_first()
            url = li.xpath('./a/@href').extract_first()
            id = re.search(r".*id=(\d+)", url).group(1)
            # 第三方cloudmusic模块创建的对象(网易云音乐通过javascript语言自定义函数，生成两个关键值params，encseckey才可以获取评论歌词等信息。)
            music = cloudmusic.getMusic(id)
            item["artist"] = music.artist
            item["comment"] = music.getHotComments()
            item["Lyrics"] = music.getLyrics()
            print(item)
