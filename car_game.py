import pygame
from pygame.locals import *
from pygame import sprite
import random

pygame.init()

# Create a window
width = 500 
height = 500
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Rele's Drive")

# Colors
gray = (100, 100, 100)
green = (76, 208, 56)
red = (200, 0, 0)
white = (255, 255, 255)
yellow = (255, 232, 0)

# Game settings 
gameover = False
speed = 2
score = 0

# Road and edge markers
road = (100, 0, 300, height)
left_edge_marker = (95, 0, 10, height)
right_edge_marker = (395, 0, 10, height)

# Lane positions
left_lane = 150
center_lane = 250
right_lane = 350
lanes = [left_lane, center_lane, right_lane]

# Lane marker animation
lane_marker_move_y = 0

# Crashing image
crash_image = pygame.image.load('images/crash.png')

class Vehicle(pygame.sprite.Sprite):
    def __init__(self, image, x, y):
        super().__init__()
        image_scale = 45 / image.get_rect().width
        new_width = int(image.get_rect().width * image_scale)
        new_height = int(image.get_rect().height * image_scale)
        self.image = pygame.transform.scale(image, (new_width, new_height))
        self.rect = self.image.get_rect(center=(x, y))

class PlayerVehicle(Vehicle):
    def __init__(self, x, y):
        image = pygame.image.load('images/car.png')
        super().__init__(image, x, y)

# Player's car setup
player = PlayerVehicle(250, 400)
player_group = pygame.sprite.GroupSingle(player)

# Loading enemy vehicle images
image_filenames = ['pickup_truck.png', 'semi_trailer.png', 'taxi.png', 'van.png']
vehicle_images = [pygame.image.load(f'images/{img}') for img in image_filenames]

# Vehicle group
vehicle_group = pygame.sprite.Group()

# Game loop
clock = pygame.time.Clock()
fps = 120
running = True

while running:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

        if event.type == KEYDOWN:
            if event.key == K_LEFT and player.rect.centerx > left_lane:
                player.rect.x -= 100
            elif event.key == K_RIGHT and player.rect.centerx < right_lane:
                player.rect.x += 100

    # Draw background
    screen.fill(green)
    pygame.draw.rect(screen, gray, road)
    pygame.draw.rect(screen, yellow, left_edge_marker)
    pygame.draw.rect(screen, yellow, right_edge_marker)

    # Draw lane markers
    lane_marker_move_y += speed * 2
    if lane_marker_move_y >= 100:
        lane_marker_move_y = 0
    for y in range(-100, height, 100):
        pygame.draw.rect(screen, white, (left_lane + 45, y + lane_marker_move_y, 10, 50))
        pygame.draw.rect(screen, white, (center_lane + 45, y + lane_marker_move_y, 10, 50))

    # Add vehicles
    if len(vehicle_group) < 2:
        add_vehicle = all(v.rect.top > v.rect.height * 1.5 for v in vehicle_group)
        if add_vehicle:
            lane = random.choice(lanes)
            image = random.choice(vehicle_images)
            vehicle = Vehicle(image, lane, -100)
            vehicle_group.add(vehicle)

    # vehicles Movement
    for vehicle in vehicle_group:
        vehicle.rect.y += speed
        if vehicle.rect.top >= height:
            vehicle.kill()
            score += 1
            if score % 5 == 0:
                speed += 1

    # Collision detection
    if pygame.sprite.spritecollide(player, vehicle_group, False):
        screen.blit(crash_image, (width // 2 - 50, height // 2 - 50))
        pygame.display.update()
        pygame.time.delay(2000)
        running = False

    # Draw sprites
    player_group.draw(screen)
    vehicle_group.draw(screen)

    # Score Display
    font = pygame.font.Font(None, 24)
    text = font.render(f'Score: {score}', True, white)
    screen.blit(text, (20, 450))

    pygame.display.update()

pygame.quit()
