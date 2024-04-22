import time
import itertools

from otree import settings
from otree.api import *

from .image_utils import encode_image

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageMorph
import random

doc = """
Your app description
"""
CHARSET = "АБВГДЕЖЗИКЛМНОПРСТУФХЦЧШЩЫЭЮЯ"
# LENGTH = 3
TEXT_SIZE = 32
TEXT_PADDING = TEXT_SIZE
TEXT_FONT = Path(__file__).parent / "assets" / "FreeSansBold.otf"

INPUT_TYPE = "text"
INPUT_HINT = "Перепишите текст с картинки"


def generate_puzzle_fields(hard_treatment):
    if hard_treatment == 1:
        LENGTH = 10
    else:
        LENGTH = 5
    text = "".join((random.choice(CHARSET) for _ in range(LENGTH)))
    return dict(text=text, solution=text)


def other_player(player):
    return player.get_others_in_group()[0]


def is_correct(response, puzzle):
    return puzzle.solution.lower() == response.lower()


def render_image(puzzle):
    text = puzzle.text
    dumb = Image.new("RGB", (0, 0))
    font = ImageFont.truetype(str(TEXT_FONT), TEXT_SIZE)
    w, h = ImageDraw.ImageDraw(dumb).textsize(text, font)
    image = Image.new("RGB", (w + TEXT_PADDING * 2, h + TEXT_PADDING * 2))
    draw = ImageDraw.Draw(image)
    draw.text((TEXT_PADDING, TEXT_PADDING), text, font=font)

    # distort
    img = image.convert("L")
    distortions = [
        ImageMorph.MorphOp(op_name="erosion4"),
        ImageMorph.MorphOp(op_name="dilation4"),
    ]
    for op in distortions:
        _, img = op.apply(img)
    return img


class C(BaseConstants):
    NAME_IN_URL = 'RealEffortTasks'
    PLAYERS_PER_GROUP = None
    NUM_ROUNDS = 1


class Subsession(BaseSubsession):
    pass


def creating_session(subsession: Subsession):
    session = subsession.session
    defaults = dict(
        retry_delay=1.0, puzzle_delay=1.0, attempts_per_puzzle=1, max_iterations=None)
    session.params = {}
    for param in defaults:
        session.params[param] = session.config.get(param, defaults[param])

    treatments = itertools.cycle([0, 1])
    for player in subsession.get_players():
        player.hard_treatment = next(treatments)


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    iteration = models.IntegerField(initial=0)
    num_trials = models.IntegerField(initial=0)
    num_correct = models.IntegerField(initial=0)
    num_failed = models.IntegerField(initial=0)

    hard_treatment = models.IntegerField()
    ret_payoff = models.CurrencyField()
    score = models.IntegerField()

    quiz1 = models.IntegerField(label='Сколько минут будет на выполнение задания?')
    quiz2 = models.BooleanField(label='Будете ли Вы знать в группу со сложными или простыми заданиями Вы попали?')
    quiz3 = models.IntegerField(label='Как будет выплачен бонус?',
                                choices=[
                                    [1, 'Случайным образом'],
                                    [2, 'После объединения в пару случайным образом с другим участником тому, '
                                        'кто выполнил больше заданий'],
                                    [3, 'Только тем, кто попали в группу со сложными заданиями']],
                                widget=widgets.RadioSelect)

    num_failed_attempts = models.IntegerField(initial=0)
    failed_too_many = models.BooleanField(initial=False)


    prior_prob_hard = models.IntegerField(min=0, max=100,
                                          label='Как Вы думаете, какова вероятность того, что '
                                                'Вы оказались в группе со сложными заданиями?')
    prior_ppl_lower = models.IntegerField(min=0, max=100,
                                          label='Как Вы думаете, сколько из каждых 100 людей выполнили '
                                                'задание хуже, чем Вы? ')

    prior_deserve_bonus = models.IntegerField(min=0, max=100,
                                              label='Основываясь на Вашем результате, как Вы думаете, насколько Вы заслуживаете бонус?')


class Puzzle(ExtraModel):
    """A model to keep record of all generated puzzles"""

    player = models.Link(Player)
    iteration = models.IntegerField(initial=0)
    attempts = models.IntegerField(initial=0)
    timestamp = models.FloatField(initial=0)
    # can be either simple text, or a json-encoded definition of the puzzle, etc.
    text = models.LongStringField()
    # solution may be the same as text, if it's simply a transcription task
    solution = models.LongStringField()
    response = models.LongStringField()
    response_timestamp = models.FloatField()
    is_correct = models.BooleanField()


def generate_puzzle(player: Player) -> Puzzle:
    """Create new puzzle for a player"""
    fields = generate_puzzle_fields(player.hard_treatment)
    player.iteration += 1
    return Puzzle.create(
        player=player, iteration=player.iteration, timestamp=time.time(), **fields
    )


def get_current_puzzle(player):
    puzzles = Puzzle.filter(player=player, iteration=player.iteration)
    if puzzles:
        [puzzle] = puzzles
        return puzzle


def encode_puzzle(puzzle: Puzzle):
    """Create data describing puzzle to send to client"""
    # generate image for the puzzle
    image = render_image(puzzle)
    data = encode_image(image)
    return dict(image=data)


def get_progress(player: Player):
    """Return current player progress"""
    return dict(
        num_trials=player.num_trials,
        num_correct=player.num_correct,
        num_incorrect=player.num_failed,
        iteration=player.iteration,
    )


def play_game(player: Player, message: dict):
    """Main game workflow
    Implemented as reactive scheme: receive message from vrowser, react, respond.

    Generic game workflow, from server point of view:
    - receive: {'type': 'load'} -- empty message means page loaded
    - check if it's game start or page refresh midgame
    - respond: {'type': 'status', 'progress': ...}
    - respond: {'type': 'status', 'progress': ..., 'puzzle': data} -- in case of midgame page reload

    - receive: {'type': 'next'} -- request for a next/first puzzle
    - generate new puzzle
    - respond: {'type': 'puzzle', 'puzzle': data}

    - receive: {'type': 'answer', 'answer': ...} -- user answered the puzzle
    - check if the answer is correct
    - respond: {'type': 'feedback', 'is_correct': true|false, 'retries_left': ...} -- feedback to the answer

    If allowed by config `attempts_pre_puzzle`, client can send more 'answer' messages
    When done solving, client should explicitely request next puzzle by sending 'next' message

    Field 'progress' is added to all server responses to indicate it on page.

    To indicate max_iteration exhausted in response to 'next' server returns 'status' message with iterations_left=0
    """
    session = player.session
    my_id = player.id_in_group
    params = session.params
    # task_module = get_task_module(player)

    now = time.time()
    # the current puzzle or none
    current = get_current_puzzle(player)

    message_type = message['type']

    # page loaded
    if message_type == 'load':
        p = get_progress(player)
        if current:
            return {
                my_id: dict(type='status', progress=p, puzzle=encode_puzzle(current))
            }
        else:
            return {my_id: dict(type='status', progress=p)}

    if message_type == "cheat" and settings.DEBUG:
        return {my_id: dict(type='solution', solution=current.solution)}

    # client requested new puzzle
    if message_type == "next":
        if current is not None:
            if current.response is None:
                raise RuntimeError("trying to skip over unsolved puzzle")
            if now < current.timestamp + params["puzzle_delay"]:
                raise RuntimeError("retrying too fast")
            if current.iteration == params['max_iterations']:
                return {
                    my_id: dict(
                        type='status', progress=get_progress(player), iterations_left=0
                    )
                }
        # generate new puzzle
        z = generate_puzzle(player)
        p = get_progress(player)
        return {my_id: dict(type='puzzle', puzzle=encode_puzzle(z), progress=p)}

    # client gives an answer to current puzzle
    if message_type == "answer":
        if current is None:
            raise RuntimeError("trying to answer no puzzle")

        if current.response is not None:  # it's a retry
            if current.attempts >= params["attempts_per_puzzle"]:
                raise RuntimeError("no more attempts allowed")
            if now < current.response_timestamp + params["retry_delay"]:
                raise RuntimeError("retrying too fast")

            # undo last updation of player progress
            player.num_trials -= 1
            if current.is_correct:
                player.num_correct -= 1
            else:
                player.num_failed -= 1

        # check answer
        answer = message["answer"]

        if answer == "" or answer is None:
            raise ValueError("bogus answer")

        current.response = answer
        current.is_correct = is_correct(answer, current)
        current.response_timestamp = now
        current.attempts += 1

        # update player progress
        if current.is_correct:
            player.num_correct += 1
        else:
            player.num_failed += 1
        player.num_trials += 1

        retries_left = params["attempts_per_puzzle"] - current.attempts
        p = get_progress(player)
        return {
            my_id: dict(
                type='feedback',
                is_correct=current.is_correct,
                retries_left=retries_left,
                progress=p,
            )
        }

    raise RuntimeError("unrecognized message from client")


# PAGES
class InstructionGeneral(Page):
    pass


# class TaskInstruction(Page):
#     pass


class RET(Page):
    timeout_seconds = 10

    live_method = play_game

    @staticmethod
    def js_vars(player: Player):
        return dict(params=player.session.params)

    @staticmethod
    def vars_for_template(player: Player):
        return dict(DEBUG=settings.DEBUG,
                    input_type=INPUT_TYPE,
                    placeholder=INPUT_HINT
                    )

    @staticmethod
    def before_next_page(player: Player, timeout_happened):
        if not timeout_happened and not player.session.params['max_iterations']:
            raise RuntimeError("malicious page submission")

        participant = player.participant
        participant.score = player.num_correct
        participant.hard_treatment = player.hard_treatment




class Results(Page):
    pass


class RETInstruction(Page):
    pass


class RETQuiz(Page):
    form_model = 'player'
    form_fields = [
        'quiz1',
        'quiz2',
        'quiz3'
    ]

    @staticmethod
    def error_message(player: Player, values):
        solutions = dict(quiz1=2, quiz2=False, quiz3=2)

        errors = {name: 'Неверный ответ' for name in solutions if values[name] != solutions[name]}
        if errors:
            player.num_failed_attempts += 1
            return errors


class PriorBeliefs1(Page):
    form_model = 'player'
    form_fields = [
        'prior_prob_hard'
    ]


class PriorBeliefs2(Page):
    form_model = 'player'
    form_fields = [
        'prior_ppl_lower'
    ]


class PriorBeliefs3(Page):
    form_model = 'player'
    form_fields = [
        'prior_deserve_bonus'
    ]


page_sequence = [InstructionGeneral,
                 RETInstruction,
                 RETQuiz,
                 RET,
                 Results,
                 PriorBeliefs1,
                 PriorBeliefs2,
                 PriorBeliefs3
]
