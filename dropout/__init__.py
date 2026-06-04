from otree.api import *

doc = """
Dropout handler
"""


class C(BaseConstants):
    NAME_IN_URL = "dropout"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    pass


# PAGES
class MyPage(Page):
    @staticmethod
    def is_displayed(player):
        return player.participant.vars.get("dropout", False)


page_sequence = [MyPage]
