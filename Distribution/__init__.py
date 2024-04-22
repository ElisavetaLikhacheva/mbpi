from otree.api import *
import itertools

doc = """
Your app description
"""

def other_player(player):
    return player.get_others_in_group()[0]


class C(BaseConstants):
    NAME_IN_URL = 'distribution'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1

def group_by_arrival_time_method(Subsession, waiting_players):
    # session = subsession.session

    for possible_group in itertools.combinations(waiting_players, 2):
        print(possible_group[0].participant.past_group_id)
        if possible_group[0].participant.past_group_id != possible_group[1].participant.past_group_id:
            return possible_group

        # pair_ids = set(p.participant.past_group_id for p in possible_group)
        # if pair_ids not in session.past_groups:
        #     session.past_groups.append(pair_ids)
        #     return possible_group


    # # this generates all possible pairs of waiting players
    # # and checks if the group would be valid.
    # for possible_group in itertools.combinations(waiting_players, 2):
    #     # use a set, so that we can easily compare even if order is different
    #     # e.g. {1, 2} == {2, 1}
    #     pair_ids = set(p.id_in_subsession for p in possible_group)
    #     # if this pair of players has not already been played
    #     if pair_ids not in session.past_groups:
    #         # mark this group as used, so we don't repeat it in the next round.
    #         session.past_groups.append(pair_ids)
    #         # in this function,
    #         # 'return' means we are creating a new group with this selected pair
    #         return possible_group


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    other1_score = models.IntegerField()
    other2_score = models.IntegerField()
    other1_hard_treatment = models.IntegerField()
    other2_hard_treatment = models.IntegerField()
    other1_payoff = models.CurrencyField()
    other2_payoff = models.CurrencyField()

    share = models.CurrencyField(label='Как бы Вы разделили 100 очков между участниками 1 и 2? Переместите слайдер, '
                                       'чтобы зафиксировать Ваше решение.')


class WP(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def after_all_players_arrive(group):
        for p in group.get_players():
            p.other1_score = other_player(p).participant.score
            p.other1_hard_treatment = other_player(p).participant.hard_treatment
            p.other1_payoff = other_player(p).participant.ret_payoff

            p.other2_score = other_player(p).participant.other_score
            p.other2_hard_treatment = other_player(p).participant.other_hard_treatment
            p.other2_payoff = other_player(p).participant.other_ret_payoff


# PAGES
class DGInstruction(Page):
    pass


class DGDecision(Page):
    form_model = 'player'
    form_fields = ['share']


class ResultsWaitPage(WaitPage):
    pass


class Results(Page):
    pass


page_sequence = [WP,
                 DGInstruction,
                 DGDecision,
                 # ResultsWaitPage,
                 # Results
                 ]
