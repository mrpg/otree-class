from otree.api import *

doc = """
Repeated public goods game with random reshuffling
"""


class C(BaseConstants):
    NAME_IN_URL = "public_goods"
    PLAYERS_PER_GROUP = 3
    NUM_ROUNDS = 5
    ENDOWMENT = cu(20)
    MULTIPLIER = 2


class Subsession(BaseSubsession):
    pass


def creating_session(subsession):
    subsession.group_randomly()


class Group(BaseGroup):
    @property
    def total_contribution(group):
        return sum(p.contribution for p in group.get_players())

    @property
    def individual_share(group):
        return group.total_contribution * C.MULTIPLIER / C.PLAYERS_PER_GROUP


class Player(BasePlayer):
    contribution = models.CurrencyField(
        label="How much do you contribute to the public good?",
        min=cu(0),
        max=C.ENDOWMENT,
    )

    @property
    def history(player):
        return [
            {
                "round": p.round_number,
                "contribution": p.contribution,
                "total": p.group.total_contribution,
                "payoff": p.payoff,
            }
            for p in player.in_previous_rounds()
        ]


# PAGES
class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True


class Contribute(Page):
    form_model = "player"
    form_fields = ["contribution"]


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        for p in group.get_players():
            p.payoff = C.ENDOWMENT - p.contribution + group.individual_share


class Results(Page):
    pass


page_sequence = [ShuffleWaitPage, Contribute, ResultsWaitPage, Results]
