from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.http import Request
from scrapy.selector import Selector
from datetime import datetime
from pymongo import MongoClient
from utils.utils import get_seasons_list, results_url

class ResultsSpider(Spider):
    name = 'TSpider'
    allowed_domains = ['premierleague.com']
    start_urls = list()

    def __init__(self):
        seasons = get_seasons_list(1992)
        for season in seasons:
            self.start_urls.append(results_url.format(season=season))
        
    def parse(self, response):
        extractor = SgmlLinkExtractor(allow=('en-gb/matchday/matches/[0-9]{4}\-[0-9]{4}/epl.match-preview.html/[a-z\-]{0,20}\-vs\-[a-z\-]{0,20}', ))
        links = extractor.extract_links(response)
        for i in links:
            yield Request(i.url, callback=self.parse_items)
        print "url is " + response.url

    def parse_items(self, response):
        sel = Selector(response)
        details = sel.xpath('//div[contains(@class, "post_match")]')
        print response.url
        dateStr = details.xpath('./p[contains(@class, "fixtureinfo")]/span/text()').extract()[0]
        dateStr = dateStr[dateStr.find(' '):].strip()
        date = datetime.strptime(dateStr, "%d %B %Y")

        dText = details.xpath('./p[contains(@class, "fixtureinfo")]/text()').extract()
        stadium = dText[0].strip()[1:dText[0].strip()[1:].find('|')].strip()
        ref = details.xpath('./p[contains(@class, "fixtureinfo")]/a/text()').extract()[0].strip()
        attendance = dText[1].split(' ')[3]
        t1 = details.xpath('./table[contains(@class, "teaminfo")]/tr/td[contains(@class, "home")]/span/text()').extract()[0]
        t2 = details.xpath('./table[contains(@class, "teaminfo")]/tr/td[contains(@class, "away")]/span/text()').extract()[0]

        sc = details.xpath('./table[contains(@class, "teaminfo")]/tr/td[contains(@class, "countscore")]/div[contains(@id, "fixtureScore")]/span/text()').extract()
        score = sc[0] + ' - ' + sc[1]
        t1S = details.xpath('./div[contains(@class, "home goals")]/ul/li/text()').extract()
        t2S = details.xpath('./div[contains(@class, "away goals")]/ul/li/text()').extract()
        seas = sel.xpath('//div[contains(@class, "breadcrumb")]/a/text()').extract()[3]
        link = response.url
        client = MongoClient()
        db = client.fourmanwall
        details = db.matchData.insert({'teams': [t1, t2], 'score': score, 't1S': t1S, 't2S': t2S, 'season': seas, 
        'date': date, 'attendance': attendance, 'link': link, 'referee': ref, 'stadium': stadium})