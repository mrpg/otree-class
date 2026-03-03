from otree.api import *

doc = """
Diary/surveillance game
"""


class C(BaseConstants):
    NAME_IN_URL = "diary"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    ROLE_WRITER = "writer"
    ROLE_WATCHER = "watcher"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    entry = models.LongStringField()


# PAGES
class Diary(Page):
    form_model = "player"

    @staticmethod
    def get_form_fields(player):
        if player.role == C.ROLE_WRITER:
            return ["entry"]
        else:
            return []

    @staticmethod
    def js_vars(player):
        return {
            "is_watcher": player.role == C.ROLE_WATCHER,
        }

    @staticmethod
    def live_method(player, data):
        # Crucial: always add validation to live_methods!
        if player.role == C.ROLE_WRITER and isinstance(data, str):
            # live_method returns a dict having as its keys the recipients' id_in_group
            # (or 0 to return to all in group); and the value is just the value to be sent.
            return {
                player.group.get_player_by_role(C.ROLE_WATCHER).id_in_group: data[::-1],
            }


page_sequence = [Diary]
