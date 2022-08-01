import random
from words import words
import string

"""
def start_menu():
    
    Displays the navigation to start a game,
    view high scores or quit.

    nl_1 = '\n'
    nl_2 = '\n' * 2
    clear_terminal()
    print(f"{'  Main Menu  ':}")
    print(f"{' 1: Play Game ':}")
    print(f"{' 2: View High Scores ':")
    print(f"{' 3: QUIT ':}")

    while True:
        player_menu_selection = input(" " * 21 +
                                      "Please make a choice (1, 2,"
                                      "or 3): \n" + ' ' * 39)
        if player_menu_selection == '1':
            main()
            word = get_valid_word(words)
            play(word)
            while input(" " * 20 +
                        "Would you like to play again? (Y/N) \n" +
                        " " * 39).upper() == "Y":
                word = get_valid_word(words)()
                play(word)
                clear_terminal()
            menu()
        elif player_menu_selection == '2':
            display_highscores()
            menu()
        elif player_menu_selection == '3':
            sys.exit()
        else:
            clear_terminal()
            print('\n' * 3)
            print(f"{'  Main Menu ! ':*}")
            print(f"{' 1: Play Hangman ':}")
            print(f"{' 2: View High Scores ':}")
            print(f"{' 3: QUIT ':}")
            print('{:^80}'.format("Sorry " + player_menu_selection +
                                  " is an invalid option"))
start_menu()"""

hang_images = {
    0: """
            ___________
            | /        | 
            |/        ( )
            |          |
            |         / \\
            |
        """,
    1: """
            ___________
            | /        | 
            |/        ( )
            |          |
            |         / 
            |
        """,
    2: """
            ___________
            | /        | 
            |/        ( )
            |          |
            |          
            |
        """,
    3: """
            ___________
            | /        | 
            |/        ( )
            |          
            |          
            |
        """,
    4: """
            ___________
            | /        | 
            |/        
            |          
            |          
            |
        """,
    5: """
            ___________
            | /        
            |/        
            |          
            |          
            |
        """,
    6: """
            |
            |
            |
            |
            |
        """,
    7: "",
}

def get_valid_word(words):
    """
    function collects random word from selection of words in words.py
    and capitalizes the letter
    """
    word = random.choice(words) 
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()

# define game 
def main():
    """
    Starts the game, collects user letter and shows this along with print 
    statements showing if you guessed wrong or input an invalid letter
    """
    word = get_valid_word(words)
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set() # user guesses

    lives = 7

    # get user input
    while len(word_letters) > 0 and lives > 0:
        # letters used
        print('\nYou have', lives, 'lives left and you have used these letters: ', ' '.join(used_letters))

        word_list = [letter if letter in used_letters else '-' for letter in word]
        print('\nCurrent word: ', ' '.join(word_list))

        user_letter = input('Guess a letter: ').upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print('')

            # tells user whether letter is correct or incorrect
            else:
                lives = lives - 1
                print('\nYour letter,', user_letter, 'is not in the word.')
                print(hang_images[lives])
            if user_letter in word:
                used_letters.update(user_letter)
                print('\nGood guess,', user_letter, 'is in the word!')
                print(hang_images[lives])

        # tells user if they have already guessed a letter 
        # or if they input an incorrect character
        elif user_letter in used_letters:
            print('\nYou have already guessed that letter. Please try again.')
            print(hang_images[lives])
    
        else:
            print('\nInvalid character')
            print(hang_images[lives])

    # tells user whether they guessed the complete word or not
    if lives == 0:
            print('Sorry, you died. The correct word was', word)
            
            
        
    else:
        print('\nYou guessed the word', word, '!! WINNER!')
        


print("\nWelcome to Hangman!")

# Enter game loop
while True:
    user_input = input("\nEnter y/n to begin: ")
    if user_input == "y":
        main()
        continue
    elif user_input == "n":
        break
    else:
        print("\nEnter either y/n")

print(user_input)
main()

