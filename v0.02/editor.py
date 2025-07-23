import os
import pickle

import menu
from menu import *
from player import Player
from power_up import PowerUp
from settings import *
from surface import Surface
from moving_platform import MovingPlatform


def text_background(s, text_color, bg, size, screen, pos):
    x, y = pos
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', size)
    text_surface = my_font.render(f'{s}', False, text_color, bg)
    text_surface.set_alpha(150)
    screen.blit(text_surface, (x, y))
    text_surface = my_font.render(f'{s}', False, text_color)
    screen.blit(text_surface, (x, y))


def edit(surfaces, players, clock, screen):
    try:
        with open("levels/level.pkl", "rb") as f:
            surfaces = pickle.load(f)
    except:
        print("no save")
    global scroll
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 30)
    mousedown = False
    deletion = False
    object_types = [True, False, False]
    object_names = ["Ground/Wall", "PowerUp", "Moving"]
    current_obj = 0
    grid = 32
    editing = True
    pmx = 0
    pmy = 0
    selected_obj = None
    editing_index = 0
    while editing:
        screen.fill(BG)
        mx, my = pygame.mouse.get_pos()
        mx = int((mx - scroll) / grid) * grid
        my = int(my / grid) * grid
        for event in pygame.event.get():
            '''
            f12 | exit this mode
            \ | change item
            [ an ] | move tiles forward and backward
            numpad | load 0-9
            R-shift | save 0-9
            left/right | scroll
            l-shift | scroll faster
            z | edit item
            '''
            if event.type == pygame.KEYDOWN:
                if selected_obj:
                    if event.key == pygame.K_1:
                        d = selected_obj.__dict__
                        edit_items = list(d.items())
                        x = len(edit_items)
                        editing_index += 1
                        if editing_index >= x:
                            editing_index = 0
                        attr, value = edit_items[editing_index]
                        print(f"{attr},{value}")
                    if event.key == pygame.K_2:
                        d = selected_obj.__dict__
                        items = list(d.items())
                        x = len(items)
                        editing_index -= 1
                        if editing_index <= 0:
                            editing_index = x - 1
                # if event.key == pygame.K_1:
                #     for s in surfaces:
                #         if s.rect.collidepoint(mx, my):
                #             if type(s) == MovingPlatform:
                #                 s.speed[0] += 1
                # if event.key == pygame.K_2:
                #     for s in surfaces:
                #         if s.rect.collidepoint(mx, my):
                #             if type(s) == MovingPlatform:
                #                 s.speed[0] -= 1
                # if event.key == pygame.K_3:
                #     for s in surfaces:
                #         if s.rect.collidepoint(mx, my):
                #             if type(s) == MovingPlatform:
                #                 s.speed[1] += 1
                # if event.key == pygame.K_4:
                #     for s in surfaces:
                #         if s.rect.collidepoint(mx, my):
                #             if type(s) == MovingPlatform:
                #                 s.speed[1] -= 1

                if event.key == pygame.K_F12:
                    editing = False

                if event.key == pygame.K_BACKSLASH:
                    object_types[current_obj] = False
                    current_obj += 1
                    if current_obj + 1 > len(object_types):
                        current_obj = 0
                    object_types[current_obj] = True

                if event.key == pygame.K_z:
                    for s in surfaces:
                        if s.rect.collidepoint(mx, my):
                            selected_obj = s
                            i = surfaces.index(s)

                if event.key == pygame.K_LEFTBRACKET:  # moves back in draw order
                    for s in surfaces:
                        if s.rect.collidepoint(mx, my):
                            i = surfaces.index(s)
                            if not (i == 0):
                                temp = surfaces[i]
                                surfaces[i] = surfaces[i - 1]
                                surfaces[i - 1] = temp

                if event.key == pygame.K_RIGHTBRACKET:  # moves up in draw order
                    for s in surfaces:
                        if s.rect.collidepoint(mx, my):
                            i = surfaces.index(s)
                            if not (i == len(surfaces) - 1):
                                temp = surfaces[i]
                                surfaces[i] = surfaces[i + 1]
                                surfaces[i + 1] = temp

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

        key = pygame.key.get_pressed()
6
        if key[pygame.K_LSHIFT]:
            if key[pygame.K_LEFT]:
                scroll += 20
            if key[pygame.K_RIGHT]:
                scroll -= 20
        else:
            if key[pygame.K_LEFT]:
                scroll += 5
            if key[pygame.K_RIGHT]:
                scroll -= 5

        # for i in range(int(width / grid) * 100):  # draw mini grid
        #     pygame.draw.line(screen, (150, 50, 50), [grid * i + scroll, 0], [grid * i + scroll, height])
        # for i in range(int(height / grid)):
        #     pygame.draw.line(screen, (150, 50, 50), [0, grid * i], [width, grid * i])

        for i in range(int(width / grid) * 100):  # draw grid
            pygame.draw.line(screen, BLACK, [grid  * i + scroll, 0], [grid  * i + scroll, height])
        for i in range(int(height / grid * 4)):
            pygame.draw.line(screen, BLACK, [0, grid  * i], [width, grid  * i])



        for s in surfaces:
            s.draw(screen, scroll)
            s.update_attributes()
            if s.rect.collidepoint(mx, my):
                if key[pygame.K_DELETE]:
                    surfaces.pop(surfaces.index(s))
                if key[pygame.K_m]:
                    s.move(mx - pmx, my - pmy)

        for p in players:
            p.draw(screen)

        pmx = mx
        pmy = my

        if pygame.mouse.get_pressed()[0]: # get mouse pos
            mouse_pos = pygame.mouse.get_pos()
        else: # keep off screen default
            mouse_pos = [-width, -height]
        if selected_obj:
            menu.render_menu(screen, selected_obj, [width / 2, height / 2], mouse_pos)
            # d = selected_obj.__dict__
            # edit_items = list(d.items())
            # attr, value = edit_items[editing_index]
            # if type(value) is bool:
            #     if key[pygame.K_a]:
            #         setattr(selected_obj, attr, False if value else True)
            #
            #
            # text_background(f'{type(selected_obj)}', BLACK, WHITE, 30, screen, [10, 25])
            # y = 60
            # d = selected_obj.__dict__
            # items = list(d.items())
            # for i in range(len(items)):
            #     attr, value = items[i]
            #     text_background(f"{i}-{attr}: {str(value)}", BLACK, WHITE, 20, screen, [10, y])
            #     y += 25  # move down each line
        else:
            if pygame.mouse.get_pressed()[0] and not mousedown:  # could use events
                mousedown = True
                tx, ty = mx, my
            if mousedown:
                y1 = max(ty, my)
                y2 = min(ty, my)
                x1 = max(tx, mx)
                x2 = min(tx, mx)
                if x1 == x2:  # non zero sizes
                    x1 += 1
                if y1 == y2:
                    y1 += 1
                pygame.draw.rect(screen, (WHITE), [x2 + scroll, y2, abs(x2 - x1), abs(y2 - y1)])

            if not pygame.mouse.get_pressed()[0] and mousedown:  # which type
                if object_types[0]:
                    surfaces.append(Surface(x2, y2, abs(x2 - x1), abs(y2 - y1)))
                elif object_types[1]:
                    surfaces.append(PowerUp(x2, y2, 32, 32))
                elif object_types[2]:
                    surfaces.append(Surface(x2, y2, abs(x2 - x1), abs(y2 - y1)))
                print(object_types)
                print(current_obj)

                mousedown = False

            if key[pygame.K_BACKSPACE] and not deletion:
                deletion = True
                tx, ty = mx, my
            if not key[pygame.K_BACKSPACE] and deletion:
                y1 = max(ty, my)
                y2 = min(ty, my)
                x1 = max(tx, mx)
                x2 = min(tx, mx)
                evil_surface = Surface(x2, y2, abs(x2 - x1), abs(y2 - y1))
                for s in surfaces:
                    if s.rect.colliderect(evil_surface):
                        surfaces.pop(surfaces.index(s))

                deletion = False

            for s in surfaces:
                if s.rect.collidepoint(mx, my):
                    text_background(f'{type(s)}', BLACK, WHITE, 30, screen, [10, 25])
                    y = 60
                    d = s.__dict__
                    items = list(d.items())
                    for i in range(len(items)):
                        attr, value = items[i]
                        text_background(f"{i}-{attr}: {str(value)}", BLACK, WHITE, 20, screen, [10, y])
                        y += 25  # move down each line

        text_background(f'{object_names[current_obj]}', BLACK, WHITE, 30, screen, [0, 0])
        pygame.display.update()
        pygame.display.flip()

        clock.tick(60)
