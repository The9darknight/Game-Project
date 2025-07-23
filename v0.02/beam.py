import math
import time

import pygame


class Beam:
    def __init__(self, p1, p2):
        self.pos = p1.pos
        self.pos2 = p2.pos
        self.speed = 10
        x1, y1 = p1.pos
        x2, y2 = p2.pos
        angle = math.atan2(x2 - x1, y2 - y1)
        vx = math.sin(angle) * self.speed
        vy = math.cos(angle) * self.speed
        self.velocity = [vx, vy]
        self.time = time.time()
        self.life = 2

    def move(self, canvas):
        x, y = self.pos
        self.pos = [self.pos[0] + self.velocity[0], self.pos[1] + self.velocity[1]]
        pygame.draw.line(canvas, (0, 0, 255), [x, y], [self.pos[0], self.pos[1]], 3)
        return time.time() - self.time >= self.life
