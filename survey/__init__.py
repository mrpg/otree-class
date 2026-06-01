from otree.api import *

doc = """
A simple survey
"""


class C(BaseConstants):
    NAME_IN_URL = "survey"  # You can change this to hide your experimental design from participants
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    name = models.StringField(
        label="What is your name?",
    )  # "Max", "Ava", "Juliana", "Welcome", "Goodbye"
    age = models.IntegerField(
        label="How old are you (in years)?",
        min=18,
        max=120,
    )  # 0, 42, 91, -5, -999


# PAGES
class MyPage(Page):
    form_model = "player"
    form_fields = ["name", "age"]


class Results(Page):
    pass


page_sequence = [MyPage, Results]
