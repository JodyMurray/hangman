import random
import sys
import string
from google.oauth2.service_account import Credentials
import gspread
from rules import rules_page
from words import words


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SCORESHEETS = GSPREAD_CLIENT.open('high-scores').worksheet('scores')


def display_highscores():
    """
    clears the terminal and displays the highscores
    from the spreadsheet.
    """


def update_scores(new_score):
    """
    updates the highscores to the spreadsheet.
    """


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


def main():

    while True:
        print("Welcome to HANGMAN!\n")
        print("1: Play GAME.")
        print("2: See RULES.")
        print("3: See HIGHSCORES.")
        print("4: EXIT application.")
        user_input = int(input("\nPlease enter your choice: "))
        try:
            if user_input == 1:
                # Enter main gameplay
                run_game()
                continue
            elif user_input == 2:
                rules_page()
            elif user_input == 3:
                print(scores)
            elif user_input == 4:
                sys.exit()
        except ValueError:
            print("\nInvalid input. Please enter 1, 2, 3 or 4.")
            continue
        else:
            continue


def get_valid_word(words):
    """
    function collects random word from selection of words in words.py
    and capitalizes the letter
    """
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()


def level_selection_choice():
    """
    does something
    """
    print("\nPlease choose a difficulty mode: ")
    user_choice = int(
        input("\nPick a level:\n 1.Easy\n 2.Medium\n 3.Hard\n \n"))

    if user_choice == 1:
        easy_mode = [word for word in words if len(word) <= 5]
        print("\nLevel: Easy level")
    elif user_choice == 2:
        medium_mode = [word for word in words if len(word) < 10]
        print("Level: Medium level")
    elif user_choice == 3:
        hard_mode = [word for word in words if len(word) >= 10]
        print("Level: Hard level")
    else:
        print("Please only enter 1, 2 or 3")

    return user_choice


def game():
    """
    Starts the game, collects user letter and shows this along with print 
    statements showing if you guessed wrong or input an invalid letter
    """
    word = get_valid_word(words)
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # user guesses

    lives = 7

    # get user input
    while len(word_letters) > 0 and lives > 0:
        # letters used
        print('\nYou have', lives,
              'lives left and you have used these letters: ', ' '.join(used_letters))

        word_list = [
            letter if letter in used_letters else '-' for letter in word]
        print('\nCurrent word: ', ' '.join(word_list))

        user_letter = input('\nGuess a letter: ').upper()
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


def run_game():
    user_valid_words = get_valid_word
    user_level_select = level_selection_choice()
    hangman_game = game()


if __name__ == "__main__":
    main()