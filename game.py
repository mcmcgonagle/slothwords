from words import get_random_word, correct_letters_place

def start_game():
    challenge_word = get_random_word()
    return challenge_word

def check_guess(x, challenge_word, guesses):
    win = False
    print(x)
    print(challenge_word)
    if win == False and guesses >= 6:
        print('You lose!')
        print('The word was ' + challenge_word)
        return "lose"
    if x == challenge_word:
        win = True
        print("You win!")
        return "win"
    else: 
        print('Wrong!')
        my_word = list(x)
        challenge_letters = list(challenge_word)
        print(my_word)
        print(challenge_letters)
        checked_guess = correct_letters_place(my_word, challenge_letters)
        print('You have ' + str(5 - guesses) + ' guesses left')
        print(checked_guess)
        return checked_guess
