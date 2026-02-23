from otree.api import *

doc = """
oTree class slides
"""


class C(BaseConstants):
    NAME_IN_URL = "slides"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class Slides(Page):
    pass


page_sequence = [Slides]
