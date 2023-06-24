import sys
import os
import math
import datetime
import pygame
from pygame.locals import *
import render

pygame.init()

screen = pygame.display.set_mode((500, 500), pygame.RESIZABLE, 32)
display = pygame.Surface((100, 100))
font = pygame.font.Font("fonts/Pixel.ttf", 35)
temp = os.listdir("car")
temp.sort()
images = [pygame.image.load("car/" + img) for img in temp]
clock = pygame.time.Clock()
SCALE_FACTOR = 5
frame = 0


class Object:
    def __init__(self, imgs, x=0, y=0, dir=0):
        self.imgs = imgs
        self.x = x
        self.y = y
        self.dir = dir
        self.dx = 0
        self.dy = 0

    def draw(self):
        imgs = [
            pygame.transform.scale_by(
                pygame.transform.rotate(img, int(self.dir)), SCALE_FACTOR
            )
            for img in self.imgs
        ]
        render.render_stack(
            screen,
            imgs,
            (screen.get_width() / 2, screen.get_height() / 2),
            0,
            spready=5,
        )


class Car:
    def __init__(self, imgs, x=0, y=0, dir=0, speed=10):
        self.imgs = imgs
        self.x = x
        self.y = y
        self.dir = dir
        self.speed = speed
        self.d = 0
        self.tuning = 1
        self.dx = 0
        self.dy = 0
        self.previousd = 0

    def draw(self):
        imgs = [
            pygame.transform.scale_by(
                pygame.transform.rotate(img, int(self.dir)), SCALE_FACTOR
            )
            for img in self.imgs
        ]
        render.render_stack(
            screen,
            imgs,
            (screen.get_width() / 2, screen.get_height() / 2),
            0,
            spready=5,
        )

    def move(self):
        if keys[K_a] and abs(self.d) > 1.5:
            if self.d > 0:
                self.dir += 3
            else:
                self.dir -= 3
        elif keys[K_a]:
            if self.d > 0:
                self.dir += abs(self.d) / 2
            else:
                self.dir -= abs(self.d) / 2
        if keys[K_d] and abs(self.d) > 1.5:
            if self.d > 0:
                self.dir -= 3
            else:
                self.dir += 3
        elif keys[K_d]:
            if self.d > 0:
                self.dir -= abs(self.d) / 2
            else:
                self.dir += abs(self.d) / 2
        if keys[K_w] and self.d <= 7:
            self.d += 0.25
        elif keys[K_s] and self.d >= -4:
            self.d -= 0.15
        elif not keys[K_SPACE]:
            self.d *= 0.99
            if 0.005 >= self.d >= -0.005:
                self.d = 0
        if keys[K_SPACE]:
            if self.d > 0:
                self.d -= 0.15
            else:
                self.d += 0.15
            if 0.005 >= self.d >= -0.005:
                self.d = 0
            if 1 >= self.dx >= -1:
                self.d = 0
            if 1 >= self.dy >= -1:
                self.d = 0
        if keys[K_r]:
            self.x = 0
            self.y = 0
        self.dx += math.sin(math.radians(self.dir)) * self.speed * self.previousd
        self.dy += math.cos(math.radians(self.dir)) * self.speed * self.previousd
        self.dx *= 0.7
        self.dy *= 0.7
        self.dx -= math.sin(math.radians(self.dir)) * self.speed * self.d
        self.dy -= math.cos(math.radians(self.dir)) * self.speed * self.d
        self.x += self.dx
        self.y += self.dy
        self.previousd = self.d


clock = pygame.time.Clock()
car = Car(imgs=images, x=0, y=0, dir=45)
tiles = []
logo = pygame.image.load("logo.png")
logo.set_colorkey((255, 0, 0))
pygame.display.set_icon(logo)
sand = pygame.transform.scale_by(pygame.image.load("tiles/sand.png"), SCALE_FACTOR)
PREFERRED_FPS = 60


def screenshot_path():
    now = datetime.datetime.now()
    return now.strftime("screenshot_%Y-%m-%d_%H:%M:%S.%f.png")


for i in range(20):
    tiles.append([])
    for j in range(20):
        tiles[i].append(sand)
while True:
    clock.tick(60)
    screen.fill((255, 0, 255))
    offset = (screen.get_width() / 2 - car.x, screen.get_height() / 2 - car.y)
    frame += 0.5
    keys = pygame.key.get_pressed()
    takescreenshot = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_F12:
                takescreenshot = True

    if keys[K_ESCAPE]:
        pygame.quit()
        sys.exit()
    for i in range(20):
        for j in range(20):
            screen.blit(sand, (64 * i + offset[0], 64 * j + offset[1]))

    car.draw()
    car.move()
    if takescreenshot:
        pygame.image.save(screen, screenshot_path())
    clock.tick(PREFERRED_FPS)
    fps = clock.get_fps()
    screen.blit(font.render(str(int(fps)), False, (255, 255, 255)), (20, 20))
    pygame.display.update()
