import pygame
import pygame as p
import random


white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
p.init()

screen = p.display.set_mode((500, 500))
pygame.display.set_caption('Snake Game')
clock = p.time.Clock()


class Food:
    def __init__(self):
        self.x_val = random.randint(0, 24) * 20
        self.y_val = random.randint(0, 24) * 20

    def get_pos(self):
        return self.x_val, self.y_val

    def render_food(self):
        p.draw.rect(screen, red, [self.x_val, self.y_val, 20, 20])


class Snake:
    def __init__(self):
        _x = random.randint(0, 24) * 20
        _y = random.randint(0, 24) * 20
        self.body = [(_x, _y)]
        self.head = self.body[0]

    def move(self, new_x, new_y):
        self.body.insert(0, (new_x, new_y))
        self.head = self.body[0]

    def collision_detection(self):
        return True if self.head in self.body[1:] else False

    def food_collision(self, food: Food):
        return self.head == food.get_pos()

    def render(self):
        for block in self.body:
            p.draw.rect(screen, black, [block[0], block[1], 20, 20])

    def remove_last(self):
        self.body.pop()

    def in_bounds(self):
        return (0 <= self.head[0] <= 480) and (0 <= self.head[1] <= 480)


def is_valid_turn(intended_turn: str, prev_turn: str) -> bool:
    opposites = {'left': 'right', 'up': 'down', 'down': 'up', 'right': 'left'}
    try:
        if (intended_turn != prev_turn) and (intended_turn !=
                                             opposites[prev_turn]):
            return True
        else:
            return False

    except KeyError:
        return True


game_on = True
last_turn = ''

bob = Snake()
f1 = Food()

x1, y1 = bob.head
x_change = 0
y_change = 0

while game_on:
    for event in p.event.get():
        if event.type == p.QUIT:
            game_on = False
        if event.type == p.KEYDOWN:
            if event.key == p.K_LEFT and is_valid_turn('left', last_turn):
                x_change -= 20
                y_change = 0
                last_turn = 'left'
            elif event.key == p.K_RIGHT and is_valid_turn('right', last_turn):
                x_change += 20
                y_change = 0
                last_turn = 'right'
            elif event.key == p.K_DOWN and is_valid_turn('down', last_turn):
                x_change = 0
                y_change += 20
                last_turn = 'down'
            elif event.key == p.K_UP and is_valid_turn('up', last_turn):
                x_change = 0
                y_change -= 20
                last_turn = 'up'

    x1 += x_change
    y1 += y_change

    screen.fill(white)
    bob.move(x1, y1)

    if not bob.food_collision(f1):
        bob.remove_last()
    elif bob.food_collision(f1):
        f1 = Food()

    if bob.collision_detection():
        game_on = False
    if not bob.in_bounds():
        game_on = False

    bob.render()
    f1.render_food()
    pygame.display.update()
    clock.tick(10)

pygame.quit()
quit()


