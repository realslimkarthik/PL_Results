from scrapy.item import Item, Field
from utils.utils import cleaning_methods_map


class PLResultData(Item):
    link = Field()
    season = Field()
    home_team = Field()
    away_team = Field()
    score = Field()
    home_scorers = Field()
    away_scorers = Field()
    date = Field()
    attendance = Field()
    referee = Field()
    stadium = Field()

    def __setitem__(self, key, value):
        cleaning_method = cleaning_methods_map.get(key)
        clean_value = cleaning_method(value) if cleaning_method else value
        dict.__setitem__(self, key, clean_value)