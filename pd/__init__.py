from otree.api import *

doc = """
Repeated prisoner's dilemma
"""


class C(BaseConstants):
    NAME_IN_URL = "pd"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 3

    PAYOFFS = {
        (True, True): (3, 3),
        (True, False): (0, 5),
        (False, True): (5, 0),
        (False, False): (1, 1),
    }


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    cooperate = models.BooleanField(
        label="Please decide.",
        choices=[
            (True, "Cooperate"),
            (False, "Defect"),
        ],
    )

    @property
    def partner_cooperate(player):
        return player.group.get_player_by_id(3 - player.id_in_group).cooperate

        # If player.id_in_group == 1, THEN 3 - 1 = 2 (which is your partner!)
        # If player.id_in_group == 2, THEN 3 - 2 = 1 (which is YOUR partner!)
        # So this construct always returns your partner in a 2-player game:
        #   player.group.get_player_by_id(3 - player.id_in_group)


# PAGES
class MyPage(Page):
    form_model = "player"
    form_fields = ["cooperate"]


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        row_player = group.get_player_by_id(1)
        col_player = group.get_player_by_id(2)

        row_player.payoff, col_player.payoff = C.PAYOFFS[
            row_player.cooperate, col_player.cooperate
        ]

        # This is equivalent to:
        #   row_player.payoff = C.PAYOFFS[row_player.cooperate, col_player.cooperate][0]
        #   col_player.payoff = C.PAYOFFS[row_player.cooperate, col_player.cooperate][1]


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
