import pygame

class SetGUI():
    # Other
    screen = None
    setgame = None
    shown_set = -1

    # Colors
    BG_COLOR = (55, 55, 55)
    CARD_COLOR = (255, 255, 255)
    REVEAL_HIGHLIGHT_COLOR = (255, 0, 0)
    SELECTION_HIGHLIGHT_COLOR = (0, 155, 0)

    # Function to draw the shape
    SHAPE_MAP = {0 : "oval", \
                 1 : "squiggle", \
                 2 : "diamond"}

    # Which color to use
    COLOR_MAP = {0 : (255, 0, 0), \
                 1 : (255, 0, 255), \
                 2 : (0, 155, 0)}

    # Positions to draw the shapes
    NUMBER_MAP = {0 : [2], \
                  1 :[1, 3], \
                  2 : [1, 2, 3]}

    # What type of shading to use
    SHADING_MAP = {0 : "solid", \
                   1 : "striped", \
                   2 : "outlined"}


    # Dimensions
    CARD_WIDTH = 100
    CARD_HEIGHT = 60
    CARD_PADDING = 10

    HIGHLIGHT_THICKNESS = 3

    GRID_WIDTH = 3
    GRID_HEIGHT = 6

    SYMBOL_WIDTH = 20
    SYMBOL_HEIGHT = 40
    OUTLINE_THICKNESS = 2
    STRIPE_THICKNESS = 1

    WINDOW_WIDTH = GRID_WIDTH * CARD_WIDTH + (GRID_WIDTH + 1) * CARD_PADDING
    WINDOW_HEIGHT = GRID_HEIGHT * CARD_HEIGHT + (GRID_HEIGHT + 1) * CARD_PADDING

    def __init__(self, setgame):
        self.setgame = setgame


    def show(self):
        pygame.init()
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.mouse.set_visible(1)
        pygame.display.set_caption("Set")

        while self.setgame.is_running():
            self.__update()


    def __update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print("Quitting game...")
                exit()
            else:
                self.__handle_event(event)

        if self.setgame.is_running():
            self.__draw_game()
        else:
            self.__show_score()


    def __handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            mouse_coords = pygame.mouse.get_pos()
            card_position = self.__coords_to_index(mouse_coords)
            self.setgame.toggle_selection(card_position)
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:    # [esc] Close game
                print("Quitting game...")
                exit()
            if event.key == pygame.K_r:         # [r]eset game
                self.setgame.reset_game()
            if event.key == pygame.K_p:         # [p]rint game state to console
                self.setgame.print_game()
            if event.key == pygame.K_f:         # [f]ind a set on the table
                number_of_sets = len(self.setgame.get_sets_on_table())
                self.shown_set += 1
                if self.shown_set == number_of_sets:
                    self.shown_set = -1
            if event.key == pygame.K_NUMLOCK:
                self.setgame.toggle_selection(0)
            if event.key == pygame.K_KP_DIVIDE:
                self.setgame.toggle_selection(1)
            if event.key == pygame.K_KP_MULTIPLY:
                self.setgame.toggle_selection(2)
            if event.key == pygame.K_KP7:
                self.setgame.toggle_selection(3)
            if event.key == pygame.K_KP8:
                self.setgame.toggle_selection(4)
            if event.key == pygame.K_KP9:
                self.setgame.toggle_selection(5)
            if event.key == pygame.K_KP4:
                self.setgame.toggle_selection(6)
            if event.key == pygame.K_KP5:
                self.setgame.toggle_selection(7)
            if event.key == pygame.K_KP6:
                self.setgame.toggle_selection(8)
            if event.key == pygame.K_KP1:
                self.setgame.toggle_selection(9)
            if event.key == pygame.K_KP2:
                self.setgame.toggle_selection(10)
            if event.key == pygame.K_KP3:
                self.setgame.toggle_selection(11)


    def __coords_to_index(self, coords):
        x = coords[0]
        y = coords[1]
        index = x // (self.CARD_WIDTH + self.CARD_PADDING) + \
                3 * (y // (self.CARD_HEIGHT + self.CARD_PADDING))
        return index


    def __draw_game(self):
        # Draw background
        self.screen.fill(self.BG_COLOR)

        # Draw selection
        for pos in self.setgame.get_selected_indices():
            self.__draw_highlight(pos, self.SELECTION_HIGHLIGHT_COLOR)

        # Reveal sets
        if self.shown_set != -1:
            sets_on_table = self.setgame.get_sets_on_table()
            set_to_show = sets_on_table[self.shown_set]
            for pos in set_to_show:
                self.__draw_highlight(pos, self.REVEAL_HIGHLIGHT_COLOR)

        # Draw cards
        for i, card in enumerate(self.setgame.get_cards_on_table()):
            self.__draw_card(card, i)

        # Update screen
        pygame.display.update()


    def __draw_highlight(self, pos, color):
        x = pos % 3
        y = pos // 3

        rect = pygame.Rect(x * (self.CARD_WIDTH + self.CARD_PADDING) + self.CARD_PADDING - self.HIGHLIGHT_THICKNESS, \
                           y * (self.CARD_HEIGHT + self.CARD_PADDING) + self.CARD_PADDING - self.HIGHLIGHT_THICKNESS, \
                           self.CARD_WIDTH + 2 * self.HIGHLIGHT_THICKNESS, \
                           self.CARD_HEIGHT + 2 * self.HIGHLIGHT_THICKNESS)
        pygame.draw.rect(self.screen, color, rect)


    def __draw_card(self, card, pos):
        shape = self.SHAPE_MAP[card[0]]
        color = self.COLOR_MAP[card[1]]
        symbol_positions = self.NUMBER_MAP[card[2]]
        shading = self.SHADING_MAP[card[3]]

        card_x = (pos % 3) * (self.CARD_WIDTH + self.CARD_PADDING) + self.CARD_PADDING
        card_y = (pos // 3) * (self.CARD_HEIGHT + self.CARD_PADDING) + self.CARD_PADDING

        # Create card back
        card_back = pygame.Rect(card_x, card_y, self.CARD_WIDTH, self.CARD_HEIGHT)
        pygame.draw.rect(self.screen, self.CARD_COLOR, card_back)

        # Draw symbols
        for symbol_position in symbol_positions:
            center = [card_x + symbol_position * (self.CARD_WIDTH / 4), \
                      card_y + (self.CARD_HEIGHT / 2)]

            if shape == "oval":
                self.__draw_oval(center, color, shading)
            elif shape == "squiggle":
                self.__draw_squiggle(center, color, shading)
            elif shape == "diamond":
                self.__draw_diamond(center, color, shading)


    def __draw_oval(self, center, color, shading):
        if shading == "solid":
            pygame.draw.circle(self.screen, color, center, self.SYMBOL_WIDTH / 2)
        elif shading == "striped":
            pygame.draw.circle(self.screen, color, center, self.SYMBOL_WIDTH / 2, self.OUTLINE_THICKNESS)
            # TODO: Add stripes
            pygame.draw.line(self.screen, color, [center[0] - self.SYMBOL_WIDTH / 2, center[1]], [center[0] + self.SYMBOL_WIDTH / 2, center[1]], self.STRIPE_THICKNESS)
        elif shading == "outlined":
            pygame.draw.circle(self.screen, color, center, self.SYMBOL_WIDTH / 2, self.OUTLINE_THICKNESS)


    def __draw_squiggle(self, center, color, shading):
        x = center[0] - self.SYMBOL_WIDTH / 2
        y = center[1] - self.SYMBOL_HEIGHT / 2

        if shading == "solid":
            pygame.draw.rect(self.screen, color, [x, y, self.SYMBOL_WIDTH, self.SYMBOL_HEIGHT])
        elif shading == "striped":
            pygame.draw.rect(self.screen, color, [x, y, self.SYMBOL_WIDTH, self.SYMBOL_HEIGHT], self.OUTLINE_THICKNESS)
            # TODO: Add stripes
            pygame.draw.line(self.screen, color, [center[0] - self.SYMBOL_WIDTH / 2, center[1]], [center[0] + self.SYMBOL_WIDTH / 2, center[1]], self.STRIPE_THICKNESS)
        elif shading == "outlined":
            pygame.draw.rect(self.screen, color, [x, y, self.SYMBOL_WIDTH, self.SYMBOL_HEIGHT], self.OUTLINE_THICKNESS)


    def __draw_diamond(self, center, color, shading):
        corners = [[center[0], center[1] + self.SYMBOL_HEIGHT / 2],
                   [center[0] + self.SYMBOL_WIDTH / 2, center[1]],
                   [center[0], center[1] - self.SYMBOL_HEIGHT / 2],
                   [center[0] - self.SYMBOL_WIDTH / 2, center[1]]]

        if shading == "solid":
            pygame.draw.polygon(self.screen, color, corners)
        elif shading == "striped":
            pygame.draw.polygon(self.screen, color, corners, self.OUTLINE_THICKNESS)
            # TODO: Add stripes
            pygame.draw.line(self.screen, color, [center[0] - self.SYMBOL_WIDTH / 2, center[1]], [center[0] + self.SYMBOL_WIDTH / 2, center[1]], self.STRIPE_THICKNESS)
        elif shading == "outlined":
            pygame.draw.polygon(self.screen, color, corners, self.OUTLINE_THICKNESS)

    def __show_score(self):
        # Draw background
        self.screen.fill(self.BG_COLOR)

        # Update screen
        pygame.display.update()