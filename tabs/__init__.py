from otree.api import *

doc = """
Tabs
"""


class C(BaseConstants):
    NAME_IN_URL = "tabs"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Tabs(Page):
    pass


page_sequence = [Tabs]
