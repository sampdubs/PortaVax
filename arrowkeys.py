import pygame
from gps import *
from drive import PortaVax

pygame.init()
screen = pygame.display.set_mode((400,400))

if __name__ == "__main__":
    pv = PortaVax(
        (20, 21),
        (6, 5),
        gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE),
        (0, 0),
        None, None, None)
    while True:
        speed = 0
        angle = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            angle += 0.2
        if keys[pygame.K_RIGHT]:
            angle -= 0.2
        if keys[pygame.K_UP]:
            speed += 1
        if keys[pygame.K_DOWN]:
            speed -= 1
        print(speed, angle)
        pv.drive(speed, angle)
