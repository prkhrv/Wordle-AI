# Wordle AI Solver

<img src="https://github.com/prkhrv/Wordle-AI-Solver/blob/main/screenshots/wordle-gif.gif" height="400">&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;

## Introduction

The goal is to construct an intelligent agent that can solve the wordle problem with the fewest possible attempts. Additionally, the AI must follow specific guidelines. 
  1. The AI should not know the correct response ahead of time. 
  2. The AI should use no predetermined best initial guess terms.
  3. The AI should use the correct discovered letters in the future iteration.

## Initial Approach
Our first strategy was to use a predetermined word as our first guess, then filter the best guess by using the feedback as input to filter the best guess.

### Console
<img src="https://github.com/prkhrv/Wordle-AI-Solver/blob/main/screenshots/Screenshot%202022-05-04%20031749.png" height="200">&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;

### Output
<img src="https://github.com/prkhrv/Wordle-AI-Solver/blob/main/screenshots/Screenshot%202022-05-04%20032110.png" height="400">&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;

## Problems With this Approach
* This method works as planned, but it does not provide the automation that an intelligent agent would provide.
* On the other hand, every time it makes an estimate, it requires a manual response as input from the user. 
* This strategy, however, violates Rule #3. The correct preceding letters 'R', 'A,' and 'T' are not included in the second guess.
* As an initial guess, it likewise utilizes a pre-determined word. ORATE will always be the first word in each game. As a result, it is always the search tree's root node.

## Final Solution
In our final solution, we attempted to address all of the shortcomings in our first approach by incorporating a selenium automation layer that handles automated input and output. Also, the new algorithm starts with a random word (non-heuristic), then finds the best possible word based on game feedback, and then it performs the heuristic search to get the best possible word.

* This approach is entirely automated.
* It makes use of both heuristic and non-heuristic search techniques.
* It also adheres to all of the game's rules.
* It Follows the Hard level Criteria of the game.

## Demo

<img src="https://github.com/prkhrv/Wordle-AI-Solver/blob/main/screenshots/demo-gif.gif" height="400">&nbsp;   &nbsp;   &nbsp;   &nbsp;   &nbsp;


## Library Dependencies:
* NumPy
* Selenium (4.1.0)
* webdriver-manager

## Install dependencies

```
pip install -r requirements.txt
```

## Run Local:
* `python playwordle.py`

## Credits
* Prakhar Varshney 
* Nyrika Bhargavaram Renuka


