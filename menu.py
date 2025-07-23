import pygame


def text_background(s, text_color, bg, size, screen, pos):
    x, y = pos
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', size)
    text_surface = my_font.render(f'{s}', False, text_color, bg)
    text_surface.set_alpha(150)
    screen.blit(text_surface, (x, y))
    text_surface = my_font.render(f'{s}', False, text_color)
    screen.blit(text_surface, (x, y))


def render_menu(screen, obj, pos, mouse):
    d = obj.__dict__
    edit_items = list(d.items())
    attr, value = edit_items[0]
    # if type(value) is bool:
    #     if key[pygame.K_a]:
    #         setattr(selected_obj, attr, False if value else True)

    text_background(f'{type(obj)}', 'black', 'white', 30, screen, [10, 25])
    y = 60
    d = obj.__dict__
    items = list(d.items())
    for i in range(len(items)):  # lots of magic numbers here, call me a wizard
        attr, value = items[i]
        this = type(value)
        if this is list:  # for 2D array
            a, b = value
            y += 30
            text_background(f"{i}-{attr}_x: {str(value[0])}", 'black', 'white', 20, screen,
                            [pos[0] * .75, pos[1] + y - len(items) * 25 / 2 - 30])
            text_background(f"{i}-{attr}_y: {str(value[1])}", 'black', 'white', 20, screen,
                            [pos[0] * .75, pos[1] + y - len(items) * 25 / 2])
            if render_button(screen, [pos[0] * .75 - 10, pos[1] + y - len(items) * 25 / 2 - 30], '+', mouse):
                setattr(obj, attr, [a + 1, b])
            if render_button(screen, [pos[0] * .75 - 20, pos[1] + y - len(items) * 25 / 2 - 30], '-', mouse):
                setattr(obj, attr, [a - 1, b])
            if render_button(screen, [pos[0] * .75 - 10, pos[1] + y - len(items) * 25 / 2], '+', mouse):
                setattr(obj, attr, [a, b + 1])
            if render_button(screen, [pos[0] * .75 - 20, pos[1] + y - len(items) * 25 / 2], '-', mouse):
                setattr(obj, attr, [a, b - 1])
        elif this is pygame.Rect:
            a, b, c, d = value
            y += 30
            text_background(f"{i}-{attr}_x: {str(value[0])}", 'black', 'white', 20, screen,
                            [pos[0] * .75, pos[1] + y - len(items) * 25 / 2 - 30])
            text_background(f"{i}-{attr}_y: {str(value[1])}", 'black', 'white', 20, screen,
                            [pos[0] * .75, pos[1] + y - len(items) * 25 / 2])
            if render_button(screen, [pos[0] * .75 - 10, pos[1] + y - len(items) * 25 / 2 - 30], '+', mouse):
                setattr(obj, attr, pygame.rect.Rect(a + 1, b, c, d))
            if render_button(screen, [pos[0] * .75 - 20, pos[1] + y - len(items) * 25 / 2 - 30], '-', mouse):
                setattr(obj, attr, pygame.rect.Rect(a - 1, b, c, d))
            if render_button(screen, [pos[0] * .75 - 10, pos[1] + y - len(items) * 25 / 2], '+', mouse):
                setattr(obj, attr, pygame.rect.Rect(a, b + 1, c, d))
            if render_button(screen, [pos[0] * .75 - 20, pos[1] + y - len(items) * 25 / 2], '-', mouse):
                setattr(obj, attr, pygame.rect.Rect(a, b - 1, c, d))

        else:
            text_background(f"{i}-{attr}: {str(value)}", 'black', 'white', 20, screen,
                            [pos[0] * .75, pos[1] + y - len(items) * 25 / 2])

        y += 30  # move down each line


def render_button(screen, pos, txt, mouse):

    x, y = pos
    # button_rect = pygame.rect.Rect([x,y + 7.5, 8, 8])
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 16)
    text_surface = my_font.render(f'{txt}', False, 'blue', 'orange')
    screen.blit(text_surface, (x, y))

    button_rect = text_surface.get_rect()
    pygame.draw.rect(screen, 'orange', button_rect)
    if button_rect.collidepoint(mouse):
        return True
    else:
        return False
