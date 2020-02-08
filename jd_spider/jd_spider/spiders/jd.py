# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from urllib.parse import urlencode
from scrapy_splash import SplashRequest
from ..items import JdSpiderItem

class JdSpider(scrapy.Spider):

    name = 'jd'
    allowed_domains = ['search.jd.com']
    start_urls = ['https://search.jd.com']

    def parse(self, response):
        m = input("请输入你要搜索的关键字：")
        key = urlencode({"keyword": m})
        wq = urlencode({"wq": m})
        url = "https://search.jd.com/Search?%s&enc=utf-8&%s" % (key, wq)
        # print(url)
        yield scrapy.Request(url, callback=self.parse_next, meta={"wq": wq, "key": key})
    def parse_next(self, response):
        wq = response.meta["wq"]
        key = response.meta["key"]
        # 总页数
        page_num = int(response.xpath('//div[@id="J_topPage"]/span/i/text()').extract_first())
        # print(page_num)
        lua_script = """
        function main(splash)
        splash:go(splash.args.url)
        splash:wait(1)
        splash:runjs('document.getElementsByClassName("page clearfix")[0].scrollIntoView(true)')
        splash:wait(2)
        return splash:html()
        end"""
        for i in range(1, page_num+1):
            if i == 1:
                url = 'https://search.jd.com/Search?%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&%s&page=1&s=1&click=0'% (key,wq)
            else:
                page = i*2-1
                s = (i-1)*60+1
                url = "https://search.jd.com/Search?%s&enc=utf-8&qrst=1&rt=1&stop=1&vt=2&%s&page=%s&s=%s&click=0" % (key, wq, str(page), str(s))
                # print(url)
            yield SplashRequest(url, endpoint="execute", args={"lua_source": lua_script}, cache_args=['lua_source'], callback=self.parse_second)
    def parse_second(self, response):
        le = LinkExtractor(restrict_xpaths='//div[@id="J_goodsList"]/ul/li/div/div[@class="p-img"]/a|//div[@id="J_goodsList"]/ul/li/div/div/div[2]/div[1]/div[1]/a')
        url_list = le.extract_links(response)
        print(len(url_list))
        headers = {"referer":response.url,
                   ":authority": "item.jd.com"}
        for link in url_list:
            url = link.url
            yield scrapy.Request(url,callback=self.parse_item,headers=headers,dont_filter=True)
    def parse_item(self, response):
        print("1")
