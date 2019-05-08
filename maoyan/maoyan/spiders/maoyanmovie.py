# -*- coding: utf-8 -*-
import logging
import os
import re

import requests
import scrapy
from fontTools.ttLib import TTFont

# 猫眼电影的官网主页地址
host = "https://maoyan.com"
# 字体映射字典
woffDict = {'uniEBF6': '0', 'uniF620': '8', 'uniEEFD': '9', 'uniE767': '2', 'uniE4C8': '6',
            'uniE18D': '3', 'uniE58F': '1', 'uniE655': '4', 'uniF50A': '5', 'uniF441': '7'}
# 从字体中正则出需要替换数字的文本
regexFont = re.compile(r"&#x(.{4});")
# 从电影详情页面正则出woff文件
regexWoff = re.compile(r"url\(\'(.*?\.woff)\'\)")

baseFont = TTFont("base.woff")


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
        font = downLoadWoff(response)
        # 评分  票房节点
        movieStatsNode = response.xpath('//div[@class="movie-stats-container"]')[0]
        # 处理电影的用户评分，评分人数，累计票房 都是字体加密后的数据，后面需要进行解密
        score = movieStatsNode.xpath("./div[1]/div/span/span/text()").extract_first()
        num = movieStatsNode.xpath("./div[1]/div/div/span/span/text()").extract_first()
        booking = "".join(movieStatsNode.xpath("./div[2]/div//span/text()").extract())
        a = re.findall(r'<span class="stonefont">(.*?)</span>', response.text)
        for i in a:
            x = getFontNumber(font, i)
            print(x)


def downLoadWoff(response):
    # 正则提取woff文件
    woff = regexWoff.search(response.text).group(1)
    # woff的地址
    woffLink = "http:" + woff
    # 需要将woff文件请求并存入到本地目录中
    woffFileName = "font\\" + os.path.basename(woff)
    if not os.path.exists(woffFileName):
        with open(woffFileName, "wb") as file:
            file.write(requests.get(url=woffLink).content)

    # 使用python的FontTools库进行字体文件的处理
    font = TTFont(woffFileName)
    return font


def getFontNumber(font, text):
    # 从字体中提取出来的部分长度4的字符串列表
    textExtractList = regexFont.findall(text)
    for textExtract in textExtractList:
        text = text.replace("&#x{};".format(textExtract), getNum(font, "uni{}".format(textExtract.upper())))
    return text


def getNum(font, fonName):
    uniFont = font["glyf"][fonName]
    for key, value in woffDict.items():
        if uniFont == baseFont["glyf"][key]:
            return value