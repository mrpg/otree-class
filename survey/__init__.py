from otree.api import *

doc = """
My first oTree app: a simple survey
"""


class C(BaseConstants):
    NAME_IN_URL = "survey"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    fname = models.StringField(
        label="What is your first name?",
    )
    age = models.IntegerField(
        label="How old are you in years?",
        min=18,
        max=120,
    )  # An integer is a "whole" number


# PAGES
class Questionnaire(Page):
    form_fields = ["fname", "age"]
    form_model = "player"


class Results(Page):
    pass


page_sequence = [
    Questionnaire,
    Results,
]
