# spelling-bee
Recreating Sam Ezersky's New York Times Spelling Bee puzzle

# What Does This Project Do

Spelling Bee takes in no input.

It spits out:

- One primary letter and six secondary letters
- These letters are used to make a Spelling Bee-type puzzle
- An object containing all the words and the scores you would get if you came up with those words (scoring rubric)
- Scoring ranges based on the words that can be formed and their lengths (bonus goal)
- TUI for getting scored

# Constraints of the 7 Letters

- Must exist a pangram
- lower and upper bound on number of words
- for each word of length l, lower and upper bound

# Scoring

- 1 point for 4 letters
- n points for n letters, n>=5
- bonus of 7 for pangram
