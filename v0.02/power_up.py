# from main_loop
import random

import pygame

from surface import Surface


class PowerUp(Surface):
    power = None

    def generate_power(self):
        if self.power == None:
            self.power = random.randint(1, 2)
        if self.power == 1:
            self.color = (0, 255, 0)
        if self.power == 2:
            self.color = (0, 0, 255)
        return self.power

    def draw(self, screen, scroll):
        pygame.draw.rect(screen, self.color,
                         [self.rect.left + scroll, self.rect.top, self.rect.width, self.rect.height])
