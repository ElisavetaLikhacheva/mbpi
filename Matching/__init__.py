from otree.api import *


doc = """
Your app description
"""


# def set_payoffs(group):
#     winner = group.get_player_by_role('Winner')
#     loser = group.get_player_by_role('Loser')
#     winner.payoff = winner.inc_endowment + C.COMMON_SHARE - group.share
#     recipient.payoff = recipient.inc_endowment + group.share


class C(BaseConstants):
    NAME_IN_URL = 'mbpi'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

    # WINNER_ROLE = 'Winner'
    # LOSER_ROLE = 'Loser'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    winner_role = models.BooleanField()


# PAGES
class WP1(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def after_all_players_arrive(group: Group):
        # subsession = group.subsession

        for p in group.get_players():
            if p.participant.score > p.get_others_in_group()[0].participant.score:
                p.winner_role = 1
            elif p.participant.score < p.get_others_in_group()[0].participant.score:
                p.winner_role = 0
            else:
                p.winner_role = 0


class MatchingResultsWinners(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.winner_role == 'Winner'


class MatchingResultsLoser(Page):

    @staticmethod
    def is_displayed(player: Player):
        player.winner_role == 'Loser'


class Mpl(Page):
    pass


class MplResults(Page):
    pass


class PosteriorBeliefs(Page):
    pass

page_sequence = [
    WP1,
    MatchingResultsWinners,
    MatchingResultsLoser,
    Mpl,
    MplResults,
    PosteriorBeliefs,
]
