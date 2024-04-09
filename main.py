import pygame
from pygame.locals import *
import math
import random
from lxml import etree
import os

pygame.init()
clock = pygame.time.Clock()

game_width = 900
game_height = 506
game = pygame.display.set_mode((game_width, game_height), pygame.RESIZABLE)
current_size = game.get_size()
virtual_surface = pygame.Surface((game_width, game_height))
background = pygame.image.load(os.getcwd() + "\\background.png").convert_alpha()
hallway = pygame.image.load(os.getcwd() + "\\hallway.png").convert_alpha()
charachter_x = 1296
charachter_y = 216
image = pygame.image.load("C:\\Users\\Михаил.KALINKA\\Downloads\\Punk_run.png")
image = pygame.transform.scale(image, (charachter_x, charachter_y))
class main_charachter:
    charachter_y = 216
    run = pygame.image.load("animations_mp\\run.png")
    run_frame = run.get_width()//run.get_height()
    ch_run = pygame.transform.scale(run, (charachter_y*run_frame, charachter_y))
    r_run = pygame.image.load("animations_mp\\r_run.png")
    r_run_frame = r_run.get_width() // r_run.get_height()
    ch_r_run = pygame.transform.scale(r_run, (charachter_y * r_run_frame, charachter_y))
    idle = pygame.image.load("animations_mp\\idle.png")
    idle_frame = idle.get_width()//idle.get_height()
    ch_idle = pygame.transform.scale(idle, (charachter_y*idle_frame, charachter_y))

a = main_charachter()
running = True
s = 0
bg_x = 0
hw_x = 0
flag_now = "idle"
flag = "idle"
while running:
    for e in pygame.event.get():
        if e.type == QUIT:
            running = False
            break
        elif e.type == VIDEORESIZE:
            current_size = e.size
            break
        elif pygame.key.get_pressed()[K_d]:
            s += 0.5
            if s >= a.run_frame:
                s = 0
            if bg_x <= -game_width:
                bg_x = 0
            bg_x -= 2
            hw_x -= 5
            flag = "run"
            break
        elif pygame.key.get_pressed()[K_a]:
            s += 0.5
            if s >= a.r_run_frame:
                s = 0
            if bg_x >= game_width:
                bg_x = 0
            bg_x += 2
            hw_x += 5
            flag = "reverse_run"
            break
    else:
        s += 0.25
        if s >= a.idle_frame:
            s = 0
        flag = "idle"
    virtual_surface.blit(background, (bg_x, 0))
    virtual_surface.blit(background, (bg_x + game_width, 0))
    virtual_surface.blit(background, (bg_x - game_width, 0))
    virtual_surface.blit(hallway, (hw_x, 0))
    if flag != flag_now:
        flag_now = flag
        s = 0
    print(flag_now)
    if flag_now == "run":
        virtual_surface.blit(a.ch_run, (0, 900 - 620), (a.charachter_y*int(s), 0, a.charachter_y, a.charachter_y))
    elif flag_now == "reverse_run":
        virtual_surface.blit(a.ch_r_run, (0, 900 - 620), (a.charachter_y * int(s), 0, a.charachter_y, a.charachter_y))
    elif flag_now == "idle":
        virtual_surface.blit(a.ch_idle, (0, 900 - 620), (a.charachter_y*int(s), 0, a.charachter_y, a.charachter_y))
    scaled_surface = pygame.transform.scale(virtual_surface, current_size)
    game.blit(scaled_surface, (0,0))
    pygame.display.flip()

    clock.tick(12)

quit()