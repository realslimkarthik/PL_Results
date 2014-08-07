from scrapy.spider import Spider
from scrapy.http import FormRequest
from scrapy.http import Request
from scrapy.selector import HtmlXPathSelector
from plResults.items import PlLinksItem
from pymongo import MongoClient
from datetime import time, datetime
import pytz

url = 'http://www.premierleague.com/en-gb/matchday/matches.html?paramClubId=ALL&paramComp_100=true&view=.dateSeason'

class FixtureSpider(Spider):
    name = 'FSpider'
    allowed_domains = ['www.premierleague.com']
    start_urls = [url]
    
    def parse(self, response):
        client = MongoClient()
        db = client.fourmanwall
        hxs = HtmlXPathSelector(response)
        tabs = hxs.select('//table[contains(@class, "contentTable")]')
        fixts = db.fixtures
        uk = pytz.timezone('Europe/London')
        for i in tabs:
            dateString = i.xpath('./tr/th/text()').extract()[0].strip()
            datestr = dateString[dateString.find(' '):].strip()
            tRows = i.xpath('./tr')
            for j in tRows:
                try:
                    teams = j.xpath('./td[contains(@class, "clubs")]/a/text()').extract()[0]
                except IndexError:
                    continue
                v = teams.find(' v ')
                t1 = teams[0:v].strip()
                t2 = teams[v + 3:].strip()
                loc = j.xpath('./td[contains(@class, "location")]/a/text()').extract()[0].strip()
                time = j.xpath("./td[contains(@class, 'time')]/text()").extract()[0].strip()
                date = datetime.strptime(datestr + " " + time, "%d %B %Y %H:%M")
                uk_dt = uk.localize(date, is_dst=None)
                utc_date = uk_dt.astimezone(pytz.utc)
                print utc_date
                print date
                fixts.insert({'date': utc_date, 'teams': [t1, t2], 'location': loc})
                # fixts.insert({'date': dStr[0] + " " + dStr[1][0:3] + " " + dStr[2][2:], 'teams': [t1, t2], 'location': loc})
                print [t1, t2]