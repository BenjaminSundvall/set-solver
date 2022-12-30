from setgame import SetGame
from setgui import SetGUI


def play_cli_game():
    setgame = SetGame()

    exit = False

    while not exit:
        # Ask the player for three cards
        # print("\033c", end='')
        # os.system("clear")
        print("\n=======================================================\n")
        setgame.print_game()
        input_str = input("\n[t]ake a set, [f]ind all sets, [v]iew found sets, [q]uit, [r]eset game: ")

        # Handle special inputs
        if input_str == "q":
            print("Quitting game...")
            exit = True
        elif input_str == "r":
            print("Resetting game...")
            setgame = SetGame()
        elif input_str == "v":
            print("Viewing found sets...")
            for taken_set in setgame.get_taken_sets():
                print(taken_set)
        elif input_str == "f":
            print("Finding all sets...")
            found_sets = setgame.__find_sets_on_table()
            print("Found", len(found_sets), "sets!")
            print("Sets in the board:", found_sets)
        elif input_str == "t":
            print("Taking a set...")
            index_str = input("Please choose three positions on the form \"[0-11] [0-11] [0-11]\": ")
            # Convert the answer to three indices
            index_1, index_2, index_3 = [int(index) for index in index_str.split()]

            # See if those three cards form a set
            setgame.select_index(index_1)
            setgame.select_index(index_2)
            setgame.select_index(index_3)


def play_gui_game():
    setgame = SetGame()
    setgui = SetGUI(setgame)

    setgui.show()


if __name__=="__main__":
    # play_cli_game()
    play_gui_game()