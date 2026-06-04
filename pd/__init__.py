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
    @property
    def history(group) -> list[dict]:
        rval = []

        for g in group.in_previous_rounds():
            # g here is the group in each previous round!

            rval.append(
                {
                    "round": g.round_number,
                    "player1": g.get_player_by_id(1).cooperate,
                    "player2": g.get_player_by_id(2).cooperate,
                }
            )

        return rval

    @property
    def any_dropout(group):
        return any(p.ever_dropout for p in group.get_players())


class Player(BasePlayer):
    cooperate = models.BooleanField(
        label="Please decide.",
        choices=[
            (True, "Cooperate"),
            (False, "Defect"),
        ],
    )
    timed_out = models.BooleanField(initial=False)

    @property
    def partner_cooperate(player):
        return player.group.get_player_by_id(3 - player.id_in_group).cooperate

        # If player.id_in_group == 1, THEN 3 - 1 = 2 (which is your partner!)
        # If player.id_in_group == 2, THEN 3 - 2 = 1 (which is YOUR partner!)
        # So this construct always returns your partner in a 2-player game:
        #   player.group.get_player_by_id(3 - player.id_in_group)

    @property
    def ever_dropout(player):
        return any(
            player.in_round(r).timed_out for r in range(1, player.round_number + 1)
        )


# PAGES
@staticmethod
def dropout_checker(player, upcoming_apps):
    if player.group.any_dropout:
        player.participant.vars["dropout"] = True
        player.participant.vars["dropout_me"] = player.ever_dropout

        # Further logic here, e.g., adjustment of payoffs

        return upcoming_apps[-1]  # Send this person to final app ("dropout")


class MyPage(Page):
    form_model = "player"
    form_fields = ["cooperate"]
    timeout_seconds = 10
    app_after_this_page = dropout_checker

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            player.timed_out = True


class ResultsWaitPage(WaitPage):
    app_after_this_page = dropout_checker

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
    app_after_this_page = dropout_checker


page_sequence = [MyPage, ResultsWaitPage, Results]
