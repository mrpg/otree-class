from otree.api import *

doc = """
Show and reshow instructions
"""


class C(BaseConstants):
    NAME_IN_URL = "instruction_modal"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    contribution = models.CurrencyField(
        label="What is your contribution?",
        min=cu(0),
        max=cu(10),
    )


# PAGES
class ViewInstructions(Page):
    pass


class Decision(Page):
    form_model = "player"
    form_fields = ["contribution"]


page_sequence = [ViewInstructions, Decision]
