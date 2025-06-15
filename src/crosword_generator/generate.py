from random import shuffle

from .constants import *
from .crossword import WordPlacementGrid

class CrosswordBuilder:
    def __init__(self, words:list, grid_size, max_iteration_count=50) -> None:
        self.words = sorted(words, key=lambda w: len(w), reverse=True)
        self.grid_size = grid_size
        self.max_iteration_count = max_iteration_count

    def __str__(self):
        return f"crossword generator({self.grid_size}): {self.words}"
    
    def get_many_valid_word_placements(self, word, grid):
        """
        Returns a list of tuples ((row,col), direction) for each 
        valid placement of word in grid
        """
        valid_placements = []
        # iterate through each char in word to find matching chars in the grid
        for index, char in enumerate(word):
            matches = grid.match_many_char(char)
            
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
    
    def iterative_placement(self):
        # create a blank grid
        grid = WordPlacementGrid(self.grid_size)
        words = self.words.copy()
        
        # place first word
        words.sort(key= lambda x: len(x), reverse=True)
        first_word = words.pop(0)
        (row, col) = grid.get_center_placement(first_word, HORIZONTAL)
        grid.place_word(first_word, row, col, HORIZONTAL)
        
        # shuffle words to get random placement order
        shuffle(words)
        max_iterations = 2 * len(words)
        iteration_count = 0
        
        while len(words) and iteration_count<max_iterations:
            word = words.pop(0)
            iteration_count += 1
            # valid_placement = self.get_valid_word_placement(word, grid)

            # get all valid placements for word in current grid
            valid_placements = self.get_many_valid_word_placements(word, grid)
            
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

    def generate(self):
        """
        Return grid with self.words calling iterative_placement multiple times
        untill all words have been placed in the grid or until self.max_iteration_count
        
        If could not place all words in grid, returns None
        """
        # starting with grid-size
        # iteratively place words x timess
        grid = self.iterative_placement()
        iteration_counter = 0
        # stop when all words have been placed in grid or when iteration reaches max_count
        while len(self.words) != len(grid.get_words()) and iteration_counter < self.max_iteration_count:
            iteration_counter += 1
            grid = self.iterative_placement()
        
        print("iteration count", iteration_counter)
        if len(self.words) != len(grid.get_words()):
            return None
        else:
            return grid

class CrosswordGenerator:
    """
    Use CrosswordBuilder and internal settings to generate valid crossword.
    """
    def __init__(self, word_list, attempts=None, max_grid_size=None) -> None:
        """
        - word_list: a validated list of words to use in puzzle
        - attempts: how many times builder will try to place words on the grid before returning None(defaults to 50)
        - max_grid_size: how large a grid can get before generation fails (defaults to MAX_WORD_LEN + 20)
        """
        self.words = word_list
        self.grid_size = self._get_min_grid_size()
        self.max_grid_size = max_grid_size or MAX_WORD_LEN + 20 # will stop trying and return impossible
        if self.grid_size > self.max_grid_size:
            raise ValueError("WORD LIST IS TOO LARGE TO GENERATE")
        self.attempts = attempts or 50

    def _get_min_grid_size(self):
        """
        Returns an integer to be used as starting grid_size for generator
        based on wordlist.
        """
        from math import sqrt, ceil
        lengths = [len(s) for s in self.words]
        total = sum(lengths)
        lengths.sort()
        longest = lengths[-1] # axis cannot be smaller then the longest word
        area_axis = ceil(sqrt(total)*1.2) # expect at least 20% of the grid to be empty
        return max(longest, area_axis)

    def generate(self):
        """
        Generate at least min_options of valid puzzles (a valid puzzle is one that contains all words in word-list)
        and store them in self.grids.

        Tries to generate a valid puzzle self.attempt times 
        starting from the smallest grid-size(as defined in the init method)
        if not enough valid puzzles were generated, grid_size is incremented untill max_grid_size

        #TBD : In many scenarios(eg: max_grid_size is close to largest word length) it is possible that no valid grid can be generated 
        and there is no error catch implemented to handle this.
        
        """
        while self.grid_size < self.max_grid_size:
            builder = CrosswordBuilder(self.words, self.grid_size, self.attempts)
            grid = builder.generate()
            if grid:
                crossword = grid.export()
                return crossword
            else:
                self.grid_size += 1
        return None
