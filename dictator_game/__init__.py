from otree.api import *

doc = """
Simple dictator game
"""


class C(BaseConstants):
    NAME_IN_URL = "dictator_game"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(50)

    ROLE_DICTATOR = "dictator"
    ROLE_RECIPIENT = "recipient"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    amount_sent = models.CurrencyField(
        label="Decide how much to send to the recipient.",
        min=cu(0),
        max=C.ENDOWMENT,
    )


class Player(BasePlayer):
    pass


# PAGES
class Dictate(Page):
    form_model = "group"  # NOT "player"!
    form_fields = ["amount_sent"]

    @staticmethod
    def is_displayed(player):
        # DO NOT DO THIS - IT IS FRAGILE AND NOT EASY TO UNDERSTAND:
        # return player.id_in_group == 1

        return player.role == C.ROLE_DICTATOR


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        for player in group.get_players():
            if player.role == C.ROLE_DICTATOR:
                player.payoff = C.ENDOWMENT - group.amount_sent
            else:
                player.payoff = group.amount_sent


class Results(Page):
    pass


page_sequence = [Dictate, ResultsWaitPage, Results]
