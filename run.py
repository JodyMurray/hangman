import random
import sys
from words import words
import string


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

def menu():

    while True:
        print("Welcome to HANGMAN!")
        print("Pick 1 to play GAME.")
        print("Pick 2 to see RULES.")
        print("Or pick 3 to EXIT application.")
        user_input = int(input("Please enter your choice: \n"))
        try: 
            if user_input == 1:
                #Enter main gameplay
                main()
                continue
            elif user_input == 2:
                #Function to explain what hangman is
                break
            elif user_input == 3:
                sys.exit()
        except ValueError:
            print("Invalid input. Please enter 1, 2 or 3.")
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

    print("Please pick a difficulty mode.")
    user_choice = int(input("Pick a level:\n 1.Easy\n 2.Medium\n 3.Hard\n"))

    if user_choice == 1:
        level = "Easy"
    elif user_choice == 2:
        level = "Medium"
    elif user_choice == 3:
        level = "Hard"

    return user_choice

level = level_selection_choice()

def level_selection(user_choice):
    """
    Defines levels with length of words
    gives three choices of difficulty
    """


    if user_choice == "Easy":
        easy = [word for word in words if len(word) <= 5]
        print(f"{level}: Easy level")
        return easy
    elif user_choice == "Medium":
        Medium = [word for word in words if len(word) < 10]
        print(f"{level}: Medium level")
        return Medium
    elif user_choice == "Hard":
        hard = [word for word in words if len(word) >= 10]
        return hard
    else:
        print("Please only enter 1, 2 or 3")

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


def run_game():
    

