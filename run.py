import sys
import gspread
import re
from google.oauth2.service_account import Credentials
from words import words
import string
import random
from rules import rules_page


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('high-scores2')
High_Scores = SHEET.worksheet('scores')
Scores = High_Scores.get_all_values()

def update_worksheet(Scores, worksheet):
    """
    Receives a list of integers to be insterted into a worksheet
    Update the relevant worksheet with the data provided. 
    """
    print(f"Updating {worksheet} scores worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(Scores)
    print(f"{worksheet} worksheet updated successfully\n")
    score_data = get_score_name()
    update_worksheet(score_data, "scores")


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
        print("Welcome to HANGMAN! \n")
        print("1: Play GAME. \n")
        print("2: See RULES. \n")
        print("3: See HIGHSCORES. \n")
        print("4: EXIT application. \n")
        user_input = int(input("Please enter your choice: \n"))
        try:
            if user_input == 1:
                # Enter main gameplay
                run_game()
                continue
            elif user_input == 2:
                rules_page()
            elif user_input == 3:
                print(Scores)
                break
            elif user_input == 4:
                sys.exit()
        except ValueError:
            print("Invalid input. Please enter 1, 2, 3 or 4. \n")
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
    Selects a level difficulty mode for the game, based on user input
    """
    
    print("Please choose a difficulty mode: \n")
    user_choice = int(
        input("Pick a level:\n 1.Easy\n 2.Medium\n 3.Hard\n"))

    if user_choice == 1:
        easy_mode = [word for word in words if len(word) <= 5]
        print("Level: Easy level \n")
    elif user_choice == 2:
        medium_mode = [word for word in words if len(word) < 10]
        print("Level: Medium level \n")
    elif user_choice == 3:
        hard_mode = [word for word in words if len(word) >= 10]
        print("Level: Hard level \n")
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


def get_score_name():
    """
    Get name for high scores
    """
    while True: 

        print("Please enter name: \n")
        print("Example: Yoda Murray. \n")

        user = input("Enter your name: \n")

        if validate_name(user):
            break

    # worksheet_to_update = Scores
    # worksheet_to_update.append_row(Scores)

    return user


def validate_name(user):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """

    values = get_score_name

    # try:
    #     [str(value) for value in values]
    #     if len(values) != 6:
    #         raise ValueError(
    #             f"Exactly 6 values required, you provided {len(values)}"
    #         )
    # except ValueError as e:
    #     print(f"Invalid data: {e}, please try again.\n")
    #     return False

    # return True

    regex_name = re.compile(r'^([a-z]+)( [a-z]+)*( [a-z]+)*$', re.IGNORECASE)

    res = regex_name.search(user)

    if res:
        print(f"Welcome, {user}!")
        return True
    else:
        print("Invalid. Please enter a valid name.")
        return False


def run_game():

    """
    Order of game functions
    """

    user_valid_words = get_valid_word(words)
    level_mode = level_selection_choice()
    hangman_game = game()
    get_name = get_score_name()
    # score_data = validate_name()


if __name__ == "__main__":
    main()
