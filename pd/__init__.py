from otree.api import *

doc = """
Repeated prisoner’s dilemma
"""


class C(BaseConstants):
    NAME_IN_URL = "pd"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3

    PAYOFF_MATRIX = {
        (True, True): (cu(9), cu(9)),
        (True, False): (cu(0), cu(12)),
        (False, True): (cu(12), cu(0)),
        (False, False): (cu(3), cu(3)),
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    cooperate = models.BooleanField(
        label="Please select your action.",
        choices=[
            [True, "Cooperate"],
            [False, "Defect"],
        ],
    )

    @property
    def partner(self):
        # This works because:
        # 3 - 1 = 2  (1's partner)
        # 3 - 2 = 1  (2's partner)
        # BAZINGA!
        return self.group.get_player_by_id(3 - self.id_in_group)


# PAGES
class Decide(Page):
    form_fields = ["cooperate"]
    form_model = "player"  # Not group!


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        player1 = group.get_player_by_id(1)
        player2 = group.get_player_by_id(2)

        # Python supports "parallel assignments:"
        # >>> a, b, c = 42, -15, 3
        # >>> a
        # 42
        # >>> b
        # -15
        # >>> c
        # 3

        player1.payoff, player2.payoff = C.PAYOFF_MATRIX[
            player1.cooperate, player2.cooperate
        ]


class Results(Page):
    pass


class FinalResults(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    Decide,
    ResultsWaitPage,
    Results,
    FinalResults,
]
