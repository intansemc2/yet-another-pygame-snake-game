import os
import random
import sys
import pygame
from enum import Enum, auto
from pygame.math import Vector2

from utils import body_direction, head_direction, tail_direction


class Fruit:
    def __init__(self) -> None:
        self.pos = Vector2(
            x=random.randint(0, cell_number - 1),
            y=random.randint(0, cell_number - 1),
        )
        self.color = (255, 0, 0)
        self.image = pygame.image.load(os.path.abspath('./graphics/apple.png')).convert_alpha()
        self.image = pygame.transform.scale(self.image, (cell_size, cell_size))

    def draw(self, use_image=False):
        fruit_rect = pygame.Rect(
            int(self.pos.x * cell_size), int(self.pos.y * cell_size),
            cell_size, cell_size
        )

        if use_image:
            screen.blit(self.image, fruit_rect)
        else:
            pygame.draw.rect(screen, self.color, fruit_rect)

    def gen_pos(self, avoid_positions: Vector2):
        while True:
            new_pos = Vector2(
                x=random.randint(0, cell_number - 1),
                y=random.randint(0, cell_number - 1),
            )
            if new_pos in avoid_positions:
                continue

            self.pos = new_pos
            return


class SNAKE_DIRECTION(Enum):
    UP = Vector2(0, -1)
    RIGHT = Vector2(1, 0)
    DOWN = Vector2(0, 1)
    LEFT = Vector2(-1, 0)
    NONE = Vector2(0, 0)


class SNAKE_UPDATE_RESULT(Enum):
    OK = auto()
    DEAD = auto()
    EAT = auto()


class Snake:
    def __init__(self) -> None:
        # snake blocks order: tail, body,... head
        self.body = []
        self.color = (0, 140, 0)
        self.direction = SNAKE_DIRECTION.RIGHT
        self.previous_direction = SNAKE_DIRECTION.RIGHT
        self.reset()

        self.images = {
            'head_up': pygame.image.load(os.path.abspath('./graphics/head_up.png')).convert_alpha(),
            'head_down': pygame.image.load(os.path.abspath('./graphics/head_down.png')).convert_alpha(),
            'head_left': pygame.image.load(os.path.abspath('./graphics/head_left.png')).convert_alpha(),
            'head_right': pygame.image.load(os.path.abspath('./graphics/head_right.png')).convert_alpha(),

            'tail_up': pygame.image.load(os.path.abspath('./graphics/tail_up.png')).convert_alpha(),
            'tail_down': pygame.image.load(os.path.abspath('./graphics/tail_down.png')).convert_alpha(),
            'tail_left': pygame.image.load(os.path.abspath('./graphics/tail_left.png')).convert_alpha(),
            'tail_right': pygame.image.load(os.path.abspath('./graphics/tail_right.png')).convert_alpha(),

            'body_tl': pygame.image.load(os.path.abspath('./graphics/body_tl.png')).convert_alpha(),
            'body_tr': pygame.image.load(os.path.abspath('./graphics/body_tr.png')).convert_alpha(),
            'body_bl': pygame.image.load(os.path.abspath('./graphics/body_bl.png')).convert_alpha(),
            'body_br': pygame.image.load(os.path.abspath('./graphics/body_br.png')).convert_alpha(),
            'body_horizontal': pygame.image.load(os.path.abspath('./graphics/body_horizontal.png')).convert_alpha(),
            'body_vertical': pygame.image.load(os.path.abspath('./graphics/body_vertical.png')).convert_alpha(),
        }
        for key, image in self.images.items():
            self.images[key] = pygame.transform.scale(image, (cell_size, cell_size))

        self.eat_sound = pygame.mixer.Sound(os.path.abspath('./sound/crunch.wav'))

    def reset(self):
        mid_pos = int(cell_number / 2)
        self.body = [
            Vector2(mid_pos-1, mid_pos), Vector2(mid_pos, mid_pos), Vector2(mid_pos+1, mid_pos)
        ]
        self.direction = SNAKE_DIRECTION.NONE
        self.previous_direction = SNAKE_DIRECTION.RIGHT

    def draw(self, use_image=False):
        if use_image:
            # draw head
            snake_rect = pygame.Rect(
                int(self.body[-1].x * cell_size), int(self.body[-1].y * cell_size),
                cell_size, cell_size
            )
            screen.blit(self.images[head_direction(self.body)], snake_rect)

            # draw body
            for i, snake_block in enumerate(self.body[1:-1]):
                snake_rect = pygame.Rect(
                    int(snake_block.x * cell_size), int(snake_block.y * cell_size),
                    cell_size, cell_size
                )
                direction = body_direction(self.body, i + 1)
                screen.blit(self.images[direction], snake_rect)

            # draw tail
            snake_rect = pygame.Rect(
                int(self.body[0].x * cell_size), int(self.body[0].y * cell_size),
                cell_size, cell_size
            )
            screen.blit(self.images[tail_direction(self.body)], snake_rect)
        else:
            for snake_block in self.body:
                snake_rect = pygame.Rect(
                    int(snake_block.x * cell_size), int(snake_block.y * cell_size),
                    cell_size, cell_size
                )
                pygame.draw.rect(screen, self.color, snake_rect)

    def update(self, target_position: Vector2):
        if self.direction == SNAKE_DIRECTION.NONE:
            return SNAKE_UPDATE_RESULT.OK

        self.previous_direction = self.direction
        next_head_position = self.body[-1] + self.direction.value

        if next_head_position.x < 0 or \
                next_head_position.x >= cell_number or \
                next_head_position.y < 0 or \
                next_head_position.y >= cell_number:
            return SNAKE_UPDATE_RESULT.DEAD
        if next_head_position in self.body:
            return SNAKE_UPDATE_RESULT.DEAD

        # if the snake still alive, add new block to the end of the list
        if next_head_position == target_position:
            self.body = [*self.body, target_position]
            self.eat_sound.play()
            return SNAKE_UPDATE_RESULT.EAT

        self.body = [*self.body[1:], next_head_position]
        return SNAKE_UPDATE_RESULT.OK

    def update_direction(self, new_direction: SNAKE_DIRECTION):
        if self.previous_direction.value + new_direction.value == Vector2(0, 0):
            return
        self.direction = new_direction


def draw_grass():
    screen.fill((23, 23, 23))
    for row_index in range(cell_number):
        for col_index in range(cell_number):
            if row_index % 2 == 0 and col_index % 2 == 0 or \
                    row_index % 2 != 0 and col_index % 2 != 0:
                grass_rect = pygame.Rect(
                    int(row_index * cell_size),
                    int(col_index * cell_size),
                    cell_size, cell_size,
                )
                pygame.draw.rect(screen, (26, 26, 26), grass_rect)


def draw_score():
    score_text = str(len(snake.body) - 3)
    score_surface = game_font.render(score_text, True, (255, 255, 255))
    screen.blit(score_surface, (10, 10))


def game_over():
    snake.reset()
    fruit.gen_pos(snake.body)


if __name__ == '__main__':
    pygame.init()
    cell_size = 40
    cell_number = 16

    game_font = pygame.font.Font(os.path.abspath('./font/PoetsenOne-Regular.ttf'), 25)

    screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
    clock = pygame.time.Clock()

    SNAKE_UPDATE = pygame.USEREVENT
    pygame.time.set_timer(SNAKE_UPDATE, 200)

    fruit = Fruit()
    snake = Snake()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == SNAKE_UPDATE:
                update_result = snake.update(fruit.pos)
                if update_result == SNAKE_UPDATE_RESULT.DEAD:
                    game_over()

                if update_result == SNAKE_UPDATE_RESULT.EAT:
                    fruit.gen_pos(snake.body)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP or event.key == pygame.K_w:
                    snake.update_direction(SNAKE_DIRECTION.UP)
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    snake.update_direction(SNAKE_DIRECTION.DOWN)
                elif event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    snake.update_direction(SNAKE_DIRECTION.LEFT)
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    snake.update_direction(SNAKE_DIRECTION.RIGHT)

        draw_grass()

        fruit.draw(True)
        snake.draw(True)

        draw_score()

        pygame.display.update()
        clock.tick(30)
