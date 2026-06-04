from os import environ

SESSION_CONFIGS = [
    dict(
        name="slides",
        app_sequence=["slides"],
        num_demo_participants=1,
    ),
    dict(
        name="survey",
        app_sequence=["survey"],
        num_demo_participants=1,
    ),
    dict(
        name="donation",
        app_sequence=["donation"],
        num_demo_participants=1,
    ),
    dict(
        name="dictator_game",
        app_sequence=["dictator_game"],
        num_demo_participants=2,  # <- THIS IS IMPORTANT
    ),
    dict(
        name="ultimatum_game",
        app_sequence=["ultimatum_game"],
        num_demo_participants=2,
    ),
    dict(
        name="pd",
        app_sequence=["pd", "dropout"],  # <- NOTE: dropout handler at the end
        num_demo_participants=2,
    ),
    dict(
        name="pd_1round",
        app_sequence=["pd_1round"],
        num_demo_participants=2,
    ),
]

ROOMS = [
    dict(
        name="simple_room",
        display_name="simple_room",
        participant_label_file="_rooms/my_labels.txt",  # oTree will authenticate participants!
    ),
]

# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=2.50,
    participation_fee=7.00,
    doc="",
)

PARTICIPANT_FIELDS = [
    "my_var"
]  # player.participant.my_var instead of player.participant.vars["my_var"]
SESSION_FIELDS = []

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = "en"

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = "AUD"
USE_POINTS = False

ADMIN_USERNAME = "admin"
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get("OTREE_ADMIN_PASSWORD")

DEMO_PAGE_INTRO_HTML = """ """

try:
    with open(".secret", "r") as f:
        SECRET_KEY = f.read().strip()
except FileNotFoundError:
    import secrets

    SECRET_KEY = secrets.token_hex()

    with open(".secret", "w") as f:
        f.write(SECRET_KEY)
