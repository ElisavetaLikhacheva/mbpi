from os import environ

SESSION_CONFIGS = [
    dict(
        name='all',
        display_name='Base version',
        app_sequence=['RETasks', 'Matching', 'Distribution', 'Questionnaire'],
        num_demo_participants=4,
        # use_browser_bots=True
    ),
    dict(
        name='Real_effort_task_only',
        display_name='RETasks',
        app_sequence=['RETasks'],
        num_demo_participants=4,
        # use_browser_bots=True
    ),
    dict(
        name='Questionnaire',
        display_name='Questionnaire',
        app_sequence=['Questionnaire'],
        num_demo_participants=4,
        # use_browser_bots=True
    ),
    # dict(
    #     name='Real-effort task only',
    #     display_name='Base version',
    #     app_sequence=['RETasks'],
    #     num_demo_participants=4,
    #     # use_browser_bots=True
    # ),
]
# if you set a property in SESSION_CONFIG_DEFAULTS, it will be inherited by all configs
# in SESSION_CONFIGS, except those that explicitly override it.
# the session config can be accessed from methods in your apps as self.session.config,
# e.g. self.session.config['participation_fee']

SESSION_CONFIG_DEFAULTS = dict(
    real_world_currency_per_point=1, participation_fee=50, doc=""
)

PARTICIPANT_FIELDS = ['is_dropout',
                      'hard_treatment',
                      'score',
                      'other_hard_treatment',
                      'other_score',
                      'ret_payoff',
                      'other_ret_payoff',
                      'past_group_id',

                      'mpl_info',
                      'mpl_payoff',
                      'message']

SESSION_FIELDS = ['params']

# ISO-639 code
# for example: de, fr, ja, ko, zh-hans
LANGUAGE_CODE = 'ru'

# e.g. EUR, GBP, CNY, JPY
REAL_WORLD_CURRENCY_CODE = 'RUB'
USE_POINTS = True

ADMIN_USERNAME = 'admin'
# for security, best to set admin password in an environment variable
ADMIN_PASSWORD = environ.get('OTREE_ADMIN_PASSWORD')

DEMO_PAGE_INTRO_HTML = """ """

SECRET_KEY = '4867905599132'

# adjustments for testing
# generating session configs for all varieties of features
import sys

ROOMS = [
    dict(
        name='econ_lab',
        display_name='Experimental Economics Lab'
    ),
]

if sys.argv[1] == 'test':
    MAX_ITERATIONS = 5
    FREEZE_TIME = 0.1
    TRIAL_PAUSE = 0.2
    TRIAL_TIMEOUT = 0.3

    SESSION_CONFIGS = [
        # dict(
        #     name=f"testing_sliders",
        #     num_demo_participants=1,
        #     app_sequence=['sliders'],
        #     trial_delay=TRIAL_PAUSE,
        #     retry_delay=FREEZE_TIME,
        #     num_sliders=3,
        #     attempts_per_slider=3,
        # ),
    ]
    for task in ['decoding', 'matrix', 'transcription']:
        SESSION_CONFIGS.extend(
            [
                dict(
                    name=f"testing_{task}_defaults",
                    num_demo_participants=1,
                    app_sequence=['real_effort'],
                    puzzle_delay=TRIAL_PAUSE,
                    retry_delay=FREEZE_TIME,
                ),
                dict(
                    name=f"testing_{task}_retrying",
                    num_demo_participants=1,
                    app_sequence=['real_effort'],
                    puzzle_delay=TRIAL_PAUSE,
                    retry_delay=FREEZE_TIME,
                    attempts_per_puzzle=5,
                ),
                dict(
                    name=f"testing_{task}_limited",
                    num_demo_participants=1,
                    app_sequence=['real_effort'],
                    puzzle_delay=TRIAL_PAUSE,
                    retry_delay=FREEZE_TIME,
                    max_iterations=MAX_ITERATIONS,
                ),
            ]
        )
