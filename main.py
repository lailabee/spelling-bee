import itertools
from argparse import ArgumentParser

import optimize

def play(filename=None):
    if filename:
        print("Filename supplied: {}".format(filename))
    print("Oh boy, playing the game!")

def _print_found_word(wordList):
    print("{} {}".format(wordList.pivot_letter, wordList.letters))

def _save_found_word(filename, wordList):
    with open(filename, 'a') as f:
        f.write("({},{})\n".format(wordList.pivot_letter, wordList.letters))

def generate(filename=None):
    if filename is None:
        filename = "pangrams.txt"
    try:
        for i in itertools.count():
            if i%10 == 0:
                print("You can exit any time with Ctrl-C.")
            wordList = optimize.find_word()
            _print_found_word(wordList)
            _save_found_word(filename, wordList)
    except KeyboardInterrupt:
        return

def main():
    parser = ArgumentParser("Play SpellingBean and generate new " +
                            "SpellingBean puzzles to play")
    parser.add_argument("action",
                        choices=["play", "generate"])
    parser.add_argument("-f", "--file")

    a = parser.parse_args()

    if a.action == "play":
        play(a.file)
    else:
        generate(a.file)

if __name__ == "__main__":
    main()