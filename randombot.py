from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager

import numpy as np
from numpy import random
from time import sleep

from bot import Bot

import collections

WORD_LENGTH = 5
# ALLOWED_GUESSES = 6

GREEN = 'g'
YELLOW = 'y'
GRAY = 'a'

class RandomBot(Bot):

    """
    A bot that makes random guessed-attempts

    Method
    ------
    play_worlde(self)
        Opens web browser, navigates to NYT Wordle site, and proceeds to make 
        six random guessed-attempts.

    """

    def make_random_guess(self):
        """
        Generates random guess from list of valid guesses

        """
        # self.wordle_guesses = np.loadtxt('wordle-guesses.txt', dtype = str)

        guess_idx = random.randint(low = 0, high = len(self.state))
        guess = self.state[guess_idx]
        self.actions.send_keys(guess)
        self.actions.send_keys(Keys.RETURN)
        self.actions.perform()
    
    def get_pattern(self, guess, solution):
        """Returns a wordle pattern for a guess given a target solution."""
        pattern = ""
        for i in range(WORD_LENGTH):
            # Letter is at the right spot
            if guess[i] == solution[i]:
                pattern += GREEN
            # Letter is not in the word
            elif guess[i] not in solution:
                pattern += GRAY
            else:
                # Look ahead and count the number of greens of that letter 
                n = 0
                for j in range(i + 1, WORD_LENGTH):
                    if (solution[j] == guess[i]) and (solution[j] == guess[j]):
                        n += 1
                # Count the number of occurences of that letter so far
                n += collections.Counter(guess[:i])[guess[i]] + 1
                # If the solution has less than n of that letter, add a gray
                if n > collections.Counter(solution)[guess[i]]:
                    pattern += GRAY
                else:
                        pattern += YELLOW

        return pattern
    
    def matches_pattern(self,word, guess, pattern):
        """Check whether a word matches a pattern gotten from an earlier guess."""
        return (self.get_pattern(guess, word) == pattern)
    
    def filter_words(self,words, guess, pattern):
        """Filter out any words that do not match a pattern from an earlier guess."""
        for word in words.copy():
            if not self.matches_pattern(word, guess, pattern):
                index = np.argwhere(words==word)
                # words.remove(word) # Numpy Array
                words = np.delete(words, index)
        return words


    def evaluate_guess(self, idx):
        """
        Evaluates the quality of guess at time step `idx` through simple scoring metric

        Scoring system:
            (1) Each letter of an attempt can take on three values: 'correct', 'present', 'absent'
                --> 'correct' : letter is in answer and at correct position
                --> 'present' : letter is in answer but at incorrect position
                --> 'absent'  : letter is not in answer
            (2) Assign each label an integer value
                --> 'correct' : 2
                --> 'present' : 1
                --> 'absent'  : 0
            (3) Score an attempt by evaluating each letter, multiply by coresponding label-integer, sum and 
                divide by 10. 
                --> Maximum score is 1.0 (all letters correct)
                --> Minimum score is 0.0 (no letters in answer)

        Parameters
        ----------
        idx : int
            integer indicating attempt number

        Returns
        -------
        correctness : float
            ratio describing quality of attempt
        
        """

        # Interpret gameboard
        game_app = self.driver.find_element(By.TAG_NAME , 'game-app')
        game_rows = self.driver.execute_script("return arguments[0].shadowRoot.getElementById('board')", game_app).find_elements(By.TAG_NAME, 'game-row')
        game_tiles = self.driver.execute_script('return arguments[0].shadowRoot', game_rows[idx]).find_elements(By.CSS_SELECTOR , 'game-tile')

        # Quantize evaluation 
        eval_to_int = {
            'correct' : 2,
            'present' : 1,
            'absent'  : 0
        }

        current_state = self.state
        new_pat = ""
        guess = ""
        correctness = 0

        # Parse pattern
        for i, tile in enumerate(game_tiles):
            letter = tile.get_attribute('letter')
            eval = tile.get_attribute('evaluation')

            correctness+= eval_to_int[eval]

            guess +=letter
            # Letter is present and at exact position in answer
            if eval == 'correct':
                # Add words to new state with letter at position `i` in word
                # new_state = [word for word in current_state if word[i] == letter]
                new_pat +="g"
            # Letter is present in answer
            elif eval == 'present':
                # Add words to new state with letter in word
                # new_state = [word for word in current_state if letter in word]
                new_pat +="y"
            # Letter is not present in answer
            else:
            # Add words to new state without letter in word
                # new_state = [word for word in current_state if letter not in word ]
                new_pat +="a"
        
        correctness /= 10
        print('Correctness: {:.2f}'.format(correctness))

        self.pattern = new_pat
        self.state = self.filter_words(current_state,guess,self.pattern)

        # print(self.state,self.pattern)
        if self.pattern == "g"*5 :
            print("Word Found !! {}".format(guess))
            return 1
        return 0


        # # Evaluate guess
        # correctness = 0
        # for letter in letters:
        #     print(letter.get_attribute('evaluation'))
        #     correctness += eval_to_int[letter.get_attribute('evaluation')]
        

    def play_wordle(self):
        """
        Plays game of Wordle

        """

        # Open Wordle site
        self.open_wordle()

        # Make guesses
        for i in np.arange(6):
            self.make_random_guess()
            check = self.evaluate_guess(i)
            if check == 1:
                break
            sleep(5)

        # Quit
        sleep(3)
        self.driver.quit()
