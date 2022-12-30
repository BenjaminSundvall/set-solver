import random
import time

class SetGame:
    """
    A game of set consists of a deck of unique cards and a number of
    cards on the table.
    """
    __start_time = None
    __is_running = False

    __cards_in_deck = []
    __cards_on_table = []
    __sets_on_table = []

    __selected_indices = []
    __taken_sets = []

    def __init__(self):
        """
        Initializes a new game of set by creating a new deck of cards
        and placing 12 of them on the table.
        """
        self.reset_game()


    def reset_game(self):
        self.__start_time = time.time()
        self.__is_running = True

        self.__cards_in_deck = []
        self.__cards_on_table = []
        self.__sets_on_table = []

        self.__selected_indices = []
        self.__taken_sets = []

        # Create a deck of 81 unique cards
        for shape in range(3):
            for color in range(3):
                for number in range(3):
                    for shading in range(3):
                        new_card = (shape, color, number, shading)
                        self.__cards_in_deck.append(new_card)

        # Shuffle the deck
        random.shuffle(self.__cards_in_deck)

        # If there are no sets on the table, add three more cards at a time until there is
        self.__refill_table()

        print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈")
        print("Starting new game...")
        print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈")


    def is_running(self):
        return self.__is_running


    def get_cards_in_deck(self):
        return self.__cards_in_deck


    def get_cards_on_table(self):
        return self.__cards_on_table


    def get_sets_on_table(self):
        return self.__sets_on_table


    def get_taken_sets(self):
        return self.__taken_sets


    def get_selected_indices(self):
        return self.__selected_indices


    def is_selected(self, index):
        # Make sure that the index is an int
        if type(index) != int:
            print("Warning: is_selected() - index is not an int")
            return False

        return index in self.__selected_indices


    def select_index(self, index):
        """
        Adds index to list of selected indices. Returns True if
        successful and False if the index is not selectable.
        """

        # Make sure that the index is an int
        if type(index) != int:
            print("Warning: select_index() - index is not an int")
            return False

        # Check if the index a avalid number
        if index >= len(self.__cards_on_table):
            return False

        # Check if the index is not already selected
        if index in self.__selected_indices:
            return False

        self.__selected_indices.append(index)

        # If this is the third index selected, try to take the set
        if len(self.__selected_indices) > 2:
            index_1 = self.__selected_indices[0]
            index_2 = self.__selected_indices[1]
            index_3 = self.__selected_indices[2]

            taken_set = self.__try_take_set(index_1, index_2, index_3)

            self.__selected_indices.clear()

        return True


    def deselect_index(self, index):
        # Make sure that the index is an int
        if type(index) != int:
            print("Warning: deselect_index() - index is not an int")
            return False

        # Remove the index from selected indices and return True
        if index in self.__selected_indices:
            self.__selected_indices.remove(index)
            return True

        # If the index was not selected before, return False
        return False


    def print_game(self):
        print("\nCards left in deck:", len(self.__cards_in_deck))
        print("Sets found:", len(self.__taken_sets))
        print("+----------------------------------------+")
        for i in range(4):
            print("|", self.__cards_on_table[3*i], self.__cards_on_table[3*i + 1], self.__cards_on_table[3*i + 2], "|")
        print("+----------------------------------------+")


################################################################################
#  Private functions                                                           #
################################################################################


    def __different_indices(self, index_1, index_2, index_3):
        """
        Returns True if the three indices are unique, otherwise false.
        """
        return not ((index_1 == index_2) or (index_1 == index_3) or (index_2 == index_3))


    def __is_set(self, card_1, card_2, card_3):
        """
        Returns True if the cards at the three given positions form a
        set, otherwise False. If two indices are the same, a set can not
        be formed and the function returns False.
        """

        # Check if the cards at the given positions form a set
        for feat_num in range(4):
            if (card_1[feat_num] == card_2[feat_num]) and (card_1[feat_num] == card_3[feat_num]) and (card_2[feat_num] == card_3[feat_num]):
                # print("Features in position", feat_num, "are all the same!")
                pass
            elif (card_1[feat_num] != card_2[feat_num]) and (card_1[feat_num] != card_3[feat_num]) and (card_2[feat_num] != card_3[feat_num]):
                # print("Features in position", feat_num, "are all different!")
                pass
            else:
                # print("Features in position", feat_num, "only partially match! The cards don't form a set!")
                return False    # If a feature is not ok, return False...
        return True     # If all features are ok, return True...


    def __try_take_set(self, index_1, index_2, index_3):
        """
        Tries to take the set on the given indices. Returns a tuple of
        cards in the taken set. Returns None if the cards don't form a
        set.
        """
        print("Taking set at", index_1, index_2, index_3)

        # Make sure that all three incides are unique
        if not self.__different_indices(index_1, index_2, index_3):
            print("The indices are not unique! Please choose three unique indices.")
            return None

        card_1 = self.__cards_on_table[index_1]
        card_2 = self.__cards_on_table[index_2]
        card_3 = self.__cards_on_table[index_3]
        taken_set = (card_1, card_2, card_3)

        # Make sure that the given cards form a set
        if not self.__is_set(card_1, card_2, card_3):
            # print("The given cards do not form a set, sorry...", taken_set)
            print("INVALID SET! - Set:", taken_set)
            return None
        print("VALID SET! - Set:", taken_set)

        # print("You found a set, congratulations!", taken_set)
        self.__taken_sets.append(taken_set)

        # Remove the cards at the given indices
        self.__cards_on_table = [element for i,element in enumerate(self.__cards_on_table) if i not in [index_1, index_2, index_3]]

        # If there are no sets on the table, add three more cards at a time until there is
        self.__refill_table()

        return taken_set


    def __refill_table(self):
        # Make sure that there are at least 12 cards on the table
        while len(self.__cards_on_table) < 12:
            if not self.__cards_in_deck:
                break
            self.__cards_on_table.append(self.__cards_in_deck.pop())

        # If there are no sets on the table, add three more cards at a time until there is
        self.__find_sets_on_table()
        while len(self.__sets_on_table) == 0:
            if not self.__cards_in_deck:
                print("No more sets can be crated. Ending game...")
                self.__game_over()
                return
            print("No set found, adding 3 new cards...")
            for i in range(3):
                self.__cards_on_table.append(self.__cards_in_deck.pop())
            self.__find_sets_on_table()


    def __find_sets_on_table(self):
        print("Finding sets...")

        self.__sets_on_table = []
        number_of_cards_on_table = len(self.__cards_on_table)

        for i in range(number_of_cards_on_table):
            for j in range(i, number_of_cards_on_table):
                for k in range(j, number_of_cards_on_table):
                    # Make sure that all three incides are unique
                    if not self.__different_indices(i, j, k):
                        # print("The indices are not unique! Please choose three unique indices.")
                        continue

                    card_1 = self.__cards_on_table[i]
                    card_2 = self.__cards_on_table[j]
                    card_3 = self.__cards_on_table[k]
                    found_set = (card_1, card_2, card_3)

                    # If the cards form a set, add them to the sets on table
                    if self.__is_set(card_1, card_2, card_3):
                        print("Set found on positions:", i, j, k, "| Set is:", found_set)
                        self.__sets_on_table.append((i, j, k))

        print(len(self.__sets_on_table), "sets found!")


    def __game_over(self):
        game_time = int(time.time() - self.__start_time)
        self.__is_running = False
        print("Game over! You found", len(self.__taken_sets), "sets in", game_time, "seconds!")