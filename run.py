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
    """
    Game structure with menu selection and validator.
    """
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
                continue
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


def get_valid_word():
    """
    function collects random word from selection of words in words.py
    and capitalizes the letter
    """
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()


# def level_selection_choice(min_word_length):
#     """
#     somthing
#     """
#     while True:
#         level_choice = int(input(
#             '\nPick a level:\n 1.Easy\n 2.Medium\n 3.Hard\n \n"))'))
#         print('\nPlease choose a difficulty mode: ')
#         try:
#             level_choice = int(min_word_length)
#             if level_choice == 1:
#                 min_word_length = [len(word) <= 5]
#             print("Easy Level")
#             return level_choice
#             continue
#             elif level_choice == 2:
#                 min_word_length = [len(word) < 10]
#                 return level_choice
#             elif level_choice == 3:
#                 min_word_length = [len(word) >= 10]
#                 break
#                 return level_choice
#             else:
#                 print("Please only enter 1, 2 or 3")
#             return level_choice

def get_min_word_length():
    """
    Choose length of word
    """
    while True:
        min_word_length = input(
            'What minimum word length do you want? [4-16] ')
        try:
            min_word_length = int(min_word_length)
            if 4 <= min_word_length <= 16:
                return min_word_length
            else:
                print('{0} is not between 4 and 16'.format(min_word_length))
        except ValueError:
            print('{0} is not an integer between 4 and 16'.format(
                min_word_length))


def game():
    """
    Starts the game, collects user letter and shows this along with print 
    statements showing if you guessed wrong or input an invalid letter
    """
    word = get_valid_word()
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # user guesses
    min_word_length = get_min_word_length()

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
        return True


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

    # values = get_score_name

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


def update_high_score_sheet():
    """
    In this function, create a list with the score and full name after validation,
    then add it to the google sheets using "googlesheets.append_row(list)".
    First ensure full functionality of program:
    Level selection still isn´t working well. Once fixed, move onto google sheets.
    """

    # Add list to show to user: score and full name
    # googlesheets.append_row(list) to add row to google sheets


def run_game():
    """
    Order of game functions
    """

    user_valid_words = get_valid_word()
    level_choice = level_selection_choice()
    hangman_game = game()

    get_name = get_score_name()


if __name__ == "__main__":
    main()
