import random

from otree.api import *

doc = """
Framed donation experiment
"""


class C(BaseConstants):
    # C is for Constants
    NAME_IN_URL = "donation"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    ENDOWMENT = cu(25)


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    # 'payoff' is always there - it’s a CurrencyField!

    show_image = (
        models.BooleanField()
    )  # THIS WOULD BE WRONG, NEVER DO IT: initial=random.choice([True, False])

    # A BooleanField takes only two values:
    # True (1)
    # False (0)

    donation_amount = models.CurrencyField(
        label="How much would you like to donate?",
        min=cu(0),
        max=C.ENDOWMENT,
    )

    recipient = models.StringField(
        label="Please specify the recipient of your donation.",
        choices=["Max", "The dolphins", "University of Cologne"],
    )

    @property  # <- This is seriously good practice. Use more @propertys!
    def donation_amount_doubled(self):
        # 'self' is the actual player
        return 2 * self.donation_amount


# To randomize choice order:
# def recipient_choices(player):
#     choices = ["Max", "The dolphins", "University of Cologne"]
#
#     random.shuffle(choices)
#
#     return choices


def creating_session(subsession):
    for player in subsession.get_players():
        player.show_image = random.choice([True, False])


# PAGES
class ShowImage(Page):
    @staticmethod
    def is_displayed(player):
        return player.show_image


class Donation(Page):
    form_fields = ["recipient", "donation_amount"]
    form_model = "player"

    @staticmethod
    def before_next_page(player, timeout_happened):
        player.payoff = C.ENDOWMENT - player.donation_amount


class Results(Page):
    @staticmethod
    def vars_for_template(player):
        # This function is BANNED!
        pass


page_sequence = [ShowImage, Donation, Results]
