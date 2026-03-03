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
        widget=widgets.RadioSelectHorizontal,
    )

    timed_out = models.BooleanField(
        initial=False,
    )

    @property
    def partner(self):
        # This works because:
        # 3 - 1 = 2  (1's partner)
        # 3 - 2 = 1  (2's partner)
        # BAZINGA!
        return self.group.get_player_by_id(3 - self.id_in_group)

    @property
    def ever_dropped_out(self):
        # Any, are you OK? Are you OK, any?
        return any(p.timed_out for p in self.in_rounds(1, self.round_number))

    @property
    def partner_ever_dropped_out(self):
        return any(
            p.timed_out for p in self.partner.in_rounds(1, self.partner.round_number)
        )


# PAGES
@staticmethod
def group_still_alive(player):
    # Helper method for use in multiple Pages.
    # Don’t Repeat Yourself (DRY).
    # Neither I nor my partner must have dropped out, EVER.
    return not (player.ever_dropped_out or player.partner_ever_dropped_out)


class Discuss(Page):
    is_displayed = group_still_alive


class Decide(Page):
    form_fields = ["cooperate"]
    form_model = "player"  # Not group!
    timeout_seconds = 120
    is_displayed = group_still_alive

    @staticmethod
    def before_next_page(player, timeout_happened):
        if timeout_happened:
            print(f"{player} timed out!")
            player.timed_out = True


class ResultsWaitPage(WaitPage):
    is_displayed = group_still_alive

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
    is_displayed = group_still_alive

    @staticmethod
    def before_next_page(player, timeout_happened):
        if player.round_number == C.NUM_ROUNDS:  # Only run in final round
            import random

            # Note: my_round disappears without a trace after this method runs, so …
            my_round = random.randint(1, C.NUM_ROUNDS)

            # … better save it in participant.vars:
            player.participant.vars["round_selected_for_payment"] = my_round
            player.participant.payoff = player.in_round(my_round).payoff


class FinalResults(Page):
    @staticmethod
    def is_displayed(player):
        return player.round_number == C.NUM_ROUNDS


page_sequence = [
    Discuss,
    Decide,
    ResultsWaitPage,
    Results,
    FinalResults,
]
