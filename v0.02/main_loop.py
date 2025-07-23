import os
import pickle
import time

import pygame

from beam import Beam
from editor import edit
from goal import Goal
from player import Player
from power_up import PowerUp
from settings import *
from surface import Surface

screen = pygame.display.set_mode((width, height))
canvas = pygame.Surface((25600, height))

p1_camera = pygame.Rect(0, 0, width / 2, height)
p2_camera = pygame.Rect(0, 0, width / 2, height)


def main():
    global scroll
    global p1_camera
    global p2_camera
    pygame.init()
    clock = pygame.time.Clock()
    running = True
    mousedown = False
    deletion = False
    grid = 8
    current_time = time.time()
    pmx = 0
    pmy = 0

    object_types = [1, 0]
    current_obj = 0

    surfaces = []
    beams = []
    players = []
    try:
        with open("levels/level0/surfaces.pkl", "rb") as f:
            surfaces = pickle.load(f)
        with open("levels/level0/players.pkl", "rb") as f:
            player_data = pickle.load(f)
            players = [Player(d["x"], d["y"], d["id"]) for d in player_data]
    except:
        print("no save")
        with open("level.pkl", "rb") as f:
            surfaces = pickle.load(f)
        players = [Player(1000, 1000, 1), Player(1000, 1000, 2)]  # [p1, p2]

    for s in surfaces:  # cleanup
        if s.rect.width == 0 or s.rect.height == 0:
            surfaces.pop(surfaces.index(s))

    p1, p2 = [players[0], players[1]]
    p1.p2, p2.p2 = [players[1], players[0]]
    hoob = Goal(8096, 48)
    while running:
        dt = (time.time() - current_time)
        mx, my = pygame.mouse.get_pos()
        mx = int(mx / grid) * grid
        my = int(my / grid) * grid
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                '''
                f12 | edit mode
                wasd and arrows | does as expected
                esc | reset
                numpad | load 0-9
                R-shift | save 0-9
                space | beam
                k | kick
                '''
                if event.key == pygame.K_F12:
                    edit(surfaces, players, clock, screen)
                    scroll = 0
                if event.key == pygame.K_UP and p1.grounded == True:
                    p1.control(0, 15, 0)
                if event.key == pygame.K_k:
                    p1.control(0, 0, 1)
                if event.key == pygame.K_DOWN:
                    p1.control(0, -1, 0)
                if event.key == pygame.K_w and p2.grounded == True:
                    p2.control(0, 15, 0)
                if event.key == pygame.K_s:
                    p2.control(0, -1, 0)

                if event.key == pygame.K_ESCAPE:
                    running = False

                for i in range(10):
                    if event.key == getattr(pygame, f'K_KP{i}'):
                        if key[pygame.K_RSHIFT]:
                            if not os.path.exists(f"levels/level{i}/"):
                                os.mkdir(f"levels/level{i}/")
                            with open(f"levels/level{i}/surfaces.pkl", "wb") as f:
                                pickle.dump(surfaces, f)
                            with open(f"levels/level{i}/players.pkl", "wb") as f:
                                player_data = [{"x": p.pos[0], "y": p.pos[1], "id": p.id} for p in players]
                                pickle.dump(player_data, f)
                        else:
                            with open(f"levels/level{i}/surfaces.pkl", "rb") as f:
                                surfaces = pickle.load(f)
                            with open(f"levels/level{i}/players.pkl", "rb") as f:
                                player_data = pickle.load(f)
                                players = [Player(d["x"], d["y"], d["id"]) for d in player_data]
                                p1, p2 = players

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_DOWN:
                    if not p1.scrunched:
                        p1.control(0, -2, 0)
                    else:
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_DOWN))
                if event.key == pygame.K_s:
                    if not p2.scrunched:
                        p2.control(0, -2, 0)
                    else:
                        pygame.event.post(pygame.event.Event(pygame.KEYUP, key=pygame.K_s))
        screen.fill(RED)
        canvas.fill(BG)
        key = pygame.key.get_pressed()

        ################################################
        if key[pygame.K_SPACE]:
            if dt > .5:
                beams.append(Beam(p1, p2))
                current_time = time.time()
        if key[pygame.K_LEFT]:
            p1.control(-1, 0, 0)
            p1.facing = 1
        if key[pygame.K_RIGHT]:
            p1.control(1, 0, 0)
            p1.facing = 0
        if key[pygame.K_a]:
            p2.control(-1, 0, 0)
            p2.facing = 1
        if key[pygame.K_d]:
            p2.control(1, 0, 0)
            p2.facing = 0
        ################################################

        if pygame.mouse.get_pressed()[0] and not mousedown:
            mousedown = True
            tx, ty = mx, my
        if mousedown:
            y1 = max(ty, my)
            y2 = min(ty, my)
            x1 = max(tx, mx)
            x2 = min(tx, mx)
            if x1 == x2:
                x1 += 1
            if y1 == y2:
                y1 += 1
            pygame.draw.rect(screen, (WHITE), [x2, y2, abs(x2 - x1), abs(y2 - y1)])
            # pygame.draw.

        if not pygame.mouse.get_pressed()[0] and mousedown:
            if object_types[0]:
                surfaces.append(Surface(x2, y2, abs(x2 - x1), abs(y2 - y1)))
            elif object_types[1]:
                surfaces.append(PowerUp(x2, y2, 32, 32))

            mousedown = False

        if key[pygame.K_BACKSPACE] and not deletion:
            deletion = True
            tx, ty = mx, my
        if not key[pygame.K_BACKSPACE] and deletion:
            y1 = max(ty, my)
            y2 = min(ty, my)
            x1 = max(tx, mx)
            x2 = min(tx, mx)
            evil_surface = Surface(x2, y2, abs(x2 - x1), abs(y2 - y1))  # the deletion box
            for s in surfaces:
                if s.rect.colliderect(evil_surface):
                    surfaces.pop(surfaces.index(s))

            deletion = False

        ################################################
        for s in surfaces:
            s.surface_actions()
            if s.rect.colliderect(p1_camera) or s.rect.colliderect(p2_camera):
                s.draw(canvas, scroll)
                s.move(0, 0)
                if s.rect.collidepoint(mx, my):
                    if key[pygame.K_DELETE]:
                        surfaces.pop(surfaces.index(s))
                    if key[pygame.K_m]:
                        s.move(mx - pmx, my - pmy)

        for p in players:
            # pygame.draw.line(canvas, (0, 255, 0), p.pos, [0, 0])
            if time.time() - p.time[2] > .1:
                p.grounded = False
            p.movement(surfaces)
            p.collision(hoob)
            p.draw(canvas)
        # p1.collision(p2)
        # p2.collision(p1)
        ################################################

        pmx = mx
        pmy = my
        hoob.draw(canvas)
        for b in beams:
            if b.move(canvas):
                beams.pop(beams.index(b))

        if p1.pos[0] < p2.pos[0]:
            p2_camera = pygame.Rect(p2.pos[0] - width / 4, 0, width / 2, height)
            p1_camera = pygame.Rect(p1.pos[0] - width / 4, 0, width / 2, height)
        else:
            p1_camera = pygame.Rect(p2.pos[0] - width / 4, 0, width / 2, height)
            p2_camera = pygame.Rect(p1.pos[0] - width / 4, 0, width / 2, height)

        if p1_camera.colliderect(p2_camera):
            midpoint = (p1.pos[0] + p2.pos[0]) / 2
            p1_camera = pygame.Rect(midpoint - width / 2, 0, width / 2, height)
            p2_camera = pygame.Rect(midpoint, 0, width / 2, height)
            screen.blit(canvas, (0, 0), p1_camera)
            screen.blit(canvas, (width / 2, 0), p2_camera)
        else:
            screen.blit(canvas, (0, 0), p1_camera)
            screen.blit(canvas, (width / 2, 0), p2_camera)
            pygame.draw.line(screen, (0, 0, 255), [width / 2, 0], [width / 2, height], 2)

        pygame.display.update()
        pygame.display.flip()

        clock.tick(60)

    # pygame.quit()
    return


while True:
    main()
