import pygame

from settings import *
from surface import Surface


class MovingPlatform(Surface):
    def __init__(self, x, y, w, h):
        self.rect = pygame.rect.Rect(x, y, w, h)
        self.color = RED
        self.speed = [0, 0]
        if h == 1:
            self.movethrough = True
        else:
            self.movethrough = False
        self.bouncing = False
        self.scrolling = True
        self.x_limits = [0, 25600]
        self.y_limits = [0, height]
        self.attributes = f'speed={self.speed} | bouncing = {self.bouncing} | scrolling = {self.scrolling} | xlim {self.x_limits} | ylim {self.y_limits}'

    # # def update_attributes(self):
    #     self.attributes = f'speed={self.speed} | bouncing = {self.bouncing} | scrolling = {self.scrolling} | xlim {self.x_limits} | ylim {self.y_limits}'

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, RED,
                         [self.rect.left + scroll, self.rect.top, self.rect.width, self.rect.height])

    def surface_actions(self):
        x, y = self.speed
        self.move(x, y)
        # if self.rect.top > self.y_limits[1] and self.scrolling:
        #     self.move(0, -(self.y_limits[1] - self.y_limits[0]))
