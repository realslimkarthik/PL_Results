from scrapy.spider import Spider
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from scrapy.http import Request
from scrapy.selector import Selector
from datetime import datetime, time
from pymongo import MongoClient

seasonLinks = ['1992-1993', '1993-1994', '1994-1995', 
'1995-1996', '1996-1997', '1997-1998', '1998-1999', '1999-2000', 
'2000-2001', '2001-2002', '2002-2003', '2003-2004', '2004-2005', 
'2005-2006', '2006-2007', '2007-2008', '2008-2009', '2009-2010', 
'2010-2011', '2011-2012', '2012-2013', '2013-2014']


url = 'http://www.premierleague.com/en-gb/matchday/results.html?paramClubId=ALL&paramComp_8=true&paramSeason=%s&view=.dateSeason'

class TheSpider(Spider):
    name = 'TSpider'
    allowed_domains = ['premierleague.com']
    start_urls = list()

    def __init__(self):
        for i in seasonLinks:
            self.start_urls.append(url % i)
        
    def parse(self, response):
        extractor = SgmlLinkExtractor(allow = ('en-gb/matchday/matches/[0-9]{4}\-[0-9]{4}/epl.match-preview.html/[a-z\-]{0,20}\-vs\-[a-z\-]{0,20}', ))
        links = extractor.extract_links(response)
        for i in links:
            yield Request(i.url, callback = self.parse_items)
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