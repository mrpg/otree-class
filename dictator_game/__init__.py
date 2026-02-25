from otree.api import *

doc = """
Simple dictator game
"""


class C(BaseConstants):
    NAME_IN_URL = "dictator_game"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    DICTATOR_ENDOWMENT = cu(10)

    # We can define roles as follows:
    ROLE_DICTATOR = "dictator"
    ROLE_RECIPIENT = "recipient"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    amount_given = models.CurrencyField(
        label="How much do you want to give to the recipient?",
        min=cu(0),
        max=(C.DICTATOR_ENDOWMENT),
    )


class Player(BasePlayer):
    pass


# PAGES
class Dictate(Page):
    form_fields = ["amount_given"]
    form_model = "group"  # <- This is crucial!

    @staticmethod
    def is_displayed(player):
        return player.role == C.ROLE_DICTATOR


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        # This method allows you to write code for when both players
        # are ready to pass from this WaitPage. Here, we will just
        # set the payoffs according to players’ role.

        # The following code finds players by their role.

        dictator = group.get_player_by_role(C.ROLE_DICTATOR)
        recipient = group.get_player_by_role(C.ROLE_RECIPIENT)

        # And this code assigns players’ payoffs.

        dictator.payoff = C.DICTATOR_ENDOWMENT - group.amount_given
        recipient.payoff = group.amount_given


class Results(Page):
    pass


page_sequence = [Dictate, ResultsWaitPage, Results]
