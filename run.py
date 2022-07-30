import random
from words import words
import string

def get_valid_word(words):
    word = random.choice(get_min_word_length()) 
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()

def get_min_word_length():
    """Get user-inputted minimum word length for the game."""
    while True:
        min_word_length = input(
            'What minimum word length do you want? [4-16] ')
        try:
            min_word_length = int(min_word_length)
            if 4 < min_word_length <= 16:
                return min_word_length
            else:
                print('{0} is not between 4 and 16'.format(min_word_length))
        except ValueError:
            print('{0} is not an integer between 4 and 16'.format(
                min_word_length))
        

def hangman():
    word = get_valid_word(words)
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set() # user guesses
    min_word_length = get_min_word_length()

    lives = 6

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
            
            else:
                lives = lives -1
                print('\nWrong letter!')

        elif user_letter in used_letters:
            print('\nYou have already guessed that letter. Please try again.')
    
        else:
            print('\nInvalid character')
    
        if lives == 0:
            print('Sorry, you died. The correct word was', word)
        else:
            print('\nYou guessed the word', word, '!! WINNER!')


print("\nWelcome to Hangman!")


while True:
    user_input = input("\nEnter y/n to begin: ")
    if user_input=="y":
        hangman()
        continue
    elif user_input=="n":
        break
    else:
        print("\nEnter either yes/no")

print(user_input)
hangman()

