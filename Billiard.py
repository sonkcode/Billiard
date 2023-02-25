import sys

import pygame
import random

pygame.init()

WIDTH = 800
HEIGHT = 600

WHITE = (255, 255, 255)
GREEN = (0, 85, 36)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Billiard for Sergey Kudelya. Created by Art.Pro")

class Ball:
    def __init__(self, x, y, r, color, vx, vy, image):
        self.x = x
        self.y = y
        self.r = r
        self.color = color
        self.vx = vx
        self.vy = vy
        self.image = image

    def draw(self, screen):
        ball_rect = self.image.get_rect(center=(int(self.x), int(self.y)))
        screen.blit(self.image, ball_rect)

    def move(self):
        self.x += self.vx
        self.y += self.vy

    def check_walls_collision(self):
        if self.x - self.r < 0 or self.x + self.r > WIDTH:
            self.vx = -self.vx
        if self.y - self.r < 0 or self.y + self.r > HEIGHT:
            self.vy = -self.vy

    def check_ball_collision(self, other_ball):
        distance = ((self.x - other_ball.x) ** 2 + (self.y - other_ball.y) ** 2) ** 0.5
        if distance < self.r + other_ball.r:
            self.vx, other_ball.vx = other_ball.vx, self.vx
            self.vy, other_ball.vy = other_ball.vy, self.vy

    def check_pockets_collision(self, pockets):
        for pocket in pockets:
            distance = ((self.x - pocket.x) ** 2 + (self.y - pocket.y) ** 2) ** 0.5
            if distance < self.r:
                return True
        return False

class Pocket:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.circle(screen, BROWN, (int(self.x), int(self.y)), 30)

class Table:
    def __init__(self):
        self.balls = []
        self.pockets = []
        self.ball_images = []
        for i in range(7):
            x = random.randint(50, WIDTH - 50)
            y = random.randint(50, HEIGHT - 50)
            ball_image = pygame.image.load(f"ball{i+1}.png")
            ball_image = pygame.transform.scale(ball_image, (80, 80))
            ball = Ball(x, y, 10, WHITE, 4.7, 4.7, ball_image)
            self.balls.append(ball)
            self.ball_images.append(ball_image)

        for pocket_x, pocket_y in [(0, 0), (WIDTH / 2, 0), (WIDTH, 0), (0, HEIGHT), (WIDTH / 2, HEIGHT), (WIDTH, HEIGHT)]:
            pocket = Pocket(pocket_x, pocket_y)
            self.pockets.append(pocket)

    def run(self, screen):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(GREEN)

            for ball in self.balls:
                ball.move()
                ball.check_walls_collision()

                for other_ball in self.balls:
                    if ball != other_ball:
                        ball.check_ball_collision(other_ball)

                if ball.check_pockets_collision(self.pockets):
                    self.balls.remove(ball)

                ball.draw(screen)

            for pocket in self.pockets:
                pocket.draw(screen)

            pygame.display.flip()
            clock.tick(60)

if __name__ == '__main__':
    table = Table()
    table.run(screen)