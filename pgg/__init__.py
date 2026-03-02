from otree.api import *

doc = """
Public goods game with history table
"""


class C(BaseConstants):
    NAME_IN_URL = "pgg"
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 5
    MULTIPLIER = 2
    ENDOWMENT = cu(10)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    @property
    def contributions(self):
        return sum(p.contribution for p in self.get_players())

    @property
    def account_balance(self):
        return C.MULTIPLIER * self.contributions


class Player(BasePlayer):
    contribution = models.CurrencyField(
        label="How much do you wish to contribute to the group account?",
        min=cu(0),
        max=C.ENDOWMENT,
    )

    @property
    def history(self):
        return [
            {
                "round": p.round_number,
                "my_contrib": p.contribution,
                "my_payoff": p.payoff,
                "contributions": p.group.contributions,
                "account_balance": p.group.account_balance,
            }
            for p in self.in_previous_rounds()
        ]


# PAGES
class Decide(Page):
    form_fields = ["contribution"]
    form_model = "player"


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        for player in group.get_players():
            player.payoff = (
                C.ENDOWMENT
                + (C.MULTIPLIER / C.PLAYERS_PER_GROUP) * group.account_balance
                - player.contribution
            )


class Results(Page):
    pass


page_sequence = [Decide, ResultsWaitPage, Results]
