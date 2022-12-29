import pygame

class SetGUI():
    # Other
    screen = None
    setgame = None

    # Colors
    BG_COLOR = (55, 55, 55)
    CARD_COLOR = (255, 255, 255)
    HIGHLIGHT_COLOR = (255, 0, 0)

    # Card maps
    SHAPE_MAP = {0 : None, \
                 1 : None, \
                 2 : None}
    COLOR_MAP = {0 : (255, 0, 0), \
                 1 : (255, 0, 255), \
                 2 : (0, 255, 0)}
    NUMBER_MAP = {0 : 1, \
                  1 : 2, \
                  2 : 3}
    SHADING_MAP = {0 : None, \
                   1 : None, \
                   2 : None}


    # Dimensions
    CARD_WIDTH = 100
    CARD_HEIGHT = 60
    CARD_PADDING = 10
    HIGHLIGHT_THICKNESS = 3
    GRID_WIDTH = 3
    GRID_HEIGHT = 5
    WINDOW_WIDTH = GRID_WIDTH * CARD_WIDTH + (GRID_WIDTH + 1) * CARD_PADDING
    WINDOW_HEIGHT = GRID_HEIGHT * CARD_HEIGHT + (GRID_HEIGHT + 1) * CARD_PADDING

    def __init__(self, setgame):
        self.setgame = setgame

    def show(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.mouse.set_visible(1)
        pygame.display.set_caption("Set")

        # background = pygame.Surface(screen.get_size())
        # background = background.convert()
        # background.fill((250,250,250))
        # screen.blit(background, (0,0))
        # pygame.display.flip()

        # button.collidepoint(mouse_pos)

        exit = False
        while not exit:
            exit = self.update()


    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting")
                return True
            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            #     print("LMB Down")
            #     pos = pygame.mouse.get_pos()
            #     print(pos)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                # Figure out which card was clicked
                mouse_coords = pygame.mouse.get_pos()
                card_position = self.__coords_to_index(mouse_coords)
                print("Clicked card number", card_position, "at coordinates", mouse_coords)

                # Select the clicked card
                if card_position in self.setgame.get_selected_indices():
                    self.setgame.deselect_index(card_position)
                else:
                    self.setgame.select_index(card_position)

            # elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
            #     print("RMB Down")
            #     pos = pygame.mouse.get_pos()
            #     print(pos)
            # elif event.type == pygame.MOUSEBUTTONUP and event.button == 3:
            #     print("RMB Up")
            #     pos = pygame.mouse.get_pos()
            #     print(pos)

        # Draw background
        self.screen.fill(self.BG_COLOR)

        # Draw highlights
        for i in self.setgame.get_selected_indices():
            self.__draw_highlight(i)

        # Draw cards
        for i, card in enumerate(self.setgame.get_cards_on_table()):
            self.__draw_card(card, i)

        pygame.display.update()

        return False


    def __coords_to_index(self, coords):
        x = coords[0]
        y = coords[1]
        index = x // (self.CARD_WIDTH + self.CARD_PADDING) + \
                3 * (y // (self.CARD_HEIGHT + self.CARD_PADDING))
        return index


    def __draw_highlight(self, pos):
        x = pos % 3
        y = pos // 3

        rect = pygame.Rect(x * (self.CARD_WIDTH + self.CARD_PADDING) + self.CARD_PADDING - self.HIGHLIGHT_THICKNESS, \
                           y * (self.CARD_HEIGHT + self.CARD_PADDING) + self.CARD_PADDING - self.HIGHLIGHT_THICKNESS, \
                           self.CARD_WIDTH + 2 * self.HIGHLIGHT_THICKNESS, \
                           self.CARD_HEIGHT + 2 * self.HIGHLIGHT_THICKNESS)
        pygame.draw.rect(self.screen, self.HIGHLIGHT_COLOR, rect)


    def __draw_card(self, card, pos):
        shape = self.SHAPE_MAP[card[0]]
        color = self.COLOR_MAP[card[1]]
        number = self.NUMBER_MAP[card[2]]
        shading = self.SHADING_MAP[card[3]]

        x = pos % 3
        y = pos // 3

        # Create card back
        card_back = pygame.Rect(x * (self.CARD_WIDTH + self.CARD_PADDING) + self.CARD_PADDING, \
                           y * (self.CARD_HEIGHT + self.CARD_PADDING) + self.CARD_PADDING, \
                           self.CARD_WIDTH, \
                           self.CARD_HEIGHT)
        pygame.draw.rect(self.screen, self.CARD_COLOR, card_back)

        # Draw symbols
        # TODO: Implement...

