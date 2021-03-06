from datetime import date, timedelta

from factory import DjangoModelFactory, fuzzy, Iterator, SubFactory, LazyAttribute

from core.models import Player, Match, Season, SeasonPlayer


class PlayerFactory(DjangoModelFactory):
    class Meta:
        model = Player

    slack_id = fuzzy.FuzzyText(length=20)


class MatchFactory(DjangoModelFactory):
    class Meta:
        model = Match

    winner = SubFactory(PlayerFactory)
    loser = SubFactory(PlayerFactory)
    channel = '1234567890'


class SeasonFactory(DjangoModelFactory):
    class Meta:
        model = Season

    name = fuzzy.FuzzyText(length=10)
    start_date = fuzzy.FuzzyDate(date(2016, 1, 1))
    end_date = LazyAttribute(lambda o: o.start_date + timedelta(days=10))
    active = False


class SeasonPlayerFactory(DjangoModelFactory):
    class Meta:
        model = SeasonPlayer

    elo_score = fuzzy.FuzzyInteger(1000, 15000)
    win_count = fuzzy.FuzzyInteger(0, 20)
    loss_count = fuzzy.FuzzyInteger(0, 20)