import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

GREEN = (34, 139, 34)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

clock = pygame.time.Clock()
SNAKE_SPEED = 5


class Snake:

    def __init__(self):
        self.reset()

    def reset(self):
        self.size = 1
        self.body = [[WIDTH // 2, HEIGHT // 2]]
        self.direction = pygame.K_RIGHT
        self.change_to = self.direction

    def move(self):

        if self.change_to == pygame.K_LEFT and not self.direction == pygame.K_RIGHT:
            self.direction = self.change_to
        if self.change_to == pygame.K_RIGHT and not self.direction == pygame.K_LEFT:
            self.direction = self.change_to
        if self.change_to == pygame.K_UP and not self.direction == pygame.K_DOWN:
            self.direction = self.change_to
        if self.change_to == pygame.K_DOWN and not self.direction == pygame.K_UP:
            self.direction = self.change_to

        head = self.body[0].copy()

        if self.direction == pygame.K_LEFT:
            head[0] -= 20
        elif self.direction == pygame.K_RIGHT:
            head[0] += 20
        elif self.direction == pygame.K_UP:
            head[1] -= 20
        elif self.direction == pygame.K_DOWN:
            head[1] += 20

        self.body.insert(0, head)
        if len(self.body) > self.size:
            self.body.pop()

    def grow(self):
        self.size *= 2

    def draw(self, window):
        for segment in self.body:
            pygame.draw.rect(window, BLUE, (*segment, 20, 20))

    def check_collision_with_self(self):

        return self.body[0] in self.body[1:]

    def check_collision_with_walls(self):
        head = self.body[0]
        return head[0] < 0 or head[0] >= WIDTH or head[1] < 0 or head[
            1] >= HEIGHT


class Apple:

    def __init__(self):
        self.position = self.spawn_apple()

    def spawn_apple(self):
        return [
            random.randint(0, (WIDTH // 20) - 1) * 20,
            random.randint(0, (HEIGHT // 20) - 1) * 20
        ]

    def draw(self, window):
        pygame.draw.rect(window, RED, (*self.position, 20, 20))



snake = Snake()
apples = [Apple()]

APPLE_SPAWN_INTERVAL = 10
last_apple_spawn_time = time.time()

run = True
while run:
    clock.tick(SNAKE_SPEED)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        elif event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP,
                             pygame.K_DOWN):
                snake.change_to = event.key

    snake.move()

    for apple in apples:
        if snake.body[0] == apple.position:
            snake.grow()
            apples.remove(apple)

    if snake.check_collision_with_self() or snake.check_collision_with_walls():
        snake.reset()
        apples = [Apple()]

    current_time = time.time()
    if current_time - last_apple_spawn_time > APPLE_SPAWN_INTERVAL:
        apples.append(Apple())
        last_apple_spawn_time = current_time

    window.fill(GREEN)

    snake.draw(window)
    for apple in apples:
        apple.draw(window)

    pygame.display.update()

pygame.quit()