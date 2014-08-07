from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from plResults.items import PlLinksItem
from pymongo import MongoClient
import datetime

url = 'http://www.premierleague.com/en-gb/matchday/results.html?paramComp_100=true&view=.dateSeason'

class PlLinkSpider(BaseSpider):
    name = 'PlL'
    allowed_domains = ['www.premierleague.com']
    start_urls = [url]
    
    def parse(self, response):
        client = MongoClient()
        db = client.fourmanwall
        mLinks = db.matchLinks

        fullUrl = 'http://www.premierleague.com'
        hxs = HtmlXPathSelector(response)
        tabs = hxs.xpath('//table[contains(@class, "contentTable")]')
        for i in tabs:
            dateString = i.xpath('./tr/th/text()').extract()[0].strip()
            dateString = dateString[dateString.find(' '):].strip()
            date = datetime.strptime(dateString + " " + time, "%d %B %Y %H:%M")
            matches = mLinks.find({'date': {'$gt': d}})
            # if matches = None:


        gameLinks = hxs.xpath('//table[contains(@class, "contentTable")]/tr/td[contains(@class, "clubs score")]/a/@href').extract()
        t1 = hxs.xpath('//table[contains(@class, "contentTable")]/tr/td[contains(@class, "clubs rHome")]/a/text()').extract()
        t2 = hxs.xpath('//table[contains(@class, "contentTable")]/tr/td[contains(@class, "clubs rAway")]/a/text()').extract()
        print len(gameLinks)
        for i in range(0, 462):
            try:
                mLinks.insert({'_id': fullUrl + gameLinks[i], 'season': seas[8:], 'teams': [t1[i], t2[i]]})
            except IndexError:
                break