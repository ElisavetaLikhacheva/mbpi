from otree.api import *
import random
import itertools

doc = """
Your app description
"""


# np.random.seed(0)
class C(BaseConstants):
    NAME_IN_URL = 'questionnaire'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1
    # ENDOWMENT = cu(10)
    # DICTATOR_ROLE = 'A'
    # RECIPIENT_ROLE = 'Б'
    # COMMON_SHARE = cu(150)
    # TREATMENT = [1, 2, 3, 4, 5, 6, 7]

    Q_GENDER = [
        [0, 'Мужской'],
        [1, 'Женский'],
    ]
    Q_FINANCIAL_CONDITIONS = [
        [1, '1 — Денег не хватает даже на питание'],
        [2, '2 — На питание денег хватает, но не хватает на покупку одежды и обуви'],
        [3, '3 — На покупку одежды и обуви денег хватает, но не хватает на покупку бытовой техники (холодильник, телевизор, компьютер)'],
        [4, '4 — На покупку бытовой техники денег хватает, но не хватает на покупку автомобиля'],
        [5, '5 — На автомобиль денег хватает, но не хватает на покупку недвижимого имущества'],
        [6, '6 — Материальных затруднений не испытываем, есть возможность приобрести любое движимое и недвижимое имущество'],
        # [9, 'Затрудняюсь ответить'],
    ]
    Q_EDUCATION = [
        [1, 'Начальное общее образование (4 класса)'],
        [2, 'Основное общее образование (9 классов)'],
        [3, 'Среднее (полное) общее образование (11 классов)'],
        [4, 'Среднее профессиональное образование (колледж/техникум)'],
        [5, 'Неоконченное высшее образование'],
        [6, 'Высшее образование (бакалавриат, специалитет)'],
        [7, 'Два и более высших образования или аспирантура'],
    ]
    Q_MARRIAGE = [
        [1, 'Никогда не состоял(a)'],
        [2, 'В зарегистрированном браке'],
        [3, 'В незарегистрированном браке'],
        [4, 'Вдовец (вдова)'],
        [5, 'Разведен (разведена)'],
        [6, 'Брак зарегистрирован, но вместе не живем'],
        [7, 'Затрудняюсь ответить']

    ]
    Q_INEQUALITY_PROBLEM = [
        [1, 'Не проблема вообще'],
        [2, 'Небольшая проблема'],
        [3, 'Проблема'],
        [4, 'Серьезная проблема'],
        [5, 'Очень серьезная проблема']
    ]
    Q_INCOME_INCREASING = [
        [1, 'Возросло'],
        [2, 'Не изменилось'],
        [3, 'Снизилось'],
    ]
    Q_4_YES_NO = [
        [1, 'Да'],
        [2, 'Скорее да'],
        [3, 'Скорее нет'],
        [4, 'Нет'],
    ]
    Q_4_IMPORTANT = [
        [1, 'Очень важно'],
        [2, 'Довольно важно'],
        [3, 'Не очень важно'],
        [4, 'Совсем неважно'],
    ]
    Q_TRUST = [
        [1, "Нужно быть очень осторожным с другими людьми"],
        [2, "Большинству людей можно вполне доверять"],
    ]
    # Q_PARTY = [
    #     [1, 'Единая Россия'],
    #     [2, 'Коммунистическая партия Российской Федерации (КПРФ)'],
    #     [3, 'Справедливая Россия — За правду (СРЗП)'],
    #     [4, 'Либерально-демократическая партия России (ЛДПР)'],
    #     [5, 'Новые люди'],
    #     [6, 'Российская объединённая демократическая партия «Яблоко»'],
    #     [7, 'Другая зарегистрированная партия'],
    #     [8, 'Нет партии, которая могла бы представлять мои интересы'],
    #     [9, 'Я не интересуюсь политикой'],
    # ]
    Q_PYRAMIDS = [
        [1, 'А'],
        [2, 'Б'],
        [3, 'В'],
        [4, 'Г'],
        [5, 'Д']
    ]
    Q_PLACE_LIVING = [
        [1, 'Крупный город с населением больше 1 миллиона человек'],
        [2, 'Город с населением от 250 тысяч человек до 1 миллиона'],
        [3, 'Город с населением от 50 до 250 тысяч человек'],
        [4, 'Город с населением от 10 до 50 тысяч человек'],
        [5, 'Населенный пункт до 10 тысяч человек'],
    ]
    Q_OCCUPATION = [
        [1, 'Государственная служба'],
        [2, 'Частный сектор'],
        [3, 'Собственный бизнес или самозанятость'],
        [4, 'Некоммерческий сектор'],
        [5, 'Студент'],
        [6, 'Безработный'],
        [7, 'Выбыл(а) из состава рабочей силы (выход на пенсию, отпуск по уходу за ребенком)'],
    ]
    Q_CHARITY = [
        [1, 'Нет'],
        [2, 'Да, жертвовал(а) деньги на благотворительность'],
        [3, 'Да, участвовал(а) в качестве волонтера'],
        [4, 'Да, жертвовал(а) деньги и участвовал(а) волонтером']
    ]
    # Q_FINANCIAL_CONDITIONS = [
    #     [1, 'Денег не хватает даже на питание'],
    #     [2, 'На питание денег хватает, но не хватает на покупку одежды и обуви'],
    #     [3, 'На покупку одежды и обуви денег хватает, но не хватает на покупку мелкой бытовой техники'],
    #     [4, 'На покупку мелкой бытовой техники денег хватает, но не хватает на покупку крупной бытовой техники'],
    #     [5, 'Денег хватает на покупку крупной бытовой техники, но мы не сможем купить новую машину'],
    #     [6, 'На новую машину денег хватает, но мы не можем купить небольшую квартиру'],
    #     [7, 'На небольшую квартиру денег хватает, но мы не смогли бы купить большую квартиру в хорошем районе'],
    #     [8, 'Материальных затруднений не испытываем, при необходимости могли бы приобрести квартиру, дом'],
    #     [9, 'Затрудняюсь ответить'],
    # ]
    Q_RELIGION = [
        [1, 'Католицизм'],
        [2, 'Протестантизм'],
        [3, 'Православие'],
        [4, 'Иудаизм'],
        [5, 'Ислам'],
        [6, 'Буддизм'],
        [7, 'Другую религию'],
        [8, 'Не исповедую никакой религии (атеист)']
    ]
    Q_BIG5 = [
        [1, 'Полностью согласен'],
        [2, 'Скорее согласен'],
        [3, 'Затрудняюсь ответить'],
        [4, 'Скорее не согласен'],
        [5, 'Полностью не согласен']
    ]
    Q_REGIONS = [
        [77, 'Москва'],
        [78, 'Санкт-Петербург'],
        [22, 'Алтайский край'],
        [28, 'Амурская область'],
        [29, 'Архангельская область'],
        [30, 'Астраханская область'],
        [31, 'Белгородская область'],
        [32, 'Брянская область'],
        [33, 'Владимирская область'],
        [34, 'Волгоградская область'],
        [35, 'Вологодская область'],
        [36, 'Воронежская область'],
        [93, 'Донецкая Народная Республика'],
        [79, 'Еврейская автономная область'],
        [75, 'Забайкальский край'],
        [90, 'Запорожская область'],
        [37, 'Ивановская область'],
        [99, 'Иные территории, включая город и космодром Байконур'],
        [38, 'Иркутская область'],
        [7, 'Кабардино-Балкарская Республика'],
        [39, 'Калининградская область'],
        [40, 'Калужская область'],
        [41, 'Камчатский край'],
        [9, 'Карачаево-Черкесская Республика'],
        [42, 'Кемеровская область - Кузбасс'],
        [43, 'Кировская область'],
        [44, 'Костромская область'],
        [23, 'Краснодарский край'],
        [24, 'Красноярский край'],
        [45, 'Курганская область'],
        [46, 'Курская область'],
        [47, 'Ленинградская область'],
        [48, 'Липецкая область'],
        [94, 'Луганская Народная Республика'],
        [49, 'Магаданская область'],
        [50, 'Московская область'],
        [51, 'Мурманская область'],
        [83, 'Ненецкий автономный округ'],
        [52, 'Нижегородская область'],
        [53, 'Новгородская область'],
        [54, 'Новосибирская область'],
        [55, 'Омская область'],
        [56, 'Оренбургская область'],
        [57, 'Орловская область'],
        [58, 'Пензенская область'],
        [59, 'Пермский край'],
        [25, 'Приморский край'],
        [60, 'Псковская область'],
        [1, 'Республика Адыгея (Адыгея)'],
        [4, 'Республика Алтай'],
        [2, 'Республика Башкортостан'],
        [3, 'Республика Бурятия'],
        [5, 'Республика Дагестан'],
        [6, 'Республика Ингушетия'],
        [8, 'Республика Калмыкия'],
        [10, 'Республика Карелия'],
        [11, 'Республика Коми'],
        [91, 'Республика Крым'],
        [12, 'Республика Марий Эл'],
        [13, 'Республика Мордовия'],
        [14, 'Республика Саха (Якутия)'],
        [15, 'Республика Северная Осетия - Алания'],
        [16, 'Республика Татарстан (Татарстан)'],
        [17, 'Республика Тыва'],
        [19, 'Республика Хакасия'],
        [61, 'Ростовская область'],
        [62, 'Рязанская область'],
        [63, 'Самарская область'],
        [64, 'Саратовская область'],
        [65, 'Сахалинская область'],
        [66, 'Свердловская область'],
        [92, 'Севастополь'],
        [67, 'Смоленская область'],
        [26, 'Ставропольский край'],
        [68, 'Тамбовская область'],
        [69, 'Тверская область'],
        [70, 'Томская область'],
        [71, 'Тульская область'],
        [72, 'Тюменская область'],
        [18, 'Удмуртская Республика'],
        [73, 'Ульяновская область'],
        [27, 'Хабаровский край'],
        [86, 'Ханты-Мансийский автономный округ - Югра'],
        [95, 'Херсонская область'],
        [74, 'Челябинская область'],
        [20, 'Чеченская Республика'],
        [21, 'Чувашская Республика - Чувашия'],
        [87, 'Чукотский автономный округ'],
        [89, 'Ямало-Ненецкий автономный округ'],
        [76, 'Ярославская область'],
    ]
    Q_BENEFITS = [
        [1, 'Проигрываю'],
        [2, 'Безразлично'],
        [3, 'Выигрываю']
    ]
    Q_CHURCH_ATTENDANCE = [
        [1, 'Вообще не бываю'],
        [2, '1 раз в месяц или реже'],
        [3, '2-3 раза в месяц'],
        [4, '4 раза в месяц или чаще'],
        [5, 'Без ответа, я атеист']
    ]
    # Q_IS_OCCUPIED_CHOICES = [[False, _('Нет')], [True, _('Да')]]
    Q_OCCUPATION_PARENT_CHOICES = [
        [1, "Руководители"],
        [2, "Специалисты высшего уровня квалификации"],
        [3, "Специалисты среднего уровня квалификации"],
        [4, "Служащие, занятые подготовкой и оформлением документации, учетом и обслуживанием"],
        [5, "Работники сферы обслуживания и торговли, охраны граждан и собственности"],
        [6, "Квалифицированные работники сельского и лесного хозяйства, рыбоводства и рыболовства"],
        [7, "Квалифицированные рабочие промышленности, строительства, транспорта и рабочие родственных занятий"],
        [8, "Операторы производственных установок и машин, сборщики и водители"],
        [9, "Неквалифицированные рабочие"],
        [10, "Военнослужащие"],
    ]


# FUNCTIONS
# def set_payoffs(group):
#     dictator = group.get_player_by_role('A')
#     recipient = group.get_player_by_role('Б')
#     dictator.payoff = dictator.inc_endowment + C.COMMON_SHARE - group.share
#     recipient.payoff = recipient.inc_endowment + group.share


def other_player(player):
    return player.get_others_in_group()[0]


# def creating_session(subsession):
#     subsession.group_randomly(fixed_id_in_group=True)


def high_position(label):
    return models.IntegerField(label=label, choices=C.Q_4_IMPORTANT, widget=widgets.RadioSelect)


def scale(label):
    return models.IntegerField(label=label, choices=range(0, 11), widget=widgets.RadioSelectHorizontal)


def big5(label):
    return models.IntegerField(label=label, choices=C.Q_BIG5, widget=widgets.RadioSelect)


def children_live_max(player):
    return player.children


def big5_calculation(first, second):
    return 3 + (first - second) / 2


# def endowment_ecu(num_financial_conditions):
#     if num_financial_conditions == 1:
#         inc_endowment = cu(5)
#     elif num_financial_conditions == 2:
#         inc_endowment = cu(15)
#     elif num_financial_conditions == 3:
#         inc_endowment = cu(25)
#     elif num_financial_conditions == 4:
#         inc_endowment = cu(50)
#     elif num_financial_conditions == 5:
#         inc_endowment = cu(180)
#     else:
#         inc_endowment = cu(250)
#     return inc_endowment


class Subsession(BaseSubsession):
    # num_groups_created = models.IntegerField(initial=0)
    pass


class Group(BaseGroup):
    # share = models.CurrencyField(min=0, max=C.COMMON_SHARE, label='Сколько очков Вы передадите участнику Б?')
    # treatment = models.IntegerField()
    #
    # check_info = models.BooleanField(label='Вы хотите получить информацию о финансовом положении другого '
    #                                        'участника?')
    # avoid_info = models.BooleanField(label='Вы хотите НЕ получать информацию о финансовом положении '
    #                                        'другого участника?')
    pass

class Player(BasePlayer):
    # other_player_financial_conditions = models.IntegerField()
    # inc_endowment = models.CurrencyField()

    # design_fairness = models.StringField(
    #     label='Как Вы считаете, соответствует ли соотношение очков, которое получили люди с разным финансовом положением, '
    #           'распределению доходов в России?',
    #     choices=C.Q_4_YES_NO,
    #     widget=widgets.RadioSelect
    # )

    # dictator_reasons = models.StringField(initial='',blank=True,
    #     label='Чем Вы руководствовались, определяя сумму, которую Вы передали участнику Б?',
    # )
    year_of_birth = models.IntegerField(
        label='В каком году Вы родились?',
        min=1900,
        max=2022,
        # initial=1999,
        # blank=True
    )
    female = models.StringField(
        label='Пожалуйста, укажите Ваш пол.',
        choices=C.Q_GENDER,
        widget=widgets.RadioSelectHorizontal,
        # initial=1,
        # blank=True
    )
    financial_conditions = models.IntegerField(
        label='Пожалуйста, выберите вариант ответа, который наиболее точно описывает финансовое положение Вашей семьи, не залезая в долги и не беря кредитов.',
        choices=C.Q_FINANCIAL_CONDITIONS,
        widget=widgets.RadioSelect,
        # initial=1,
    )

    education = models.StringField(
        label='Укажите наивысшую оконченную ступень образования, по которой Вы имеете диплом.',
        choices=C.Q_EDUCATION,
        widget=widgets.RadioSelect,
    )
    marriage = models.StringField(
        label='Вы состоите в браке?',
        choices=C.Q_MARRIAGE,
        widget=widgets.RadioSelect,
    )
    children = models.IntegerField(
        label='Сколько у Вас детей?',
        min=0,
    )

    # q related to inequality
    inequality_problem = models.StringField(
        label='Как Вы думаете, неравенство — серьезная проблема в России?',
        choices=C.Q_INEQUALITY_PROBLEM,
        widget=widgets.RadioSelect,
    )
    income_inequality_increasing = models.StringField(
        label='Как Вы считаете, неравенство доходов возросло или снизилось в последние годы в России?',
        choices=C.Q_INCOME_INCREASING,
        widget=widgets.RadioSelect,
    )
    income_satisfactory = models.StringField(
        label='Довольны ли Вы своим заработком?',
        choices=C.Q_4_YES_NO,
        widget=widgets.RadioSelectHorizontal,
    )
    income_deserving = models.StringField(
        label='Как Вы считаете, всегда ли люди с высоким доходом заслуживают такой уровень дохода?',
        choices=C.Q_4_YES_NO,
        widget=widgets.RadioSelectHorizontal,
    )
    income_comp_parents = models.StringField(
        label='По сравнению с уровнем жизни Ваших родителей, когда они были в Вашем возрасте, '
              'Вы живете сейчас лучше, хуже или примерно также?',
        choices=[
            [1, 'Лучше'],
            [2, 'Примерно так же'],
            [3, 'Хуже']
        ],
        widget=widgets.RadioSelectHorizontal,
    )
    unemployment_100 = models.IntegerField(
        label='Как Вы думаете, сколько человек из каждых 100 жителей России на данный момент не имеет '
              'работы и ищет её?',
        min=0,
        max=100)

    high_position_family = high_position('родиться в обеспеченной семье?')
    high_position_education = high_position('получить хорошее образование?')
    high_position_work = high_position('упорно работать?')
    high_position_networking = high_position('знать нужных людей?')
    high_position_social_elevators = high_position('иметь в стране развитые социальные лифты?')

    # economic redistribution
    redistr_changes = models.StringField(
        label='Хотели бы Вы изменить систему перераспределения в России?',
        choices=[
            [1, 'Уменьшить перераспределение'],
            [2, 'Оставить без изменений'],
            [3, 'Увеличить перераспределение']
        ],
        widget=widgets.RadioSelect,
    )
    redistr_benefits_now = models.StringField(
        label='В этом году',
        choices=C.Q_BENEFITS,
        widget=widgets.RadioSelect,
    )
    redistr_benefits_life = models.StringField(
        label='В течение жизни',
        choices=C.Q_BENEFITS,
        widget=widgets.RadioSelect,
    )
    redistr_tax_rate = models.StringField(
        label='Хотели бы вы изменить налоговую ставку в России?',
        choices=[
            [1, 'Уменьшить налоговую ставку'],
            [2, 'Оставить без изменений'],
            [3, 'Увеличить налоговую ставку']
        ],
        widget=widgets.RadioSelect,
    )

    # perception of inequality
    russian_pyramid = models.StringField(
        label='Как Вы считаете, какая диаграмма лучше всего описывает современное российское '
              'общество?',
        choices=C.Q_PYRAMIDS,
        widget=widgets.RadioSelectHorizontal,
    )

    ideal_pyramid = models.StringField(
        label='Какой тип общества Вы бы предпочли?',
        choices=C.Q_PYRAMIDS,
        widget=widgets.RadioSelectHorizontal,
    )

    median_income = models.IntegerField(
        label='Как вы думаете, сколько составляет медианный ежемесячный доход в России? Укажите ответ в рублях.',
        min=0,
    )

    poor_10 = models.IntegerField(
        label='Как Вы думаете, какой средний ежемесячный доход у 10% самых бедных жителей России? '
              'Укажите ответ в рублях.',
        min=0,
    )

    rich_10 = models.IntegerField(
        label='Как Вы думаете, какой средний ежемесячный доход у 10% самых богатых жителей России? '
              'Укажите ответ в рублях.',
        min=0,
    )

    percent_below = models.IntegerField(
        label='Как Вы думаете, какой процент людей в России зарабатывает меньше, чем Вы?',
        min=0, max=100,
    )
    income = models.IntegerField(
        label='Сколько в среднем ежемесячно Вы зарабатываете? Укажите ответ в рублях.',
        min=0,
        blank=True
    )

    # political preferences
    general_trust = models.IntegerField(
        label='Как Вы считаете, в целом большинству людей можно доверять, или же при общении с другими '
              'людьми осторожность никогда не повредит?',
        choices=C.Q_TRUST,
        widget=widgets.RadioSelect,
    )
    trust_country = scale('Государству в целом')
    trust_political_parties = scale('Политическим партиям')
    trust_government = scale('Правительству')
    trust_courts = scale('Судам и судебной системе')
    trust_television = scale('Телевидению')
    trust_mass_media = scale('Новостным средствам массовой информации')

    trust_family = scale('Вашей семье')
    trust_neighbours = scale('Вашим соседям')
    trust_acquant = scale('Людям, с которыми Вы лично знакомы')
    trust_stranger = scale('Людям, с которыми Вы не знакомы')

    social_mobility = scale('Как Вы считаете, насколько хорошо работают социальные лифты в России?')
    politics_interest = scale('Можете ли Вы описать себя как человека, который интересуется политикой? ')

    effort_luck = scale('')
    responsibility = scale('')
    income_equality = scale('')
    competition = scale('')
    left_right = scale('')

    # party_vote = models.StringField(
    #     label='За какую партию Вы голосовали на выборах в Государственную думу, если бы они состоялись сегодня?',
    #     choices=C.Q_PARTY,
    #     widget=widgets.RadioSelect,
    # )
    # corruption = scale('В какую точку Вы поместили бы Россию на этой шкале?')

    democracy_redistribution = scale('Правительство берет налоги с богатых для поддержки бедных')
    democracy_elections = scale('Люди выбирают политических лидеров на свободных выборах')
    democracy_unemployment_allowance = scale('Безработные получают государственное пособие')
    democracy_income_equality = scale('Государство обеспечивает равенство доходов')
    democracy_order = scale('Люди подчиняются властям')
    democracy_gender_equality = scale('У мужчин и женщин равные права')

    important_democracy = scale('Насколько для Вас важно жить в демократической стране?')
    Russia_democracy = scale('Как Вы считаете, насколько демократично управляется Россия в настоящее время?')

    # background
    religion = models.StringField(
        label='Какую религию Вы исповедуете?',
        choices=C.Q_RELIGION,
        widget=widgets.RadioSelect,
    )
    church_attendance = models.StringField(
        label='Как часто Вы посещаете храм?',
        choices=C.Q_CHURCH_ATTENDANCE,
        widget=widgets.RadioSelect,
    )
    mother_education = models.StringField(
        label='Пожалуйста, укажите наивысшую оконченную ступень образования Вашей матери.',
        choices=C.Q_EDUCATION,
        widget=widgets.RadioSelect,
    )
    father_education = models.StringField(
        label='Пожалуйста, укажите наивысшую оконченную ступень образования Вашего отца.',
        choices=C.Q_EDUCATION,
        widget=widgets.RadioSelect,
    )
    region = models.StringField(
        label='Укажите регион Вашего фактического места жительства',
        choices=C.Q_REGIONS,
    )
    regional_income = models.IntegerField(
        label='Как Вы считаете, каков среднемесячный доход жителей Вашего региона? Напишите, пожалуйста, Вашу оценку (в рублях в месяц)',
    )
    place_living_now = models.StringField(
        label='Какая из указанных категорий населенных пунктов соответствует тому пункту, в котором Вы '
              'сейчас '
              'проживаете?',
        choices=C.Q_PLACE_LIVING,
        widget=widgets.RadioSelect,
    )
    place_living_sensible_years = models.StringField(
        label='Какая из указанных категорий населенных пунктов соответствует тому пункту, где Вы проживали в '
              'возрасте 16 лет?',
        choices=C.Q_PLACE_LIVING,
        widget=widgets.RadioSelect,
    )
    is_occupied = models.BooleanField(label="В настоящее время вы трудоустроены?",
                                      widget=widgets.RadioSelectHorizontal,
                                      )
    self_employed = models.BooleanField(label="Являетесь ли вы в настоящее время самозанятым?",
                                        widget=widgets.RadioSelectHorizontal
                                        )

    occupation = models.StringField(
        label='Пожалуйста, укажите к какой сфере относится Ваша деятельность.',
        choices=C.Q_OCCUPATION_PARENT_CHOICES,
        widget=widgets.RadioSelect,
    )
    charity = models.StringField(
        label='Жертвовали ли Вы за последний год деньги на благотворительность '
              'или участвовали волонтером в некоммерческих организациях?',
        choices=C.Q_CHARITY,
        widget=widgets.RadioSelect,
    )
    # big5
    big5_1 = big5(label='сдержанный человек')
    big5_2 = big5(label='в целом доверчивый человек')
    big5_3 = big5(label='склонны к лени')
    big5_4 = big5(label='расслаблены и способны справляться со стрессом')
    big5_5 = big5(label='имеете немного интересов')
    big5_6 = big5(label='общительны')
    big5_7 = big5(label='склонны выискивать чужие ошибки')
    big5_8 = big5(label='тщательно выполняете работу')
    big5_9 = big5(label='легко нервничаете')
    big5_10 = big5(label='имеете богатое воображение')

    big5_extraversion = models.FloatField()
    big5_agreeableness = models.FloatField()
    big5_conscientiousness = models.FloatField()
    big5_neuroticism = models.FloatField()
    big5_openness = models.FloatField()

    # justified
    just_allowance = scale('Получение государственных пособий, на которые человек не имеет права ')
    just_freeride = scale('Проезд без оплаты в общественном транспорте')
    just_thieving = scale('Кража чужой собственности')
    just_tax_evasion = scale('Неуплата налогов, если есть такая возможность')
    just_bribe = scale('Получение взятки, используя служебное положение')
    just_violence = scale('Насилие против других людей ')
    just_political_violence = scale('Использование насилия в политической борьбе ')

    #risk
    risk_general = scale('Насколько Вы любите рисковать в целом?')
    risk_finance = scale('В финансовых вопросах')
    risk_sport = scale('В свободное время и во время занятий спортом')
    risk_profession = scale('В вашей профессии')
    risk_health = scale('В том, что касается вашего здоровья')
    risk_strangers = scale('В отношениях с незнакомыми людьми')
    risk_drive = scale('Во время езды за рулем')


    # personal
    freedom_choice = scale('')
    life_satisfaction = scale('')
    finance_satisfaction = scale('')


# PAGES
class Demographics(Page):
    form_model = 'player'
    form_fields = ['year_of_birth',
                   'female',
                   'education',
                   'marriage',
                   'children',
                   'financial_conditions',
                   ]


class InequalityAssessment(Page):
    form_model = 'player'
    form_fields = ['inequality_problem',
                   'income_inequality_increasing',
                   'income_satisfactory',
                   'income_deserving',
                   'income_comp_parents',
                   'unemployment_100',

                   'high_position_family',
                   'high_position_education',
                   'high_position_work',
                   'high_position_networking',
                   'high_position_social_elevators',
                   ]


class Perception(Page):
    form_model = 'player'
    form_fields = ['russian_pyramid',
                   'ideal_pyramid',
                   'median_income',
                   'poor_10',
                   'rich_10',
                   'percent_below',
                   # 'income'
                   ]


class Redistribution(Page):
    form_model = 'player'
    form_fields = [
        'redistr_changes',
        'redistr_benefits_now',
        'redistr_benefits_life',
        'redistr_tax_rate'
    ]


class PoliticalPreferences(Page):
    form_model = 'player'
    form_fields = [
        'general_trust',
        'trust_country',
        'trust_political_parties',
        'trust_government',
        'trust_courts',
        'trust_television',
        'trust_mass_media',

        'trust_family',
        'trust_neighbours',
        'trust_acquant',
        'trust_stranger',

        'social_mobility',
        'politics_interest',

        'effort_luck',
        'responsibility',
        'income_equality',
        'competition',
        'left_right',
        # 'party_vote',
        # 'corruption',

        'democracy_redistribution',
        'democracy_elections',
        'democracy_unemployment_allowance',
        'democracy_income_equality',
        'democracy_order',
        'democracy_gender_equality',

        'important_democracy',
        # 'Russia_democracy',
    ]


class Big5(Page):
    form_model = 'player'
    form_fields = ['big5_1',
                   'big5_2',
                   'big5_3',
                   'big5_4',
                   'big5_5',
                   'big5_6',
                   'big5_7',
                   'big5_8',
                   'big5_9',
                   'big5_10',

                   'just_allowance',
                   'just_freeride',
                   'just_thieving',
                   'just_tax_evasion',
                   'just_bribe',
                   'just_violence',
                   'just_political_violence',
                   'freedom_choice',
                   'life_satisfaction',
                   'finance_satisfaction'
                   ]

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        player.big5_extraversion = big5_calculation(player.big5_6, player.big5_1)
        player.big5_agreeableness = big5_calculation(player.big5_2, player.big5_7)
        player.big5_conscientiousness = big5_calculation(player.big5_8, player.big5_3)
        player.big5_neuroticism = big5_calculation(player.big5_9, player.big5_4)
        player.big5_openness = big5_calculation(player.big5_10, player.big5_5)


class Risk(Page):
    form_model = 'player'
    form_fields = [
        'risk_general',
        'risk_finance',
        'risk_sport',
        'risk_profession',
        'risk_health',
        'risk_strangers',
        'risk_drive',
    ]


class BackgroundInfo(Page):
    form_model = 'player'
    form_fields = [
        'religion',
        'church_attendance',
        'mother_education',
        'father_education',
        'region',
        'regional_income',
        'place_living_now',
        'place_living_sensible_years',
        'is_occupied',
        'self_employed',
        'occupation',
        'charity'
    ]


class LastQ(Page):
    pass


class TheEnd(Page):
    pass


page_sequence = [
    # WP1,
    # Detection,
    # DetectionAvoid,
    # WP2,
    # Receiver_main_decision,
    # MainDictatorDecision,
    # ResultsWaitPage,
    ### questionnaire
    Demographics,
    InequalityAssessment,
    Perception,
    Redistribution,
    PoliticalPreferences,
    Big5,
    Risk,
    BackgroundInfo,
    # Design_fairness,
    ### the end of questionnaire
    TheEnd
]
