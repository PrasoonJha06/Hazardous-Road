import pygame
from pygame import mixer
import random

print(f"\t-Pygame Community")

print(f"\nThe more distance you cover, the more points you earn.")
print(f"Press Right key to go right.")
print(f"Press Left to go left.")
print(f"Press Up to go faster.")
print(f"Press CTRL to go even faster")

pygame.init()

# Music
mixer.music.load('19th Floor - Bobby Richards.mp3')
mixer.music.play(-1)

# Screen variables
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Hazardous Road")

# Score variables
score = 0
score_increment = 0.001
game_font = pygame.font.SysFont('Segoi UI', 40)

# Road variables
road_surface = pygame.image.load('Road.png').convert()
road_y = 0
road_y_increment = 0.5

# Car variables
car_surface = pygame.image.load('Car.png').convert_alpha()
car_surface = pygame.transform.scale2x(car_surface)
car_rect = car_surface.get_rect(center=(380, 500))
car_x_increment = 0
car_y_increment = 0

# Enemy Car variables
enemy_car_surface = pygame.image.load('Enemy Car.png').convert_alpha()
enemy_car_rect = enemy_car_surface.get_rect(center=(random.randint(200, 400), -300))
enemy_car_y_increment = 1

# Truck variables
truck_surface = pygame.image.load('Truck.png').convert_alpha()
truck_rect = truck_surface.get_rect(center=(random.randint(50, 400), random.randint(-1000, -500)))
truck_y_increment = 1


def fix_car():
    """Making sure the car doesn't move out of the road"""
    if car_rect.right >= 800:
        car_rect.right = 800
    if car_rect.left <= 0:
        car_rect.left = 0


def detect_collision(obstacle):
    """Detecting if the car has collided with any other sprites"""
    global car_y_increment
    if car_rect.colliderect(obstacle):
        mixer.music.stop()
        over_sound = mixer.Sound('Crash.mp3')
        over_sound.play()
        car_y_increment = 1


def redraw_enemy_car():
    """Bringing enemy car back to game once it has gone out of the screen"""
    if enemy_car_rect.bottom >= 750:
        enemy_car_rect.x = random.randint(50, 400)
        enemy_car_rect.y = random.randint(-6000, -600)


def redraw_truck():
    """Bringing truck back to game once it has gone out of the screen"""
    if truck_rect.bottom >= 900:
        truck_rect.x = random.randint(50, 400)
        truck_rect.y = random.randint(-10000, -5000)


def accident():
    """Creating a scene of an accident"""
    global enemy_car_y_increment, truck_y_increment, road_y_increment, score_increment
    if car_rect.y >= 500:
        enemy_car_y_increment = 0
        truck_y_increment = 0
        road_y_increment = 0
        score_increment = 0


def display_score():
    """Displaying the score"""
    score_surface = game_font.render(f'Score: {int(score)}', True, (0, 0, 255))
    score_rect = score_surface.get_rect(center=(screen_width / 2, 50))
    screen.blit(score_surface, score_rect)


active = True
while active:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            active = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                car_x_increment = 1
            if event.key == pygame.K_LEFT:
                car_x_increment = -1
            if event.key == pygame.K_UP:
                road_y_increment = 2
                enemy_car_y_increment = 2.5
                truck_y_increment = 2.5
                score_increment = 0.002
            if event.key == pygame.K_RCTRL:
                road_y_increment = 5
                enemy_car_y_increment = 5.5
                truck_y_increment = 5.5
                score_increment = 0.005
            if event.key == pygame.K_LCTRL:
                road_y_increment = 5
                enemy_car_y_increment = 5.5
                truck_y_increment = 5.5
                score_increment = 0.005
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_RIGHT:
                car_x_increment = 0
            if event.key == pygame.K_LEFT:
                car_x_increment = 0
            if event.key == pygame.K_UP:
                road_y_increment = 0.5
                enemy_car_y_increment = 1
                truck_y_increment = 1
                score_increment = 0.001
            if event.key == pygame.K_RCTRL:
                road_y_increment = 0.5
                enemy_car_y_increment = 1
                truck_y_increment = 1
                score_increment = 0.001
            if event.key == pygame.K_LCTRL:
                road_y_increment = 0.5
                enemy_car_y_increment = 1
                truck_y_increment = 1
                score_increment = 0.001

    # Scoring mechanics
    score += score_increment

    # Movement mechanics of road
    road_y += road_y_increment
    if road_y >= 600:
        road_y = 0

    # Movement mechanics of sprites
    car_rect.x += car_x_increment
    car_rect.y += car_y_increment
    enemy_car_rect.y += enemy_car_y_increment
    truck_rect.y += truck_y_increment

    # Visuals
    screen.fill((124, 252, 0))
    screen.blit(road_surface, (50, road_y))
    screen.blit(road_surface, (50, road_y - 600))
    screen.blit(car_surface, car_rect)
    screen.blit(enemy_car_surface, enemy_car_rect)
    screen.blit(truck_surface, truck_rect)

    # Calling functions
    fix_car()
    detect_collision(enemy_car_rect)
    detect_collision(truck_rect)
    redraw_enemy_car()
    redraw_truck()
    accident()
    display_score()
    pygame.display.update()
