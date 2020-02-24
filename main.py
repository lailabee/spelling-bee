from argparse import ArgumentParser

import tui.game
import tui.generator

def main():
    parser = ArgumentParser("Play SpellingBean and generate new " +
                            "SpellingBean puzzles to play")
    parser.add_argument("action",
                        choices=["play", "generate"])
    parser.add_argument("-f", "--file")

    a = parser.parse_args()

    if a.action == "play":
        tui.game.play(a.file)
    else:
        tui.generator.generate(a.file)

if __name__ == "__main__":
    main()