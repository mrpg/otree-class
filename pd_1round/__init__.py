import random

from otree.api import *

doc = """
Repeated prisoner's dilemma (pay 1 round only)
"""


class C(BaseConstants):
    NAME_IN_URL = "pd_1round"
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
    payoff_here = (
        models.CurrencyField()
    )  # This substitutes for .payoff; .payoff pollutes the sum total
    pay_this = models.BooleanField(initial=False)

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

        row_player.payoff_here, col_player.payoff_here = C.PAYOFFS[  # IMPORTANT!
            row_player.cooperate, col_player.cooperate
        ]

        if group.round_number == C.NUM_ROUNDS:
            # We are in the final round
            # Randomly choose round to pay, and set .payoff!
            # Then, the sum of .payoff's is equal to the chosen round's payoff_here!

            for player in group.get_players():
                chosen_round = random.randint(1, C.NUM_ROUNDS)
                player.in_round(chosen_round).pay_this = True
                player.in_round(chosen_round).payoff = player.in_round(
                    chosen_round
                ).payoff_here

            # player.payoff will be 0 for all rounds EXCEPT the chosen round!

            # To select multiple rounds, use the below code
            # with k = number of rounds to be paid

            # k = 2

            # for player in group.get_players():
            #     chosen_rounds = random.sample(range(1, C.NUM_ROUNDS + 1), k)

            #     for chosen_round in chosen_rounds:
            #         player.in_round(chosen_round).pay_this = True
            #         player.in_round(chosen_round).payoff = player.in_round(
            #             chosen_round
            #         ).payoff_here


class Results(Page):
    pass


page_sequence = [MyPage, ResultsWaitPage, Results]
