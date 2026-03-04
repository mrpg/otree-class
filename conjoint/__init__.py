from otree.api import *

doc = """
Conjoint experiment
"""

PROFILE_ATTRS = [
    "has_beaches",
    "english",
    "accommodation",
    "partying",
    "sunny",
    "grading",
    "costs",
]


class C(BaseConstants):
    NAME_IN_URL = "conjoint"
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1

    HAS_BEACHES = [True, False]
    ENGLISH = [True, False]
    ACCOMMODATION = [True, False]
    PARTYING = [True, False]
    SUNNY = [True, False]
    GRADING = [1, 2, 3]
    COSTS = [-1, 0, 1]


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    current_pair = models.IntegerField(initial=0)
    sentinel = (
        models.IntegerField()
    )  # This is a sentinel field to prevent early submission


class Profiles(ExtraModel):
    player = models.Link(Player)
    pair_id = models.IntegerField()  # which comparison (0..n_pairs-1)
    side = models.IntegerField()  # 0 = left (Option A), 1 = right (Option B)
    has_beaches = models.BooleanField()
    english = models.BooleanField()
    accommodation = models.BooleanField()
    partying = models.BooleanField()
    sunny = models.BooleanField()
    grading = models.IntegerField()
    costs = models.IntegerField()


class Preference(ExtraModel):
    player = models.Link(Player)
    pair_id = models.IntegerField()
    preferred_side = models.IntegerField()  # 0 = left, 1 = right


def creating_session(subsession):
    import random

    for player in subsession.get_players():
        for pair_id in range(subsession.session.config["n_pairs"]):
            for side in (0, 1):
                Profiles.create(
                    player=player,
                    pair_id=pair_id,
                    side=side,
                    has_beaches=random.choice(C.HAS_BEACHES),
                    english=random.choice(C.ENGLISH),
                    accommodation=random.choice(C.ACCOMMODATION),
                    partying=random.choice(C.PARTYING),
                    sunny=random.choice(C.SUNNY),
                    grading=random.choice(C.GRADING),
                    costs=random.choice(C.COSTS),
                )


def profile_to_dict(p):
    return dict(
        has_beaches=p.has_beaches,
        english=p.english,
        accommodation=p.accommodation,
        partying=p.partying,
        sunny=p.sunny,
        grading=p.grading,
        costs=p.costs,
    )


def get_current_pair(player):
    """Return the current pair of profiles, or None if all pairs are done."""
    pair_id = player.current_pair
    if pair_id >= player.session.config["n_pairs"]:
        return None
    profiles = Profiles.filter(player=player, pair_id=pair_id)
    by_side = {p.side: p for p in profiles}
    return dict(
        type="pair",
        left=profile_to_dict(by_side[0]),
        right=profile_to_dict(by_side[1]),
        current=pair_id + 1,
        total=player.session.config["n_pairs"],
    )


def sentinel_error_message(player, value):
    # We don’t care about the value!

    if player.current_pair < player.session.config["n_pairs"]:
        return "You cannot yet proceed."


# PAGES
class Choice(Page):
    form_fields = ["sentinel"]
    form_model = "player"

    @staticmethod
    def live_method(player, data):
        if not isinstance(data, list) or len(data) == 0:
            return

        action = data[0]

        if action == "get":
            pair = get_current_pair(player)
            if pair is None:
                return {player.id_in_group: dict(type="done")}
            return {player.id_in_group: pair}

        elif action == "submit" and len(data) > 1 and data[1] in (0, 1):
            chosen_side = data[1]
            pair_id = player.current_pair
            if pair_id >= player.session.config["n_pairs"]:
                return {player.id_in_group: dict(type="done")}

            Preference.create(
                player=player,
                pair_id=pair_id,
                preferred_side=chosen_side,
            )
            player.current_pair = pair_id + 1

            pair = get_current_pair(player)
            if pair is None:
                return {player.id_in_group: dict(type="done")}
            return {player.id_in_group: pair}


def custom_export(players):
    # Each row = one pair comparison, with both profiles' attributes and the player's choice
    header = ["session", "participant_code", "pair_id"]
    for attr in PROFILE_ATTRS:
        header.append("left_" + attr)
    for attr in PROFILE_ATTRS:
        header.append("right_" + attr)
    header.append("preferred_side")
    yield header

    for p in players:
        participant = p.participant
        session = p.session
        profiles = Profiles.filter(player=p)
        preferences = Preference.filter(player=p)
        pref_by_pair = {pref.pair_id: pref.preferred_side for pref in preferences}

        # Group profiles by pair_id
        pairs = {}
        for prof in profiles:
            pairs.setdefault(prof.pair_id, {})[prof.side] = prof

        for pair_id in sorted(pairs.keys()):
            sides = pairs[pair_id]
            if 0 not in sides or 1 not in sides:
                continue
            left = sides[0]
            right = sides[1]
            row = [session.code, participant.code, pair_id]
            for attr in PROFILE_ATTRS:
                row.append(getattr(left, attr))
            for attr in PROFILE_ATTRS:
                row.append(getattr(right, attr))
            row.append(pref_by_pair.get(pair_id, ""))
            yield row


page_sequence = [Choice]
