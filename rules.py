from termcolor import colored


"""
Rules variable defined in list
"""


def rules_page():
    """
    Rules definition, making clear the rules of the game
    And press enter to go back to main menu.
    """
    print("-" * 80)
    print('\n')
    print(colored(" " * 30 + "Rules of the GAME", 'yellow'))
    rule_list = """
        \n1: The hangman should consist of a head, a body,
        2 arms, and 2 legs.
        \n2: If the player correctly
        guesses all of the letters
        before the hangman is complete, they win.
        \n3: If they loose lives, the drawing of the HANGMAN is complete
        and you lose.
        \n4: Make it to the Highscores board if you win!\n
    """
    print(colored(rule_list, 'cyan'))

    print(colored("-" * 80, 'white'))
    print('\n')
    input(colored(" " * 24 + "Press Enter to return to the menu \
        \n" + ' ' * 39, 'white'))
    SystemExit()
