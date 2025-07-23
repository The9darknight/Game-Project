# from main_loop import *
import math

import pygame


class Goal:

    def __init__(self, x, y):
        self.hover = 0
        self.pos = [x, y]
        self.holder = None
        self.size = 32
        self.image = pygame.image.load("sprites/hoob.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.size, self.size))
        self.rect = pygame.rect.Rect(self.pos[0] - self.size / 2, self.pos[1] - self.size / 2, self.size,
                                     self.size)

    def draw(self, surface):
        self.hover += .04
        if self.holder:
            self.rect = pygame.rect.Rect(self.holder.rect.topleft[0] - self.size / 4,
                                         self.holder.rect.topleft[1] - 1.5 * self.size + math.sin(self.hover) * 10,
                                         self.size,
                                         self.size)
            rect = pygame.rect.Rect([self.rect.left, self.rect.top, self.rect.width, self.rect.height])
        else:
            rect = pygame.rect.Rect(
                [self.rect.left, self.rect.top + math.sin(self.hover) * 10, self.rect.width, self.rect.height])

        surface.blit(self.image, rect.topleft)
