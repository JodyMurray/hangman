import sys
import string
import random
import re
import gspread
from google.oauth2.service_account import Credentials
from termcolor import colored
from words import words
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

def update_worksheet(High_Scores, worksheet):
    """
    Receives a list of integers to be insterted into a worksheet
    Update the relevant worksheet with the data provided.
    """
    print(f"Updating {worksheet} scores worksheet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(High_Scores)
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
        print(colored("\nWelcome to HANGMAN! \n", 'green'))
        print(colored("1: Play GAME. \n", 'yellow'))
        print(colored("2: See RULES. \n", 'yellow'))
        print(colored("3: See HIGHSCORES. \n", 'yellow'))
        print(colored("4: EXIT application. \n", 'yellow'))
        user_input = int(input(colored(
            "Please enter your choice: \n\n", 'white')))

        try:
            if user_input == 1:
                print(colored("\n\nEntering Game!\n", 'red'))
                # Enter main gameplay
                run_game()
                sys.exit()
            elif user_input == 2:
                rules_page()
                continue
            elif user_input == 3:
                print("\n")
                print(colored(Scores, 'cyan'))
                print("\n")
                print("-" * 80)
                print('\n')
                input(colored(
                    " " * 24 + "Press Enter to return to the main menu \
                        \n" + ' ' * 50, 'white'))
                main()
                break
            elif user_input == 4:
                print("\n")
                print(colored("Leaving application...", 'blue'))
                print("\n")
                sys.exit()
        except ValueError:
            print(colored("Invalid input. Please enter 1, 2, 3 or 4. \n", ))
            continue
        else:
            continue

def game():
    """
    Starts the game, collects user letter and shows this along with print
    statements showing if you guessed wrong or input an invalid letter
    """
    get_name = get_score_name()
    
    word = get_valid_word()
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set()  # user guesses

    lives = 7

    # get user input
    while len(word_letters) > 0 and lives > 0:
        # letters used
        print(colored(
            '\n\nYou have', 'magenta'), colored(lives, 'magenta'),
              colored(
                'lives left and you have used these letters: ', 'magenta'
                ), colored(' '.join(used_letters)))

        word_list = [
            letter if letter in used_letters else '-' for letter in word]
        print(colored('\n\nCurrent word: ', 'white'), (' '.join(word_list)))

        user_letter = input(colored('\n\nGuess a letter: ', 'cyan')).upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print('')

            # tells user whether letter is correct or incorrect
            else:
                lives = lives - 1
                print(colored(
                    '\nYour letter,', 'blue'), colored(
                        user_letter, 'white'), colored(
                        'is not in the word.', 'blue'))
                print(colored(hang_images[lives], 'white'))
            if user_letter in word:
                used_letters.update(user_letter)
                print(
                    colored('\nGood guess,', 'green'), colored(
                        user_letter, 'white'), colored(
                        'is in the word!', 'green'))
                print(colored(hang_images[lives], 'white'))

        # tells user if they have already guessed a letter
        elif user_letter in used_letters:
            print(colored(
                '\nYou have already guessed that letter. Please try again.\
                    ', 'red'))
            print(colored(hang_images[lives], 'white'))
        # or if they input an incorrect character
        else:
            print(colored('\nInvalid character', 'red'))
            print(colored(hang_images[lives], 'white'))

    # tells user whether they guessed the complete word or not
    if lives == 0:
        print(
            colored('Sorry, you died. The correct word was', 'blue'), colored(
                word, 'white'))
        print("\n")
        input(colored(" " * 24 + colored(
            "Press Enter to return to the menu \n", 'green') + ' ' * 24))
        main()

    else:
        print(
            colored('\nYou guessed the word', 'yellow'), colored(
                word, 'white'), colored('!! WINNER!', 'yellow'))
        worksheet_update = update_high_score_sheet(get_name)
        print(colored(Scores, 'magenta'))
        print("\n")
        print(colored(" " * 50 + get_name, 'magenta'))
        print("\n")
        print("-" * 90)
        print("\n")
        return True


def validate_name(user_name):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """

    regex_name = re.compile(r'^([a-z]+)( [a-z]+)*( [a-z]+)*$', re.IGNORECASE)

    res = regex_name.search(user_name)

    if res:
        print(colored(f"\nWelcome, {user_name}!", 'yellow'))
        return True
    else:
        print(colored("\nInvalid. Please enter a valid name.\n", 'red'))
        return False


def get_valid_word():
    """
    function collects random word from selection of words in words.py
    and capitalizes the letter
    """
    word = random.choice(words)
    while '-' in word or ' ' in word:
        word = random.choice(words)
    return word.upper()


def get_score_name():
    """
    Get name for high scores entries
    """

    while True:

        print(colored("Please enter name: \n", 'white'))
        print(colored("Example: Yoda. \n", 'cyan'))

        user_name = input(colored("Enter your name: \n\n", 'white'))

        if validate_name(user_name):
            break

    return user_name


def update_high_score_sheet(get_names):
    """
    Get name and update to high scores
    """

    player_info_list = [get_names]

    screen_info = f"""
    Winner! \n
    {get_names}\n
    """

    print(colored(screen_info, 'cyan'))

    High_Scores.append_row(player_info_list)

    return player_info_list

def run_game():
    """
    Order of game functions
    """
    user_valid_words = get_valid_word()
    hangman_game = game()


if __name__ == "__main__":
    main()
