import pygame
import random
import copy

# pygame setup
pygame.init()

# jaizdoma ko darit ar izmeru jo man ir 4k ekrans
screen = pygame.display.set_mode((1280, 1280))
clock = pygame.time.Clock()
running = True

POINT_RADIUS = 40
LINE_WIDTH = 20


class State:
    tagad_jaiet = 0
    linijas = []  # linijas ir 2 punktu indeksi
    p1_punkti = 0
    p2_punkti = 0

    def __init__(
        self, linijas: list[int], tagad_jaiet: int, p1_punkti: int, p2_punkti: int
    ):
        self.linijas = linijas
        self.tagad_jaiet = tagad_jaiet
        self.p1_punkti = p1_punkti
        self.p2_punkti = p2_punkti

    # ar kopijam ir vieglak darboties, jo ieprieksejos nevar netisam mainit
    def WithLine(self, p1: int, p2: int):
        # saja vieta ir japarbauda vai jauna linija atnem punktu
        # todo
        jaunas_linijas = copy.copy(self.linijas)
        jaunas_linijas.append([p1, p2])
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

                    # generesanu vajag mainit
                    for i in range(punktu_sk):
                        punkti.append(
                            [random.randrange(100, 1000), random.randrange(100, 1000)]
                        )

                    state = State([], 0, 0, 0)
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
                        ) ** 2 < POINT_RADIUS**2:
                            if (
                                selected_point is not None
                                and selected_point != i
                                and state.CanConnect(i, selected_point)
                            ):
                                state = state.WithLine(i, selected_point)
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
                pygame.draw.circle(screen, (255, 215, 0), punkts, POINT_RADIUS * 1.1)
            else:
                pygame.draw.circle(screen, (255, 255, 255), punkts, POINT_RADIUS)

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
