import time

import pygame

from goal import Goal
from power_up import PowerUp
from settings import *
from moving_platform import MovingPlatform


class Player: #todo: add "kart" player. goes faster maybe but drifts
    gravity = 1
    terminal_velocity = 10
    frame_time = 0.1

    def __init__(self, x, y, player_id):
        self.id = player_id
        if player_id == 2:
            sprite_dir = "sprites/p2/"
        else:
            sprite_dir = "sprites/p1/"
        # todo: load sprites into a dict
        self.sprites = [sprite_dir + "player.png", sprite_dir + "run1.png", sprite_dir + "run2.png",
                        sprite_dir + "crouch.png", sprite_dir + "crawl1.png", sprite_dir + "crawl2.png",
                        sprite_dir + "kick1.png", sprite_dir + "kick2.png"]

        self.collisions = []

        t = time.time()
        self.time = [t] * 5
        # t = 0:animating | 1:power-up | 2:coyote time | 3: stun | 4: kick

        self.facing = False
        self.grounded = False
        self.overhead = False
        self.crouched = False
        self.scrunched = False
        self.kicking = False

        self.powerUp = 0

        self.normal_width = 18
        self.normal_height = 32
        self.width = 18
        self.height = 32

        self.normal_speed = 1
        self.speed = 1
        self.pos = [x, y]
        self.velocity = [0, 0]
        self.p2 = None

        self.image = pygame.image.load(self.sprites[0]).convert_alpha()
        self.image = pygame.transform.scale(self.image, (self.width, self.height))
        self.rect = pygame.rect.Rect(self.pos[0] - self.width / 2, self.pos[1] - self.height / 2, self.width,
                                     self.height)

    def set_sprite(self, id):
        self.image = pygame.image.load(self.sprites[id - 1]).convert_alpha()
        self.image = pygame.transform.flip(self.image, self.facing, False)
        if id < 7:  # todo: fix this up
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        else:
            self.image = pygame.transform.scale(self.image, (36, 32))

    def control(self, horizontal, vertical, action):
        self.velocity[0] += horizontal * self.speed

        if vertical > 0:
            self.velocity[1] = -vertical
            if self.velocity[1] >= 10:
                self.velocity[1] = 10
        elif vertical == -1 and self.height == self.normal_height:
            self.crouched = True
            self.height = .5 * self.normal_height
            self.speed = .5 * self.normal_speed
            if self.grounded:
                self.pos[1] += self.height / 2
        elif vertical == -2 and not self.height == self.normal_height:
            self.crouched = False
            self.height = self.normal_height
            self.speed = self.normal_speed
            if self.grounded:
                self.pos[1] -= self.height / 4

        if action == 1:
            self.time[0] = time.time()
            self.kicking = True

    def walk_cycle(self, direction):
        anim = self.frame_time
        dt = time.time() - self.time[0]
        if dt < anim / self.speed:
            if self.crouched:
                self.set_sprite(5)
            else:
                self.set_sprite(2)
        elif dt < 2 * anim / self.speed:
            if self.crouched:
                self.set_sprite(6)
            else:
                self.set_sprite(3)
        else:
            self.time[0] = time.time()

    def kick(self):
        dt = time.time() - self.time[0]
        if dt < .1 / self.speed:
            self.set_sprite(7)
        elif dt < .2 / self.speed:
            self.set_sprite(8)
        elif dt < .3 / self.speed:
            self.set_sprite(7)
        else:
            self.kicking = False

    def collision(self, obj):  # todo: if you're under and jump while moving, its jittery
        collisions = [0, 0, 0, 0, 0]
        x = self.pos[0]
        if obj.rect.left - x < 10 or x - obj.rect.right < 10:
            rect = self.rect

            overhead = pygame.rect.Rect(self.pos[0] - self.width / 2, self.pos[1] - self.height / 2 - self.height / 4,
                                        self.width,
                                        self.height)  # checking just above the player
            if rect.colliderect(obj):
                onTop = ((rect.bottom - obj.rect.top) >= self.velocity[1] + self.height / 3) and (
                        (rect.top - obj.rect.bottom) <= self.velocity[1] - self.height / 3)
                self.rect = pygame.rect.Rect(self.pos[0] - self.width / 2, self.pos[1] - self.height / 2, self.width,
                                             self.height)
                if type(obj) is Goal:
                    obj.holder = self
                    collisions[4] = True
                    return collisions
                elif type(obj) is PowerUp:
                    if obj.power == None:
                        self.time[1] = 0  # clear
                        self.ability(self.p2)
                        self.powerUp = obj.generate_power()
                    collisions[4] = True
                    return collisions
                elif obj.movethrough:  # if its one of those you can jump through
                    if rect.bottom >= obj.rect.top and rect.bottom - self.velocity[1] < obj.rect.top + 5 and \
                            self.velocity[
                                1] >= 0:
                        self.velocity[1] = 0
                        self.pos[1] = obj.rect.top - self.rect.height / 2
                        collisions[0] = True
                # regular collisions
                elif rect.right >= obj.rect.left > rect.left and onTop:  # hitting the left side
                    self.velocity[0] = 0
                    self.pos[0] = obj.rect.left - self.rect.width / 2
                    collisions[2] = True
                elif rect.right >= obj.rect.right > rect.left and onTop:  # right
                    self.velocity[0] = 0
                    self.pos[0] = obj.rect.right + self.rect.width / 2
                    collisions[3] = True
                elif rect.bottom >= obj.rect.top > rect.top:  # top
                    # if type(obj) is MovingPlatform:

                    self.velocity[0]+=obj.speed[0]
                    self.velocity[1]=obj.speed[1]
                    self.velocity[1]-=self.gravity
                    self.pos[1] = obj.rect.top - self.rect.height/2
                    collisions[0] = True
                elif rect.bottom >= obj.rect.bottom > rect.top:  # bottom
                    # if type(obj) is MovingPlatform:
                    # self.pos[0]+=obj.speed[0]
                    # self.pos[1]+=obj.speed[1]
                    self.velocity[1] = 0
                    self.pos[1] = obj.rect.bottom + self.rect.height / 2
                    collisions[1] = True

        if obj.rect.colliderect(overhead):
            self.overhead = True
        return collisions

    def ability(self, p2):
        dt = time.time() - self.time[1]
        if self.powerUp == 0:
            self.time[1] = time.time()
            return None
        elif self.powerUp == 1:
            self.normal_height *= 2
            self.height *= 2
            self.time[1] = time.time()
            self.powerUp = -1
            return None
        elif self.powerUp == 2:
            self.normal_width *= 2
            self.width *= 2
            self.time[1] = time.time()
            self.powerUp = -2
            return None
        elif self.powerUp == -1:
            if dt > 5:
                self.normal_height /= 2
                self.height /= 2
                self.powerUp = 0
            return None
        elif self.powerUp == -2:
            if dt > 5:
                self.normal_width /= 2
                self.width /= 2
                self.powerUp = 0
            return None

    def movement(self, surfaces):
        self.ability(self.p2)

        if self.velocity[1] < self.terminal_velocity:
            self.velocity[1] += self.gravity
        vx, vy = self.velocity
        x, y = self.pos

        x += vx
        y += vy

        if y > height:
            y = 0
        elif y < 0:
            y = height

        if abs(vx) > .1 and not self.kicking:
            self.walk_cycle(1)
        elif self.kicking:
            self.kick()
        else:
            if self.crouched:
                self.set_sprite(4)
            else:
                self.set_sprite(1)
        self.pos = [x, y]
        self.velocity = [vx, vy]
        self.velocity[0] *= .8 * (abs(self.velocity[0]) > .33)  # if moving slower than .33: = 0
        self.rect = pygame.rect.Rect(self.pos[0] - self.width / 2, self.pos[1] - self.height / 2, self.width,
                                     self.height)

        collision_list = [0, 0, 0, 0, 0]
        for s in surfaces:
            self.collisions = self.collision(s)
            collision_list = [a or b for a, b in zip(collision_list, self.collisions)]
        if collision_list[0]:  # coyote time
            # here the player gets some grace with jumping
            # they get to jump within
            self.grounded = True
            self.time[2] = time.time()  # set the time for coyote check

        if self.grounded and self.overhead:  # cant get up if there is something in the way
            self.scrunched = True
        else:
            self.scrunched = False

        self.overhead = False

    def draw(self, surface):
        surface.blit(self.image, [self.rect.topleft[0] + scroll, self.rect.topleft[1]])
