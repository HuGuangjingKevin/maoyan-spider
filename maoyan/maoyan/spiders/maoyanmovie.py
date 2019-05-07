# -*- coding: utf-8 -*-
import scrapy
import logging

# 猫眼电影的官网主页地址
host = "https://maoyan.com"


class MaoyanmovieSpider(scrapy.Spider):
    name = 'maoyanmovie'
    allowed_domains = ['maoyan.com']

    def start_requests(self):
        start_urls = ['https://maoyan.com/films?showType=3']
        for url in start_urls:
            logging.info("开始请求主页地址:{}".format(url))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 获取主页下面所有的电影详情链接
        detailHrefList = response.xpath('//dd//a/@href').extract()
        logging.info("主页:{}下面有{}个电影".format(response.url, len(detailHrefList)))
        for href in detailHrefList:
            # 电影详情页的url
            detailUrl = host + href
            logging.info("开始请求主页:{}下面的电影详情页:{}".format(response.url, detailUrl))
            yield scrapy.Request(url=detailUrl, callback=self.parseMovieDetail)

    def parseMovieDetail(self, response):
        # 评分  票房节点
        movieStatsNode = response.xpath('//div[@class="movie-stats-container"]')[0]
        # 处理电影的用户评分，评分人数，累计票房 都是字体加密后的数据，后面需要进行解密
        score = movieStatsNode.xpath("./div[1]/div/span/span/text()").extract_first()
        num = movieStatsNode.xpath("./div[1]/div/div/span/span/text()").extract_first()
        booking = "".join(movieStatsNode.xpath("./div[2]/div//span/text()").extract())
        print(score, num, booking)
