from otree.api import *

doc = """
Repeated matching pennies
"""


class C(BaseConstants):
    NAME_IN_URL = "matching_pennies"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 10
    STAKE = cu(10)

    ROLE_MATCHER = "matcher"
    ROLE_MISMATCHER = "mismatcher"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    choice = models.BooleanField(
        label="Choose a side.",
        choices=[
            (True, "Heads"),
            (False, "Tails"),
        ],
    )

    @property
    def partner(player):
        return player.group.get_player_by_id(3 - player.id_in_group)

    @property
    def is_matcher(player):
        return player.role == C.ROLE_MATCHER

    @property
    def history(player):
        cumulative = cu(0)
        rows = []
        for p in player.in_previous_rounds():
            partner = p.group.get_player_by_id(3 - p.id_in_group)
            cumulative += p.payoff
            rows.append(
                {
                    "round": p.round_number,
                    "your_choice": p.choice,
                    "partner_choice": partner.choice,
                    "is_match": p.choice == partner.choice,
                    "payoff": p.payoff,
                    "cumulative": cumulative,
                }
            )
        return rows


# PAGES
class Choose(Page):
    form_model = "player"
    form_fields = ["choice"]


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        matcher = group.get_player_by_role(C.ROLE_MATCHER)
        mismatcher = group.get_player_by_role(C.ROLE_MISMATCHER)

        is_match = matcher.choice == mismatcher.choice
        matcher.payoff = C.STAKE if is_match else cu(0)
        mismatcher.payoff = cu(0) if is_match else C.STAKE


class Results(Page):
    pass


page_sequence = [Choose, ResultsWaitPage, Results]
