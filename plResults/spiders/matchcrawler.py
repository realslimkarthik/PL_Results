from    scrapy.spiders import CrawlSpider
from    scrapy.selector import Selector
from    plResults.items import PLResultData
from    utils.selector_lookup import SelectorLookup
from    utils.utils import extractor, get_seasons_url_list


class MatchCrawler(CrawlSpider, SelectorLookup):
    name = 'MatchCrawler'
    allowed_domains = ['premierleague.com']
    start_urls = get_seasons_url_list(1992)

    def parse_item(self, response):
        self.logger.info('Processing ' + response.url)
        result_data = PLResultData()
        full_section = Selector(response)
        data_section = full_section.xpath(self.data_section_selector)
        result_data['date'] = data_section.xpath(self.date_selector).extract()[0]
        result_data['stadium'] = extractor(data_section, self.stadium_and_attendance_data_selector, index=0)
        result_data['attendance'] = extractor(data_section, self.stadium_and_attendance_data_selector, index=0)
        result_data['score'] = extractor(data_section, self.score_selector)
        result_data['home_team'] = extractor(data_section, self.home_team_selector, index=0)
        result_data['away_team'] = extractor(data_section, self.away_team_selector, index=0)
        result_data['home_scorers'] = extractor(data_section, self.home_scorers_selector)
        result_data['away_scorers'] = extractor(data_section, self.away_scorers_selector)
        result_data['season'] = extractor(full_section, self.score_selector)
        result_data['link'] = response.url
        return result_data




