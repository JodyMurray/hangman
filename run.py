import random
from words import words
import string

def get_valid_word(words):
    word = random.choice(words) 
    while '-' in word or ' ' in word:
        word = random.choice(words)

    return word.upper()


def hangman():
    word = get_valid_word(words)
    word_letters = set(word)
    alphabet = set(string.ascii_uppercase)
    used_letters = set() # user guesses


    # get user input
    while len(word_letters) > 0:
        # letters used
        print('\nYou have used these letters: ', ' '.join(used_letters))

        word_list = [letter if letter in used_letters else '-' for letter in word]
        print('\nCurrent word: ', ' '.join(word_list))

        user_letter = input('Guess a letter: ').upper()
        if user_letter in alphabet - used_letters:
            used_letters.add(user_letter)
            if user_letter in word_letters:
                word_letters.remove(user_letter)
                print('')

        elif user_letter in used_letters:
            print('\nYou have already guessed that letter. Please try again.')
    
        else:
            print('\nInvalid character')


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

