from otree.api import *

doc = """
Framed donation experiment
"""


class C(BaseConstants):
    NAME_IN_URL = "donation"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(5)
    MULTIPLIER = 3


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    donation = models.CurrencyField(
        label="Your amount",
        min=cu(0),
        max=C.ENDOWMENT,
    )
    treatment = models.StringField()  # set in creating_session, not by the player
    charity = models.StringField(
        label="Please choose the charity.",
        choices=[
            "Unicef",
            "Doctors without borders",
            "The Royal Children's Hospital",
            "UniMelb",
            "University of Buckingham",
        ],
    )

    # use @property instead of vars_for_template
    @property
    def amount_received_by_charity(player):
        return C.MULTIPLIER * player.donation


# runs once when you create the session, before any pages are shown
def creating_session(subsession):
    import random

    for player in subsession.get_players():
        player.treatment = random.choice(["give", "take"])


# PAGES
class Donate(Page):
    form_fields = ["charity", "donation"]
    form_model = "player"

    @staticmethod
    def before_next_page(player, timeout_happened):  # runs when the player clicks Next
        player.payoff = C.ENDOWMENT - player.donation


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        pass  # THIS METHOD IS BANNED (most of the time)!


page_sequence = [Donate, Results]
