import pygame

from settings import *


def squiggle(surface, rect, scroll):
    for i in range(0, rect.width, 5):
        if i % 2:
            mod = 1
        else:
            mod = -1
        pygame.draw.circle(surface, (155, 0, 0), [rect.topleft[0] + i + scroll, rect.topleft[1] - mod + 2], 3)
        pygame.draw.circle(surface, (155, 0, 0), [rect.topleft[0] + i + 2 + scroll, rect.topleft[1] + mod + 2], 3)


class Surface:

    def __init__(self, x, y, w, h):
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.color = RED
        self.speed = [0, 0]
        self.attributes = ""
        if h == 1:
            self.movethrough = True
        else:
            self.movethrough = False

    def move(self, x, y):
        self.rect = pygame.rect.Rect(self.rect.left + x, self.rect.top + y, self.rect.width,
                                     self.rect.height)

    def update_attributes(self):
        pass

    def surface_actions(self):
        return

    def draw(self, surface, scroll):
        pygame.draw.rect(surface, self.color,
                         [self.rect.left + scroll, self.rect.top, self.rect.width, self.rect.height])
        squiggle(surface, self.rect, scroll)
