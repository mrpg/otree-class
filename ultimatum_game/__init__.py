from otree.api import *

doc = """
A simple ultimatum game
"""


class C(BaseConstants):
    NAME_IN_URL = "ultimatum_game"
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    ENDOWMENT = cu(20)

    ROLE_PROPOSER = "proposer"
    ROLE_RESPONDER = "responder"


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    offer = models.CurrencyField(
        label="How much do you offer to the responder?",
        min=cu(0),
        max=cu(C.ENDOWMENT),
    )
    accept = models.BooleanField(
        label="Do you accept this offer?",
    )

    @property  # A property is a SINGLE SOURCE OF TRUTH!
    def amount_kept(group):
        return C.ENDOWMENT - group.offer


class Player(BasePlayer):
    pass


# PAGES
class Offer(Page):
    form_model = "group"
    form_fields = ["offer"]

    @staticmethod
    def is_displayed(player):
        return player.role == C.ROLE_PROPOSER


class ResponderWaitPage(WaitPage):
    pass


class Accept(Page):
    form_model = "group"
    form_fields = ["accept"]

    @staticmethod
    def is_displayed(player):
        return player.role == C.ROLE_RESPONDER

    # This method is banned (in most cases, just use a @property). But you can
    # use it in certain exceptions. Here is an example:
    @staticmethod
    def vars_for_template(player):
        return dict(amount_kept=C.ENDOWMENT - player.group.offer)
        # You can now access this in your template as {{ amount_kept }}

        # vars_for_template is bad because:
        # 1. Modifications on player/group objects REPEAT upon RELOAD.
        # 2. Encourages code repetition, which is inherently fragile.
        # Better to use a single source of truth, with @properties that are
        # being reused consistently across your code.


class ResultsWaitPage(WaitPage):
    @staticmethod
    def after_all_players_arrive(group):
        # These methods allow you to find players by their role within the group:
        proposer = group.get_player_by_role(C.ROLE_PROPOSER)
        responder = group.get_player_by_role(C.ROLE_RESPONDER)

        if group.accept:
            proposer.payoff = (
                group.amount_kept
            )  # This is nice and clean, uses our @property!
            responder.payoff = group.offer
        else:
            proposer.payoff = responder.payoff = cu(0)


class Results(Page):
    pass


page_sequence = [Offer, ResponderWaitPage, Accept, ResultsWaitPage, Results]
