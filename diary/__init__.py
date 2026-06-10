from time import time

from otree.api import *

doc = """
Surveillance game
"""


class C(BaseConstants):
    NAME_IN_URL = "diary"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    ROLE_OBSERVER = "observer"
    ROLE_DIARIST = "diarist"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    diary_entry = models.LongStringField(initial="")
    sentinel = models.BooleanField()


class Player(BasePlayer):
    pass


class Entry(ExtraModel):
    group = models.Link(Group)
    timestamp = models.FloatField()
    entry = models.LongStringField()


def custom_export(players):
    yield ["diarist", "timestamp", "entry"]

    for player in players:
        if player.role == C.ROLE_DIARIST:
            for entry in Entry.filter(group=player.group):
                yield player.participant.code, entry.timestamp, entry.entry


def sentinel_error_message(group, value):
    # We don't care about the value!
    # We check an auxiliary condition.

    # The following check is completely arbitrary. You can go crazy!

    min_length = group.session.config["min_length"]

    if len(group.diary_entry) < min_length:
        return (
            f"Your diary entry is too short. Must be at least {min_length} characters."
        )


# PAGES
class MyPage(Page):
    form_fields = ["diary_entry", "sentinel"]
    form_model = "group"

    @staticmethod
    def live_method(player, data):
        if player.role == C.ROLE_DIARIST:  # Always validate in a live method!
            player.group.diary_entry = data

            # Save to ExtraModel
            Entry.create(
                group=player.group,
                timestamp=time(),
                entry=data,
            )

            return {player.group.get_player_by_role(C.ROLE_OBSERVER).id_in_group: data}

    @staticmethod
    def js_vars(player):
        return {"current_entry": player.group.diary_entry}


page_sequence = [
    MyPage,
]
