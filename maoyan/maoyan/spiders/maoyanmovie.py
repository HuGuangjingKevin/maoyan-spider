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
        start_urls = ['https://maoyan.com/films?showType=3&yearId=13&offset={}'.format(i * 30) for i in range(117)]
        for url in start_urls:
            logging.info("开始请求主页地址:{}".format(url))
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # 获取主页下面所有的电影详情链接
        detailHrefList = response.xpath('//div[@class="movie-item"]/a/@href').extract()
        logging.info("主页:{}下面有{}个电影".format(response.url, len(detailHrefList)))
        for href in detailHrefList:
            # 电影详情页的url
            detailUrl = host + href
            logging.info("开始请求主页下面的电影详情页:{}".format(detailUrl))
            yield scrapy.Request(url=detailUrl, callback=self.parseMovieDetail)

    def parseMovieDetail(self, response):
        item = {}
        # 评分  票房节点
        movieStatsNode = response.xpath('//div[@class="movie-stats-container"]')[0]
        # 判断这部电影是否有评分信息
        movieIdexText = movieStatsNode.xpath("./div[1]/p/text()").extract_first()
        if movieIdexText != "用户评分":
            logging.error("{}不存在评分信息，存在的是:{}".format(response.url, movieIdexText))
            return
        # 通过正则匹配到电影详情页的.woff地址，请求并保存本地，使用python的FontTools库进行字体文件的处理，得到font对象
        font = downLoadWoff(response)
        # 正则提取的字体列表
        fontTextList = re.findall(r'<span class="stonefont">(.*?)</span>', response.text)
        if len(fontTextList) == 3:  # 三个信息都有
            item["score"] = getFontNumber(font, fontTextList[0])
            item["num"] = getFontNumber(font, fontTextList[1])
            item["booking"] = getFontNumber(font, fontTextList[2]) + response.xpath(
                '//span[@class="unit"]/text()').extract_first()
            item["name"] = response.xpath('//h3[@class="name"]/text()').extract_first()
            item["nameEllipsis"] = response.xpath('//div[@class="ename ellipsis"]/text()').extract_first()
            item["type"] = response.xpath('//div[@class="movie-brief-container"]/ul/li[1]/text()').extract_first()
            countryDuration = response.xpath('//div[@class="movie-brief-container"]/ul/li[2]/text()').extract_first()
            if "/" in countryDuration:
                item["country"] = countryDuration.split("/")[0].strip()
                item["duration"] = countryDuration.split("/")[1].strip()
            else:
                item["country"] = countryDuration.strip()
                item["duration"] = ""
            item["releaseTime"] = response.xpath(
                '//div[@class="movie-brief-container"]/ul/li[3]/text()').extract_first()
            item["_id"] = re.search(r"\d+", response.url).group()
            item["url"] = response.url
            yield item
        else:
            return


def downLoadWoff(response):
    # 正则提取woff文件
    woff = regexWoff.search(response.text).group(1)
    # 前面增加http:，得到woff链接地址
    woffLink = "http:" + woff
    # 请求woff链接后将文件保存到font目录下面
    woffFileName = "font\\" + os.path.basename(woff)
    if not os.path.exists(woffFileName):
        with open(woffFileName, "wb") as file:
            file.write(requests.get(url=woffLink).content)

    # 使用python的FontTools库进行字体文件的处理
    font = TTFont(woffFileName)
    os.remove(woffFileName)
    return font


def getFontNumber(font, text):
    """
    :param font: 使用python的FontTools库进行字体文件的处理后的font
    :param text: 现在在html中的字体文本
    :return: 将字体文本用数字字符串代理后的结果返回
    """
    # 从字体中提取出来的部分长度4的字符串列表  数字和字符串
    textExtractList = regexFont.findall(text)
    for textExtract in textExtractList:
        numStr = getNum(font, "uni{}".format(textExtract.upper()))
        text = text.replace("&#x{};".format(textExtract), numStr)
    return text


def getNum(font, fonName):
    """
    :param font:  FontTools将.woff文件转换成的font
    :param fonName: 电影详情页的字体名字，以uni开头
    :return:
    """
    uniFont = font["glyf"][fonName]
    for key, value in woffDict.items():
        if uniFont == baseFont["glyf"][key]:
            return value
