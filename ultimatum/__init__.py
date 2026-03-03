from otree.api import *

doc = """
Ultimatum Game
"""


class C(BaseConstants):
    NAME_IN_URL = "ultimatum"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    PROPOSER_ENDOWMENT = cu(10)

    # We can define roles as follows:
    ROLE_PROPOSER = "proposer"
    ROLE_RECIPIENT = "recipient"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    amount_given = models.CurrencyField(
        label="How much do you want to give to your fellow player?",
        min=cu(0),
        max=C.PROPOSER_ENDOWMENT,
    )

    accept = models.BooleanField(
        label="Please select your action.",
        choices=[
            [True, "Accept"],
            [False, "Reject"],
        ],
        widget=widgets.RadioSelect,
    )

    @property
    def proposer(self):
        return self.get_player_by_role(C.ROLE_PROPOSER)

    @property
    def recipient(self):
        return self.get_player_by_role(C.ROLE_RECIPIENT)


class Player(BasePlayer):
    pass


# PAGES
class Propose(Page):
    form_fields = ["amount_given"]
    form_model = "group"

    @staticmethod
    def is_displayed(player):
        return player.role == C.ROLE_PROPOSER


class WaitRecipient(WaitPage):
    @staticmethod
    def is_displayed(player):
        return player.role == C.ROLE_RECIPIENT


class Accept(Page):
    form_fields = ["accept"]
    form_model = "group"

    @staticmethod
    def is_displayed(player):
        return player.role == C.ROLE_RECIPIENT


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):

        if group.accept:
            group.proposer.payoff = C.PROPOSER_ENDOWMENT - group.amount_given
            group.recipient.payoff = group.amount_given
        else:
            group.proposer.payoff = cu(0)
            group.recipient.payoff = cu(0)


class Results(Page):
    pass


page_sequence = [Propose, WaitRecipient, Accept, ResultsWaitPage, Results]
