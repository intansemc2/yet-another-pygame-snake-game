from enum import Enum, auto
from pygame.math import Vector2


class POINT_DIRECTION(Enum):
    NONE = auto()

    UP = auto()
    RIGHT = auto()
    DOWN = auto()
    LEFT = auto()


def point_direction(source: Vector2, other: Vector2):
    if source.y == other.y:
        if source.x < other.x:
            return POINT_DIRECTION.RIGHT
        elif source.x > other.x:
            return POINT_DIRECTION.LEFT
    elif source.x == other.x:
        if source.y < other.y:
            return POINT_DIRECTION.DOWN
        elif source.y > other.y:
            return POINT_DIRECTION.UP
    return POINT_DIRECTION.NONE


def head_direction(snake_body: list):
    head_block = snake_body[-1]
    near_head_block = snake_body[-2]

    if point_direction(head_block, near_head_block) == POINT_DIRECTION.RIGHT:
        return 'head_left'
    if point_direction(head_block, near_head_block) == POINT_DIRECTION.LEFT:
        return 'head_right'
    if point_direction(head_block, near_head_block) == POINT_DIRECTION.DOWN:
        return 'head_up'
    return 'head_down'


def tail_direction(snake_body: list):
    tail_block = snake_body[0]
    near_tail_block = snake_body[1]

    if point_direction(tail_block, near_tail_block) == POINT_DIRECTION.RIGHT:
        return 'tail_left'
    if point_direction(tail_block, near_tail_block) == POINT_DIRECTION.LEFT:
        return 'tail_right'
    if point_direction(tail_block, near_tail_block) == POINT_DIRECTION.DOWN:
        return 'tail_up'
    return 'tail_down'


def body_direction(snake_body: list, block_index: int):
    current_block = snake_body[block_index]
    previous_block = snake_body[block_index - 1]
    next_block = snake_body[block_index + 1]

    previous_dir = point_direction(current_block, previous_block)
    next_dir = point_direction(current_block, next_block)

    if previous_dir == POINT_DIRECTION.LEFT and next_dir == POINT_DIRECTION.DOWN or \
            previous_dir == POINT_DIRECTION.DOWN and next_dir == POINT_DIRECTION.LEFT:
        return 'body_bl'

    if previous_dir == POINT_DIRECTION.RIGHT and next_dir == POINT_DIRECTION.DOWN or \
            previous_dir == POINT_DIRECTION.DOWN and next_dir == POINT_DIRECTION.RIGHT:
        return 'body_br'

    if previous_dir == POINT_DIRECTION.LEFT and next_dir == POINT_DIRECTION.RIGHT or \
            previous_dir == POINT_DIRECTION.RIGHT and next_dir == POINT_DIRECTION.LEFT:
        return 'body_horizontal'

    if previous_dir == POINT_DIRECTION.LEFT and next_dir == POINT_DIRECTION.UP or \
            previous_dir == POINT_DIRECTION.UP and next_dir == POINT_DIRECTION.LEFT:
        return 'body_tl'

    if previous_dir == POINT_DIRECTION.RIGHT and next_dir == POINT_DIRECTION.UP or \
            previous_dir == POINT_DIRECTION.UP and next_dir == POINT_DIRECTION.RIGHT:
        return 'body_tr'

    if previous_dir == POINT_DIRECTION.UP and next_dir == POINT_DIRECTION.DOWN or \
            previous_dir == POINT_DIRECTION.DOWN and next_dir == POINT_DIRECTION.UP:
        return 'body_vertical'

    return 'body_vertical'
