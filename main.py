import pygame
from pygame.locals import *
import math
import random
from lxml import etree
import os

pygame.init()
pygame.display.set_caption('Present for Kristo')
clock = pygame.time.Clock()

game_width = 900
game_height = 506
game = pygame.display.set_mode((game_width, game_height), pygame.RESIZABLE)
current_size = game.get_size()
virtual_surface = pygame.Surface((game_width, game_height))
background = pygame.image.load(os.getcwd() + "\\background.png").convert_alpha()
hallway = pygame.image.load(os.getcwd() + "\\hallway.png").convert_alpha()
character_y = 216


class MainCharacter(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.character_y = 216
        self.attack = []
        self.r_attack = []
        self.animations = {}
        for i in os.listdir("animations_mp\\"):
            self.animations[i] = self.load_animations(i)
        self.current_sprite = 0
        self.image = self.animations["idle"]["idle"][self.current_sprite]
        self.rect = self.image.get_rect()
        self.state = "idle"
        self.direction = "right"
        self.run_flag = False
        self.jump_flag = 0
        self.rect.x = 0
        self.rect.y = 290

    @staticmethod
    def load_animations(t):
        a = []
        b = []
        for i in os.listdir(f"animations_mp\\{t}"):
            im = pygame.image.load(f"animations_mp\\{t}\\" + i)
            im = pygame.transform.scale(im, (character_y, character_y))
            im_r = pygame.transform.flip(im, True, False)
            a.append(im)
            b.append(im_r)
        return {t: a, "r_" + t: b}

    def animation(self, state):
        if self.state != state and state != "run":
            self.current_sprite = 0
        self.state = state

    def update(self):
        if self.state == "attack":
            self.update_anim(0.5)
        elif self.state == "run":
            self.update_pos()
            self.update_anim(0.5)
        elif self.state == "jump":
            self.update_pos()
            self.update_anim(0.2)
        elif self.state == "idle":
            self.update_anim(0.3)

    def update_anim(self, speed):
        self.current_sprite += speed
        if int(self.current_sprite) >= len(self.animations[self.state][self.state]):
            self.current_sprite = 0
            if not self.run_flag:
                self.state = "idle"
        if self.direction == "right":
            self.image = self.animations[self.state][self.state][int(self.current_sprite)]
        elif self.direction == "left":
            self.image = self.animations[self.state]["r_" + self.state][int(self.current_sprite)]
        if self.run_flag:
            self.state = "idle"
            self.run_flag = False


    def update_pos(self):
        if self.state == "run" or self.state == "jump":
            if self.direction == "left":
                self.rect.x -= 2
            elif self.direction == "right":
                self.rect.x += 2
        if self.state == "jump":
            if self.jump_flag == 0:
                self.rect.y -= 5
                self.jump_flag += 1
            elif self.jump_flag == 1:
                self.rect.y -= 5
                self.jump_flag += 1
            elif self.jump_flag == 2:
                self.rect.y += 5
                self.jump_flag += 1
            elif self.jump_flag == 3:
                self.rect.y += 5
                self.jump_flag = 0

s = 0
bg_x = 0
hw_x = 0
q = 0
moving_sprites = pygame.sprite.Group()
player = MainCharacter()
moving_sprites.add(player)
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            player.animation("attack")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.animation("jump")
        elif pygame.key.get_pressed()[K_d]:
            player.animation("run")
            player.run_flag = True
            player.direction = "right"
            if bg_x <= -game_width:
                bg_x = 0
            bg_x -= 4
            #hw_x -= 2
        elif pygame.key.get_pressed()[K_a]:
            player.animation("run")
            player.run_flag = True
            player.direction = "left"
            if bg_x >= game_width:
                bg_x = 0
            bg_x += 2


    virtual_surface.blit(background, (bg_x, 0))
    virtual_surface.blit(background, (bg_x + game_width, 0))
    virtual_surface.blit(background, (bg_x - game_width, 0))
    virtual_surface.blit(hallway, (hw_x, 0))
    scaled_surface = pygame.transform.scale(virtual_surface, current_size)
    game.blit(scaled_surface, (0, 0))
    moving_sprites.draw(game)
    moving_sprites.update()
    pygame.display.flip()
    clock.tick(24)

quit()
