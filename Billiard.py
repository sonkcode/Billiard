import pygame
import random

# инициализируем Pygame
pygame.init()
# устанавливаем размеры окна
WIDTH = 800
HEIGHT = 600

# работаем с цветами
WHITE = (255, 255, 255)
GREEN = (0, 85, 36)
BROWN = (139, 69, 19)
BLACK = (0, 0, 0)

# создаём окно
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Billiard for Sergey Kudelya. Created by Art.Pro")

# создание шаров vx, vy - регулирует скорость
balls = []
for i in range(7):
    ball = {
        "x": random.randint(50, WIDTH - 50),
        "y": random.randint(50, HEIGHT - 50),
        "r": 20,
        "color": WHITE,
        "vx": 0.2,
        "vy": 0.2
    }
    balls.append(ball)
pockets = [
    {"x": 0, "y": 0},
    {"x": WIDTH / 2, "y": 0},
    {"x": WIDTH, "y": 0},
    {"x": 0, "y": HEIGHT},
    {"x": WIDTH / 2, "y": HEIGHT},
    {"x": WIDTH, "y": HEIGHT},
]

# создание изображений шаров
ball_images = []
for i in range(1, 8):
    img = pygame.image.load(f"ball{i}.png")
    ball_images.append(pygame.transform.scale(img, (80, 80)))

# основной игровой цикл
running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # движение шаров
    for ball in balls:
        # столкновение со стенами
        if ball["x"] - ball["r"] < 0 or ball["x"] + ball["r"] > WIDTH:
            ball["vx"] = -ball["vx"]
        if ball["y"] - ball["r"] < 0 or ball["y"] + ball["r"] > HEIGHT:
            ball["vy"] = -ball["vy"]
        # движение
        ball["x"] += ball["vx"]
        ball["y"] += ball["vy"]

        # проверка столкновения с лузами
        for pocket in pockets:
            distance = ((ball["x"] - pocket["x"]) ** 2 + (ball["y"] - pocket["y"]) ** 2) ** 0.5
            if distance < ball["r"]:
                balls.remove(ball)
                break
        # чистим экран
    screen.fill(GREEN)

    for i, ball in enumerate(balls):
        ball_surface = ball_images[i]
        ball_rect = ball_surface.get_rect(center=(int(ball["x"]), int(ball["y"])))
        screen.blit(ball_surface, ball_rect)
    for pocket in pockets:
        pygame.draw.circle(screen, BROWN, (int(pocket["x"]), int(pocket["y"])), 30)
    pygame.display.flip()

pygame.quit()