import pygame
import random
import copy
import numpy as np
import gametree

# pygame setup
pygame.init()

# jaizdoma ko darit ar izmeru jo man ir 4k ekrans
screen = pygame.display.set_mode((0, 0))
clock = pygame.time.Clock()
running = True
screen_size = pygame.display.get_window_size()
center = (screen_size[0] / 2, screen_size[1] / 2)
circle_radius = screen_size[1] / 3.0
point_radius = circle_radius / 15.0

LINE_WIDTH = int(point_radius / 1.5)

punkti = []
gajiens=0
selected_point = None
state = None
selected_point = None

punktu_skaits: str = "Ievadiet lauciņu skaitu 15-25"
SEARCH_DEPTH=1
def generate_points(punktu_sk):
    p = []
    for i in range(punktu_sk):
        p.append(
            [
                center[0] + np.cos(i / punktu_sk * np.pi * 2) * circle_radius,
                center[1] + np.sin(i / punktu_sk * np.pi * 2) * circle_radius,
            ]
        )
    return p


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if state == None:
            if event.type == pygame.KEYDOWN and event.unicode.isdigit():
                if len(punktu_skaits) == 1:
                    punktu_skaits += event.unicode
                    punktu_sk = int(punktu_skaits)

                    if punktu_sk < 6 or punktu_sk > 25:
                        punktu_skaits = "Ievadiet lauciņu skaitu 15-25"
                        continue

                    punkti = generate_points(punktu_sk=punktu_sk)
                    gameinfo=gametree.GameInfo(punktu_skaits=punktu_sk,sak_dators=True,izmantot_alfa_beta=True)
                    state = gametree.GameState()
                else:
                    punktu_skaits = event.unicode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                punktu_skaits = "Ievadiet lauciņu skaitu 15-25"
        else:
            if( gajiens%2==1)==gameinfo.sak_dators:#speletaja gajiens
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if pygame.mouse.get_pressed()[0]:
                        mouse_pos = pygame.mouse.get_pos()
                        for i, punkts in enumerate(punkti):
                            if (punkts[0] - mouse_pos[0]) ** 2 + (
                                punkts[1] - mouse_pos[1]
                            ) ** 2 < point_radius**2:
                                if (
                                    selected_point is not None
                                    and selected_point != i
                                ):
                                    
                                    state.linijas.append((min(i,selected_point),max(i,selected_point)))
                                    gajiens+=1
                                    selected_point = None
                                else:
                                    selected_point = i
            else:#datora gajiens
                start_node=gametree.Node(gamestate=state,level=gajiens,gameinfo=gameinfo)
                next_node=gametree.NextMove(start_node,gameinfo,SEARCH_DEPTH)
                state=next_node.gamestate
                gajiens=next_node.level
    # clear screen
    screen.fill((0, 0, 0))

    if state == None:
        font = pygame.font.SysFont(None, 48)
        img = font.render(punktu_skaits, True, (255, 255, 255))
        text_rect = img.get_rect(
            center=(screen.get_size()[0] / 2, screen.get_size()[1] / 2)
        )
        screen.blit(img, text_rect)

        # jaievada punktu skaits
    else:
        # linijas tiek zimetas pirks punktiem jo linijam ir nesmuki gali
        for linija in state.linijas:
            pygame.draw.line(
                screen, (50, 100, 200), punkti[linija[0]], punkti[linija[1]], LINE_WIDTH
            )

        for i, punkts in enumerate(punkti):
            if i == selected_point:
                pygame.draw.circle(screen, (255, 215, 0), punkts, point_radius * 1.1)
            else:
                pygame.draw.circle(screen, (255, 255, 255), punkts, point_radius)

        teksts = "Jaiet {} \nP1 punkti {}\nP2 punkti {}"
        font = pygame.font.SysFont(None, 36)
        screen.blit(
            font.render("Jaiet: " + str(gajiens%2+1), True, (255, 255, 255)),
            (25, 50),
        )
        screen.blit(
            font.render("P1 punkti: " + str(state.p1_punkti), True, (255, 255, 255)),
            (25, 100),
        )
        screen.blit(
            font.render("P2 punkti: " + str(state.p2_punkti), True, (255, 255, 255)),
            (25, 150),
        )

        if len(state.linijas) == int(len(punkti) / 2):
            screen.blit(
                font.render("SPĒLE IR PABEIGTA!", True, (255, 255, 255)), (25, 250)
            )

    pygame.display.update()
