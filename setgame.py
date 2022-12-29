import random

class SetGame:
    """
    A game of set consists of a deck of unique cards and a number of
    cards on the table.
    """
    # cards_in_deck = []
    # cards_on_table = []

    # selected_indices = []
    # taken_sets = []

    def __init__(self):
        """
        Initializes a new game of set by creating a new deck of cards
        and placing 12 of them on the table.
        """
        self.cards_in_deck = []
        self.cards_on_table = []

        self.selected_indices = []
        self.taken_sets = []

        # Create a deck of 81 unique cards
        for shape in range(3):
            for color in range(3):
                for number in range(3):
                    for shading in range(3):
                        new_card = (shape, color, number, shading)
                        self.cards_in_deck.append(new_card)

        # Shuffle the deck
        random.shuffle(self.cards_in_deck)

        # Move 12 cards from the deck to the table
        for i in range(12):
            self.cards_on_table.append(self.cards_in_deck.pop())

        # If there are no sets on the table, add three more cards at a time until there is
        while len(self.get_sets_on_table()) == 0:
            print("No set found, adding 3 new cards...")
            for i in range(3):
                self.cards_on_table.append(self.cards_in_deck.pop())

        print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈")
        print("Starting new game...")
        print("≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈≈")


    def get_cards_in_deck(self):
        return self.cards_in_deck


    def get_cards_on_table(self):
        return self.cards_on_table


    def get_taken_sets(self):
        return self.taken_sets


    def get_selected_indices(self):
        return self.selected_indices


    def is_selected(self, index):
        # Make sure that the index is an int
        if type(index) != int:
            print("Warning: is_selected() - index is not an int")
            return False

        return index in self.selected_indices


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
        if index >= len(self.cards_on_table):
            return False

        # Check if the index is not already selected
        if index in self.selected_indices:
            return False

        self.selected_indices.append(index)

        # If this is the third index selected, try to take the set
        if len(self.selected_indices) > 2:
            index_1 = self.selected_indices[0]
            index_2 = self.selected_indices[1]
            index_3 = self.selected_indices[2]
            taken_set = self.__try_take_set(index_1, index_2, index_3)

            if taken_set is None:
                print("Invalid set at positions", index_1, index_2, index_3)
            else:
                print("Found set", taken_set, "at", index_1, index_2, index_3)

            self.selected_indices.clear()

        return True


    def deselect_index(self, index):
        # Make sure that the index is an int
        if type(index) != int:
            print("Warning: deselect_index() - index is not an int")
            return False

        # Remove the index from selected indices and return True
        if index in self.selected_indices:
            self.selected_indices.remove(index)
            return True

        # If the index was not selected before, return False
        return False


    def print_game(self):
        print("Cards left in deck:", len(self.cards_in_deck))
        print("Sets found:", len(self.taken_sets))
        print("+----------------------------------------+")
        for i in range(4):
            print("|", self.cards_on_table[3*i], self.cards_on_table[3*i + 1], self.cards_on_table[3*i + 2], "|")
        print("+----------------------------------------+")


    def get_sets_on_table(self):
        found_sets = []

        for i in range(12):
            for j in range(i, 12):
                for k in range(j, 12):
                    # Make sure that all three incides are unique
                    if not self.__different_indices(i, j, k):
                        # print("The indices are not unique! Please choose three unique indices.")
                        continue

                    card_1 = self.cards_on_table[i]
                    card_2 = self.cards_on_table[j]
                    card_3 = self.cards_on_table[k]
                    found_set = (card_1, card_2, card_3)

                    # Make sure that the given cards form a set
                    if self.__is_set(card_1, card_2, card_3):
                        print("Set found on positions:", i, j, k, "Set is:", found_set)
                        found_sets.append(found_set)

        return found_sets


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

        # Make sure that all three incides are unique
        if not self.__different_indices(index_1, index_2, index_3):
            print("The indices are not unique! Please choose three unique indices.")
            return None

        card_1 = self.cards_on_table[index_1]
        card_2 = self.cards_on_table[index_2]
        card_3 = self.cards_on_table[index_3]
        taken_set = (card_1, card_2, card_3)

        # Make sure that the given cards form a set
        if not self.__is_set(card_1, card_2, card_3):
            # print("The given cards do not form a set, sorry...", taken_set)
            return None

        # print("You found a set, congratulations!", taken_set)
        self.taken_sets.append(taken_set)

        # Remove the cards at the given indices
        self.cards_on_table = [element for i,element in enumerate(self.cards_on_table) if i not in [index_1, index_2, index_3]]

        # If there are fewer than 12 cards left on the table, add 3 new cards
        if len(self.cards_on_table) < 12:
            for i in range(3):
                self.cards_on_table.append(self.cards_in_deck.pop())

        # If there are no sets on the table, add three more cards at a time until there is
        while len(self.get_sets_on_table()) == 0:
            for i in range(3):
                self.cards_on_table.append(self.cards_in_deck.pop())

        return taken_set
