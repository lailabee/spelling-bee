from wordbase import WordBase, WordList

def score(word):
    #TODO: implement pangram bonus
    return (0 if len(word) < 4
                else 1 if len(word) == 4
                else len(word))

class GameState:
    def __init__(self, wordList):
        self.wordList = wordList
        self.score = 0
        self.pivot_letter = wordList.pivot_letter.lower()
        self.letters = wordList.letters.lower()
        self.possible_words = set(wordList.get_word_list())
        self.guessed = set()

    def guess_word(self, word):
        if word not in self.possible_words:
            return "not a word"
        elif word in self.guessed:
            return "already guessed"
        else:
            self.guessed.add(word)
            self.score += score(word)
            return score(word)

def _pop_puzzle(filename):
    """Yank the bottom line off the specified file, and store it in a trash
    file. Return a tuple with (pivot_letter, letters).
    """
    return ("s", "reptils")

def _read(state):
    return input("> ").lower()

def _evaluate(input_, state):
    """Evaluates the user input and updates state accordingly. Returns any 
    state changes.
    """
    res = state.guess_word(input_)
    if res == "not a word":
        return "Not a word."
    elif res == "already guessed":
        return "You already got that one!"
    else:
        return "Nice! +{}".format(res)

def _print(change, state):
    """Notifies the user of current game state."""
    print("----")
    if change:
        print("{}".format(change))
    print("Score: {}".format(state.score))
    print("{} {}".format(state.pivot_letter,
                         "".join(c for c in state.letters 
                                    if c != state.pivot_letter)))

def game_loop(state):
    _print(None, state)
    while True:
        input_ = _read(state)
        change = _evaluate(input_, state)
        _print(change, state)

def play(filename=None):
    if filename is None:
        filename = "pangrams.txt"
    wordBase = WordBase()
    pivot_letter, letters = _pop_puzzle(filename)
    wordList = wordBase.get_word_list(pivot_letter, letters)
    gameState = GameState(wordList)
    game_loop(gameState)