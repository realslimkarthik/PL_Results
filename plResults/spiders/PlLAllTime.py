from scrapy.spider import BaseSpider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from plResults.items import PlLinksItem
from pymongo import MongoClient
from datetime import datetime, time

seasonLinks = ['1992-1993', '1993-1994', '1994-1995', 
'1995-1996', '1996-1997', '1997-1998', '1998-1999', '1999-2000', 
'2000-2001', '2001-2002', '2002-2003', '2003-2004', '2004-2005', 
'2005-2006', '2006-2007', '2007-2008', '2008-2009', '2009-2010', 
'2010-2011', '2011-2012', '2012-2013', '2013-2014']

url = 'http://www.premierleague.com/en-gb/matchday/results.html?paramClubId=ALL&paramComp_8=true&paramSeason=%s&view=.dateSeason'

class PlLinkSpider(BaseSpider):
    name = 'PlLAllTime'
    allowed_domains = ['www.premierleague.com']
    start_urls = []
    # start_urls = [url % seasonLinks[0], url % seasonLinks[1], url % seasonLinks[2], url % seasonLinks[3],
    # url % seasonLinks[4], url % seasonLinks[5], url % seasonLinks[6], url % seasonLinks[6], 
    # url % seasonLinks[7], url % seasonLinks[8], url % seasonLinks[9], url % seasonLinks[10],
    # url % seasonLinks[11], url % seasonLinks[12], url % seasonLinks[13], url % seasonLinks[14],
    # url % seasonLinks[15], url % seasonLinks[16], url % seasonLinks[17], url % seasonLinks[18],
    # url % seasonLinks[19], url % seasonLinks[20], url % seasonLinks[21]]
    
    def __init__(self):
        for i in seasonLinks:
            self.start_urls.append(url % i)

    def parse(self, response):
        client = MongoClient()
        db = client.fourmanwall
        mLinks = db.matchLinks
        print response.url
        hxs = HtmlXPathSelector(response)
        fullUrl = 'http://www.premierleague.com'
        seas = hxs.xpath('//h2[contains(@class, "noborder")]/text()').extract()[0]
        seas = seas[8:]
        tabs = hxs.xpath('//table[contains(@class, "contentTable")]')
        j = 0
        count = 0
        for i in tabs:
            dateString = i.xpath('./tr/th/text()').extract()[0].strip()
            dateString = dateString[dateString.find(' '):].strip()
            date = datetime.strptime(dateString, "%d %B %Y")
            gameLinks = i.xpath('./tr/td[contains(@class, "clubs score")]/a/@href').extract()
            t1 = i.xpath('./tr/td[contains(@class, "clubs rHome")]/a/text()').extract()
            t2 = i.xpath('./tr/td[contains(@class, "clubs rAway")]/a/text()').extract()
            while len(gameLinks) > 0:
                try:
                    mLinks.insert({'_id': fullUrl + gameLinks.pop(), 'season': seas, 'teams': [t1.pop(), t2.pop()], 'date': date})
                except IndexError:
                    break
                count += 1
        print count
