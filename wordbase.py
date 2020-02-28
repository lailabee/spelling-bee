import itertools
import pickle
from collections import Counter, namedtuple

Word = namedtuple("Word", ["str", "set"])
def newWord(str_):
    """Given a pangram as a string, return a Word representing it."""
    return Word(str_, frozenset(str_))

lowercase = frozenset("abcdefghijklmnopqrstuvwxyz")

class Pangram:
    """Represents a set of seven letters, one of which is the pivot letter.
    Allows access to a list of all words that can be spelled with the 
    pangram, as well as a count of the lengths of all those words.

    A pangram object is created with:
    Pangram(wordBase, word, pivot_letter, word_lengths)
    This will mostly be used when loading a Pangram whose word_lengths have
    previously been computed. If you don't already know those numbers,
    you probably want to use Pangram.from_word(), which will calculate
    it at instantiation.

    Instance variables:
    Pangram.word -- a Word object representing the 7 letters
    Pangram.pivot_letter -- the pivot letter
    Pangram.word_lengths -- a Counter mapping word lengths to a count of 
                            how many words of that length can be spelled 
                            with this pangram. For example, a pangram that
                            can spell six 4-letter words and seven 5-
                            letter words would have the counter:
                            { 4: 6,
                              5: 7 }
    """
    def __init__(self, wordBase, word, pivot_letter, word_lengths):
        """Create a Pangram instance representing the given seven letters.
        Note that word lengths are *not* computed, they must be supplied.
        
        Function arguments:
        wordBase -- the WordBase instance that this pangram came from
        word -- a Word instance holding the 7 letters
        pivot_letter -- the pivot letter
        word_lengths -- a mapping of word length -> number of words of that
                                                    length that can be made
                                                    from the pangram
        """
        self.wordBase = wordBase
        self.word = word
        self.pivot_letter = pivot_letter
        self.word_lengths = word_lengths

    @classmethod
    def from_word(cls, wordBase, word, pivot_letter):
        """Return a pangram instance representing the given seven letters.
        Computes word_lengths by exhaustively searching for subwords in
        the given wordBase.

        Function arguments:
        wordBase -- the WordBase instance that this pangram came from
        word -- a Word instance holding the 7 letters
        pivot_letter -- the pivot letter
        """
        word_lengths = wordBase.get_word_lengths(word, pivot_letter)
        return cls(wordBase, word, pivot_letter, word_lengths)

    @classmethod
    def from_word_all_pivots(cls, wordBase, word):
        """Iterate over all letters in word, and return a list of the
        from_word for each pivot letter.
        """
        return [cls.from_word(wordBase, word, pivot) for pivot in word.set]


class WordBase:
    """Represents the full dictionary of guessable words, and holds
    information about all pangrams (words containing exactly 7 unique,
    optionally repeatable letters). Though a WordBase can be created by 
    its init method, it is more likely that you'll want to:
        (a) Build the Wordbase from a word file, using
            WordBase.from_wordfile(), or
        (b) Load a previously-built WordList from a file, using
            WordBase.from_pickle()
    WordBase can also store, for each pangram, information on how many
    words of varying lengths can be created from the letters in that
    pangram--that is, create a Pangram instance for each one. Because
    this is computationally intensive, however, it isn't done on
    instantiation. Instead, you must call get_pangrams(), which performs
    the search and then saves the result for future calls.

    Instance variables:
    WordBase.words -- a list of all words in the dictionary
    WordBase.candidate_pangrams -- a list of all words spelled with
                                   exactly seven letters
    """
    def __init__(self, words, candidate_pangrams, _pangrams):
        self.words = words
        self.candidate_pangrams = candidate_pangrams
        self._pangrams = _pangrams

    @classmethod 
    def from_wordfile(cls, path="/usr/share/dict/words"):
        """Given the path to a file following the Linux wordfile format (one
        word per line), return a WordBase instance representing those words.

        If no path is specified, the default location of
        /usr/share/dict/words will be used.
        """
        with open(path) as f:
            words = f.readlines()

        words = [word[:-1] for word in words]    # strip newlines
        words = [word for word in words if len(word) >= 4]
        words = [newWord(word) for word in words]
        words = [word for word in words if word.set <= lowercase]
        words = [word for word in words if len(word.set) <= 7]
        candidate_pangrams = [word for word in words if len(word.set) == 7]

        return cls(words, candidate_pangrams, None)

    @classmethod
    def from_pickle(cls, path="wordbase.pickle"):
        """Unpickle a pickled WordBase"""
        with open(path, 'rb') as f:
            in_ = pickle.load(f)
            return cls(*in_)

    def to_pickle(self, path="wordbase.pickle"):
        """Save the wordbase to disk."""
        out = (self.words, self.candidate_pangrams, self._pangrams)
        with open(path, 'wb') as f:
            pickle.dump(out, f)

    def get_subwords(self, word, pivot_letter):
        """Return a list of all words that can be made from letters of the 
        given word.

        Function arguments:
        word -- a Word instance representing the pangram
        pivot_letter -- the pivot letter
        """
        return [w for word in wordbase if pivot in w.set
                                          and w.set <= word.set]

    def get_word_lengths(self, word, pivot_letter):
        """Return a Counter mapping word lengths to the number of subwords
        of that length that can be made from the given pangram. For
        example, if the given word can make:
            -  7 words of length 4
            - 12 words of length 5
            -  9 words of length 6
            -  1 word  of length 7 (itself)
        The returned counter will read:
            {4:  7,
             5: 12,
             6:  9,
             7:  1}

        Function arguments:
        word -- a Word instance representing the pangram
        pivot_letter -- the pivot letter
        """
        lengths = Counter()
        for subword in subwords(wordbase, word, pivot):
            lengths[len(subword.str)] += 1
        return lengths

    def get_all_pangrams(self, recalculate=False):
        """Iterates over all the candidate pangrams in this wordBase and
        returns a Pangram object for each pivot letter for each candidate
        pangram. This operation takes multiple hours the first time, but
        is cached for future calls. You can force a re-calculation by
        setting the optional parameter to True.
        """
        if self._pangrams and not recalculate:
            return self._pangrams
        else:
            self._pangrams = list(itertools.chain(
                *[Pangram.from_word_all_pivots(self, word) 
                  for word in candidate_pangrams]))
            return self._pangrams