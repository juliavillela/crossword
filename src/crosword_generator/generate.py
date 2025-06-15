from random import shuffle
from math import sqrt, ceil
from .constants import *
from .word_placement_grid import WordPlacementGrid

class CrosswordGenerator:
    """"
    Generates crossword puzzles by placing a list of words into a grid.

    The generator attempts to place words iteratively on a grid, starting with
    an initial size based on word lengths, and increases the grid size as needed
    until all words fit or a maximum size limit is reached.

    Usage:
        Initialize with a list of words.
        Call `generate()` to create a crossword puzzle instance containing all words,
        or None if generation fails within constraints.
    """
    placement_attempts_per_word = 3 # Is multiplied by the number of words to define iteration limit in attempt_grid_build
    max_attempts_per_size = 50 # Maximum number of grid build attempts allowed before increasing the grid size.
    max_grid_size = 80 # Maximum allowed size of the crossword grid before giving up.

    def __init__(self, words:list) -> None:
        self.words = sorted(words, key=lambda w: len(w), reverse=True)
        self.grid_size = self._initial_grid_size()

    def __str__(self):
        return f"crossword generator({self.grid_size}): {self.words}"
    
    def _initial_grid_size(self):
        """
        Calculate the initial size for the crossword grid.

        The size is based on:
        - The length of the longest word (the grid axis cannot be smaller than this).
        - The total length of all words, estimating an area with about 20% empty space.

        Returns:
            int: The initial grid size (number of rows and columns).
        """
        lengths = [len(s) for s in self.words]
        total = sum(lengths)
        lengths.sort()
        longest = lengths[-1] # axis cannot be smaller then the longest word
        area_axis = ceil(sqrt(total)*1.2) # expect at least 20% of the grid to be empty
        return max(longest, area_axis)

    def _get_valid_word_placements(self, word:str, grid:WordPlacementGrid):
        """
        Return all valid placements for a word in the current state of the grid.
        valid placement of word in grid.
        
        A valid placement is any position where the word can legally be inserted 
        (horizontally or vertically) according to crossword constraints.
        While overlapping with at least one other character.
        """
        valid_placements = []
        # iterate through each char in word to find matching chars in the grid
        for index, char in enumerate(word):
            matches = grid.find_char_positions(char)
            
            for match in matches:
                h_col = match[1] - index
                h_row = match[0] 
                h_can_place = grid.can_place_horizontal(word, h_row, h_col)
                if h_can_place:
                    valid_placements.append(((h_row, h_col), HORIZONTAL)) 
                
                v_col = match[1]
                v_row = match[0] - index
                v_can_place = grid.can_place_vertical(word, v_row, v_col)
                if v_can_place:
                    valid_placements.append(((v_row, v_col), VERTICAL))
        return valid_placements
    
    def _attempt_grid_build(self):
        """
        Attempt to build a crossword grid by placing words iteratively.

        Starts by placing the longest word at the center of the grid horizontally.
        Then attempts to place the remaining words in random order,
        selecting one of the valid placement found for each word.

        Returns:
            WordPlacementGrid: A grid instance with as many words placed as possible.
            Some words may be missing if no valid placement was found within the iteration limit.
        """
        # # create a blank grid
        grid = WordPlacementGrid(self.grid_size)
        words = self.words.copy()
        
        # place longest word first
        # words.sort(key= lambda x: len(x), reverse=True)
        first_word = words.pop(0)
        (row, col) = grid.get_center_placement(first_word, HORIZONTAL)
        grid.place_word(first_word, row, col, HORIZONTAL)
        
        # shuffle words to get random placement order
        shuffle(words)
        max_iterations = self.placement_attempts_per_word * len(words)
        iteration_count = 0
        
        while len(words) and iteration_count<max_iterations:
            word = words.pop(0)
            iteration_count += 1
            # get all valid placements for word in current grid
            valid_placements = self._get_valid_word_placements(word, grid)
            
            # shuffle to select placement at random
            shuffle(valid_placements)

            # if valid_placement:
            if len(valid_placements):
                valid_placement = valid_placements[0]
                ((row,col), direction) = valid_placement
                grid.place_word(word, row, col, direction)
            else:
                # add word to the end of queue
                words.append(word)
        # return grid (which might be incomplete)
        return grid

    def _retry_grid_builds(self):
        """
        Attempt to build a complete crossword grid by calling `attempt_grid_build` multiple times.

        Tries to place all words in a grid of the current size by retrying the build process 
        up to `self.max_attempts_per_size` times. Returns the first grid in which all words fit.
        
        Returns:
            WordPlacementGrid: A grid with all words placed, or None if unsuccessful.
        """

        # starting with grid-size
        # iteratively place words x timess

        grid = self._attempt_grid_build()
        iteration_counter = 0

        # stop when all words have been placed in grid or when iteration reaches max_count
        while len(self.words) != len(grid.get_words()) and iteration_counter < self.max_attempts_per_size:
            iteration_counter += 1
            grid = self._attempt_grid_build()
        
        print("iteration count", iteration_counter, self.grid_size)
        if len(self.words) != len(grid.get_words()):
            return None
        else:
            return grid

    def generate(self):
        """
        Generate a complete crossword by incrementally increasing the grid size.

        Repeatedly calls `retry_grid_builds` to try generating a grid that fits all words.
        If unsuccessful at the current grid size, the size is increased by 1 and the process repeats,
        up to `self.max_grid_size`.

        Returns:
            Crossword: A completed crossword puzzle with all words placed, or None if not possible within size limit.
        """
        while self.grid_size < self.max_grid_size:
            grid = self._retry_grid_builds()
            if grid:
                crossword = grid.export()
                return crossword
            else:
                self.grid_size += 1
        return None
