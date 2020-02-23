from argparse import ArgumentParser

def play(filename=None):
    if filename:
        print("Filename supplied: {}".format(filename))
    print("Oh boy, playing the game!")

def generate(filename=None):
    if filename:
        print("Filename supplied: {}".format(filename))
    print("Gee willikers, generating some words!")

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