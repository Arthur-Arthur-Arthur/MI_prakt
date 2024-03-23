import pygame
import random
import copy
import numpy as np

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


def check_line_cross(
    linija_jauna: tuple[int, int], linija_veca: tuple[int, int], punktu_sk: int
):
    sakums_vecai = linija_veca[0]
    beigas_vecai = linija_veca[1]
    # pagriezam veco un jauno liniju ta lai veca saktos pie nulles
    rotetas_beigas_vecai = (beigas_vecai - sakums_vecai) % punktu_sk
    rotets_sakums_jaunai = (linija_jauna[0] - sakums_vecai) % punktu_sk
    rotetas_beigas_jaunai = (linija_jauna[1] - sakums_vecai) % punktu_sk
    # tagad parbaudam vai abi jaunas linija punkti ir viena puse vecajai
    sakums_pirms = rotets_sakums_jaunai < rotetas_beigas_vecai
    beigas_pirms = rotetas_beigas_jaunai < rotetas_beigas_vecai
    if sakums_pirms == beigas_pirms:
        return 0
    else:
        return 1


class State:
    tagad_jaiet = 0
    linijas = []  # linijas ir 2 punktu indeksi
    p1_punkti = 0
    p2_punkti = 0

    def __init__(
        self,
        linijas: list[tuple[int, int]] = [],
        tagad_jaiet: int = 0,
        p1_punkti: int = 0,
        p2_punkti: int = 0,
    ):
        self.linijas = linijas
        self.tagad_jaiet = tagad_jaiet
        self.p1_punkti = p1_punkti
        self.p2_punkti = p2_punkti

    # ar kopijam ir vieglak darboties, jo ieprieksejos nevar netisam mainit
    def AddLine(self, p1: int, p2: int):
        sods = 0
        for line in self.linijas:
            sods += check_line_cross((p1, p2), line, punktu_sk)
        if self.tagad_jaiet == 0:
            self.p1_punkti += sods
        elif self.tagad_jaiet == 1:
            self.p2_punkti += sods
        jaunas_linijas = copy.copy(self.linijas)
        jaunas_linijas.append((p1, p2))
        return State(
            jaunas_linijas, (self.tagad_jaiet + 1) % 2, self.p1_punkti, self.p2_punkti
        )

    def Connected(self, p1: int, p2: int):
        for linija in self.linijas:
            if (p1 == linija[0] and p2 == linija[1]) or (
                p2 == linija[0] and p1 == linija[1]
            ):
                return True
        return False

    def CanConnect(self, p1: int, p2: int):
        for linija in self.linijas:
            if p1 == linija[0] or p1 == linija[1] or p2 == linija[0] or p2 == linija[1]:
                return False
        return True


punkti = []
selected_point = None
state = None
selected_point = None

punktu_skaits: str = "Ievadiet lauciņu skaitu 15-25"


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

                    if punktu_sk < 15 or punktu_sk > 25:
                        punktu_skaits = "Ievadiet lauciņu skaitu 15-25"
                        continue

                    punkti = generate_points(punktu_sk=punktu_sk)

                    state = State()
                else:
                    punktu_skaits = event.unicode
            if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                punktu_skaits = "Ievadiet lauciņu skaitu 15-25"
        else:
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
                                and state.CanConnect(i, selected_point)
                            ):
                                state = state.AddLine(i, selected_point)
                                selected_point = None
                            else:
                                selected_point = i

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
            font.render("Jaiet: " + str(state.tagad_jaiet + 1), True, (255, 255, 255)),
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
