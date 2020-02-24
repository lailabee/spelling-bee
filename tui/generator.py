import itertools
import optimize

def _print_found_word(wordList):
    print("{} {}".format(wordList.pivot_letter, wordList.letters))

def _save_found_word(filename, wordList):
    with open(filename, 'a') as f:
        f.write("({},{})\n".format(wordList.pivot_letter, wordList.letters))

def generate(filename=None):
    if filename is None:
        filename = "puzzles.txt"
    try:
        for i in itertools.count():
            if i%10 == 0:
                print("You can exit any time with Ctrl-C.")
            wordList = optimize.find_word()
            _print_found_word(wordList)
            _save_found_word(filename, wordList)
    except KeyboardInterrupt:
        return