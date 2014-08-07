from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from pymongo import MongoClient

class MatchSpider(BaseSpider):
    name = 'MSpider'
    allowed_domains = ['www.premierleague.com']
    start_urls = list()
    def __init__(self):
        client = MongoClient()
        db = client.plDB
        links = db.matchLinks
        # print self.start_urls
        for i in links.find({'teams': 'Arsenal'}):
            self.start_urls.append(i['_id'])
        print len(self.start_urls)
        

    def parse(self, response):
        client = MongoClient()
        db = client.fourmanwall
        hxs = HtmlXPathSelector(response)
        details = hxs.select('//div[contains(@class, "post_match")]')
        date = details.select('./p[contains(@class, "fixtureinfo")]/span/text()').extract()[0]
        t1 = details.select('./table[contains(@class, "teaminfo")]/tr/td[contains(@class, "home")]/span/text()').extract()[0]
        t2 = details.select('./table[contains(@class, "teaminfo")]/tr/td[contains(@class, "away")]/span/text()').extract()[0]
        # self.start_urls.pop(0)
        if t1 == 'Arsenal':
            HoA = 'H'
        elif t2 == 'Arsenal':
            HoA = 'A'
        else:
            return

        sc = details.select('./table[contains(@class, "teaminfo")]/tr/td[contains(@class, "countscore")]/div[contains(@id, "fixtureScore")]/span/text()').extract()
        score = sc[0] + ' - ' + sc[1]
        t1S = details.select('./div[contains(@class, "home goals")]/ul/li/text()').extract()
        t2S = details.select('./div[contains(@class, "away goals")]/ul/li/text()').extract()
        print date + ' ' + t1 + ' - ' + t2
        teamData = db.arsenal

        if HoA == 'H':
            teamData.insert({'opponent': t2, 'score': score, 'HorA': HoA, 'scorerF': t1S, 'scorerA':t2S, 'date': date})
        else:
            teamData.insert({'opponent': t1, 'score': score, 'HorA': HoA, 'scorerF': t2S, 'scorerA':t1S, 'date': date})