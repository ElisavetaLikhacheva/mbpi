from otree.api import *
import numpy as np

doc = """
Your app description
"""

def other_player(player):
    return player.get_others_in_group()[0]



class C(BaseConstants):
    NAME_IN_URL = 'mbpi'
    PLAYERS_PER_GROUP = 2
    NUM_ROUNDS = 1
    BONUS = cu(100)

    # WINNER_ROLE = 'Winner'
    # LOSER_ROLE = 'Loser'


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):

    winner_role = models.BooleanField()

    ret_payoff = models.CurrencyField()
    other_ret_payoff = models.CurrencyField()
    other_score = models.IntegerField()
    other_hard_treatment = models.IntegerField()

    ###
    left_side_amount = models.IntegerField(initial=10)
    c1 = models.StringField()
    c2 = models.StringField()
    c3 = models.StringField()
    c4 = models.StringField()
    c5 = models.StringField()
    c6 = models.StringField()
    c7 = models.StringField()
    c8 = models.StringField()
    c9 = models.StringField()
    c10 = models.StringField()
    c11 = models.StringField()
    # payout = models.IntegerField()

    mpl_message = models.LongStringField()
    mpl_info = models.BooleanField()
    point_of_change = models.IntegerField()
    selected_choice = models.StringField()

    # PosteriorBeliefs
    # posterior_prob_hard = models.IntegerField(min=0, max=100,
    #                                           label='Как Вы теперь думаете, какова вероятность того, что '
    #                                             'Вы оказались в группе со сложными заданиями?')
    posterior_ppl_lower = models.IntegerField(min=0, max=100,
                                              label='Как Вы теперь думаете, сколько из каждых 100 людей выполнили'
                                                ' задание хуже, чем Вы? ')
    posterior_deserve_bonus = models.IntegerField(min=0, max=100,
                                                  label='Основываясь на Вашем результате, как Вы теперь думаете, насколько Вы заслуживаете бонус?')
    posterior_merit = models.IntegerField(min=0, max=100,
                                          label='Как Вы думаете, насколько Ваш результат определяется усилиями или удачей?')


# PAGES
class WP1(WaitPage):
    group_by_arrival_time = True

    @staticmethod
    def after_all_players_arrive(group: Group):
        # subsession = group.subsession

        for p in group.get_players():
            if p.participant.score > p.get_others_in_group()[0].participant.score:
                p.winner_role = 1
                p.participant.ret_payoff = p.ret_payoff = C.BONUS
                p.payoff = C.BONUS
            elif p.participant.score < p.get_others_in_group()[0].participant.score:
                p.winner_role = 0
                p.participant.ret_payoff = p.ret_payoff = cu(0)
                p.payoff = cu(0)
            else:
                if p.id_in_group == 1:
                    p.winner_role = 1
                    p.participant.ret_payoff = p.ret_payoff = C.BONUS
                    p.payoff = C.BONUS
                else:
                    p.winner_role = 0
                    p.participant.ret_payoff = p.ret_payoff = cu(0)
                    p.payoff = cu(0)

        for p in group.get_players():
            p.other_ret_payoff = p.participant.other_ret_payoff = other_player(p).ret_payoff
            p.other_score = p.participant.other_score = other_player(p).participant.score
            # p.hard = p.participant.other_score = other_player(p).participant.score
            p.other_hard_treatment = p.participant.other_hard_treatment = other_player(p).participant.hard_treatment

            p.participant.past_group_id = group.id


class MatchingResultsWinners(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.winner_role == 1


class MatchingResultsLosers(Page):

    @staticmethod
    def is_displayed(player: Player):
        return player.winner_role == 0


class Mpl(Page):
    pass


class MplResults(Page):
    pass


class PosteriorBeliefs1(Page):
    pass

class DecideMPL(Page):
    form_model = 'player'
    form_fields = ['c1', 'c2', 'c3', 'c4', 'c5', 'c6', 'c7', 'c8', 'c9', 'c10','c11']

    @staticmethod
    def vars_for_template(player: Player):
        keys = range(1, 12)
        values = [cu(0), cu(0), cu(0), cu(0), cu(0), cu(0), cu(10), cu(50), cu(100), cu(150), cu(250)]
        both_side_amounts = {keys[i]: [[values[-1-i], values[i]]] for i in range(len(keys))}
        print(both_side_amounts)
        return {'both_side_amounts': both_side_amounts}

    def before_next_page(player: Player, timeout_happened):
        participant = player.participant
        values = [cu(0), cu(0), cu(0), cu(0), cu(0), cu(0), cu(10), cu(50), cu(100), cu(150), cu(250)]

        # define risk aversion param to pass on to steering_app
        for i in range(1, 12):
            field_name = "c" + str(i)
            if getattr(player, field_name) == "left":
                continue
            else:
                player.point_of_change = int(field_name[1:])
                print('player.point_of_change:', player.point_of_change)
                break
        # randomly select row as prize for subject, draw lottery in case it choice was left
        p_range = [i for i in range(1, 12)]
        player.selected_choice = "c" + str(np.random.choice(p_range))

        print('selected_choice:', player.selected_choice, int(player.selected_choice[1:]))

        if getattr(player, player.selected_choice) == "right":
            participant.mpl_info = player.mpl_info = 0
            participant.mpl_payoff = values[1-int(player.selected_choice[1:])]
            player.payoff = player.payoff + participant.mpl_payoff

            print('right', participant.mpl_payoff, player.payoff)
            participant.message = f"Случайно была выбрана строка {player.selected_choice[1:]}. В ней Вы выбрали не узнавать информацию и получить дополнительно {participant.mpl_payoff}. "
        else:
            participant.mpl_info = player.mpl_info = 1
            participant.mpl_payoff = values[int(player.selected_choice[1:])-1]
            player.payoff = player.payoff + participant.mpl_payoff

            print('left', participant.mpl_payoff, player.payoff)
            participant.message = (f"Случайно была выбрана строка {player.selected_choice[1:]}. В ней Вы выбрали узнать информацию и получить дополнительно {participant.mpl_payoff}. ")


class ResultMPL(Page):
    pass


class IntroMPL(Page):
    pass

class OverallIntro(Page):
    pass


# class PosteriorBeliefs1(Page):
#     form_model = 'player'
#     form_fields = [
#         'posterior_deserve_bonus'
#     ]



class PosteriorBeliefs2(Page):
    form_model = 'player'
    form_fields = [
        'posterior_ppl_lower'
    ]


class PosteriorBeliefs3(Page):
    form_model = 'player'
    form_fields = [
        'posterior_deserve_bonus'
    ]


class PosteriorBeliefsMerit(Page):
    form_model = 'player'
    form_fields = [
        'posterior_merit'
    ]

page_sequence = [
    WP1,
    MatchingResultsWinners,
    MatchingResultsLosers,
    # OverallIntro,
    IntroMPL,
    DecideMPL,
    ResultMPL,
    # PosteriorBeliefs1,
    PosteriorBeliefs2,
    PosteriorBeliefs3,
    PosteriorBeliefsMerit
]
