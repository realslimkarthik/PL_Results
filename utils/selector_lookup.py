
class SelectorLookup(object):

    def __init__(self):
        self._team_selector_template = './table[contains(@class, "teaminfo")]/tr/td[contains(@class, \
            "{team}")]/span/text()'
        self._scorer_selector_template = './div[contains(@class, "{team} goals")]/ul/li/text()'

    @property
    def data_section_selector(self):
        return '//div[contains(@class, "post_match")]'

    @property
    def score_selector(self):
        return './table[contains(@class, "teaminfo")]/tr/td[contains(@class, "countscore")]/div[contains(@id, \
            "fixtureScore")]/span/text()'

    @property
    def date_selector(self):
        return './p[contains(@class, "fixtureinfo")]/span/text()'

    @property
    def home_team_selector(self):
        return self._team_selector_template.format(team='home')

    @property
    def away_team_selector(self):
        return self._team_selector_template.format(team='away')

    @property
    def home_scorers_selector(self):
        return self._scorer_selector_template.format(team='home')

    @property
    def away_scorers_selector(self):
        return self._scorer_selector_template.format(team='away')

    @property
    def referee(self):
        return './p[contains(@class, "fixtureinfo")]/a/text()'

    @property
    def stadium_and_attendance_data_selector(self):
        return './p[contains(@class, "fixtureinfo")]/text()'

    @property
    def season_selector(self):
        return '//div[contains(@class, "breadcrumb")]/a/text()'
