import math
import copy
from .constants import *
from .crossword import Crossword

class WordPlacementGrid:
    """
    Manages the placement of words on a square grid according to crossword-style constraints.
    
    This class is responsible for enforcing rules such as non-overlapping placements,
    valid intersections, boundary padding, and fitting within the grid dimensions.
    It maintains an internal representation of the grid and tracks all placed words
    along with their positions and orientations.

    Attributes:
        words (dict): A mapping from word (str) to a tuple:
           - position (tuple[int, int]): starting (row, col)
           - direction (str): either HORIZONTAL or VERTICAL
        grid (list): A 2D list representing the current state of the grid
    """

    def __init__(self, initial_size:int):
        """
        Initialize an empty square crossword grid.

        Args:
            initial_size (int): The initial number of rows and columns. 
            Creates a grid of size initial_size x initial_size.

        Attributes:
            words (dict[str, tuple[tuple[int, int], str]]): 
                Stores placed words with their starting positions and directions, initialized empty.
            grid (list[list[str]]): 
                2D list representing the crossword grid, initialized with EMPTY cells.
        """
        self.words = {}
        self.grid = [[EMPTY for _ in range(initial_size)] for _ in range(initial_size)]
        self.char_positions = {}

    def place_word(self, word:str, row:int, col:int, direction:str):
        """
        Place a word in the grid and update internal state.

        Add the word and its position to self.words.
        Update the grid to include the word at the specified position and direction,
        adding filler characters around intersections as needed.

        Note: This method does not validate whether the placement is allowed.
        """
        self.words[word] = ((row,col), direction)
        self._place_chars(word, row, col, direction)
        self._pad_word(word, row, col, direction)
        intersections = self._intersections(word, row, col, direction)
        for (row,col) in intersections:
            self._pad_intersection(row, col)
   
    def can_place_vertical(self, word:str, row:int, col:int):
        """
        Check if a word can be placed vertically starting at (row, col).

        Returns True if all the following constraints are satisfied:
        1. The word fits within the grid boundaries.
        2. The cell before the first letter and after the last letter is either empty or at the grid edge.
        3. The word does not overwrite any existing characters that differ from its own.
        
        Args:
            word: the word to place
            row: row index for the first character
            col: column index for the first character
        
        Returns:
            bool: True if placement is valid, False otherwise.
        """
        if not self._fits_in_grid(word, row, col, VERTICAL):
            return False
        
        # the square before the start of word and after the end of word should be empty
        prev_empty_or_edge = row == 0 or self.grid[row-1][col] in [EMPTY, FILLER]
        next_empty_or_edge = row + len(word) == len(self.grid) or self.grid[row + len(word)][col] in [EMPTY, FILLER]
        if not (prev_empty_or_edge and next_empty_or_edge):
            return False
        
        # there are no conflicting characters on the cells word will occupy
        for i, letter in enumerate(word):     
            if self.grid[row + i][col] not in [EMPTY, letter]:
                return False

        return True
    
    def can_place_horizontal(self, word:str, row:int, col:int):
        """
        Check if a word can be placed horizontally starting at (row, col).

        Returns True if all the following constraints are satisfied:
        1. The word fits within the grid boundaries.
        2. The cell before the first letter and after the last letter is either empty or at the grid edge.
        3. The word does not overwrite any existing characters that differ from its own.
        Args:
            word: the word to place
            row: row index for the first character
            col: column index for the first character

        Returns:
            bool: True if placement is valid, False otherwise.
        """
        if not self._fits_in_grid(word, row, col, HORIZONTAL):
            return False
        
        # the square before the start of word and after the end of word should be empty
        prev_empty_or_edge = col == 0 or self.grid[row][col-1] in [EMPTY, FILLER]
        next_empty_or_edge = col + len(word) == len(self.grid) or self.grid[row][col + len(word)] in [EMPTY, FILLER]
        if not (prev_empty_or_edge and next_empty_or_edge):
            return False
        
        # there are no conflicting characters on the cells word will occupy
        for i, letter in enumerate(word):
            if self.grid[row][col + i] not in [None, letter]:
                return False
        return True
    
    def copy(self):
        initial_size = len(self.grid)
        new_grid = WordPlacementGrid(initial_size)
        new_grid.grid = copy.deepcopy(self.grid)
        new_grid.char_positions = copy.deepcopy(self.char_positions)
        new_grid.words = self.words.copy()
        return new_grid
    
    def remove_word(self, word:str):
        (row, col), direction = self.words[word]
        intersections = self._intersections(word, row, col, direction)

        for index, char in enumerate(word):
            if direction == VERTICAL:
                r, c = row + index, col
            else:
                r, c = row, col + index

            if (r, c) not in intersections:
                # delete from grid
                self.grid[r][c] = EMPTY
                # delete from char_positions
                if (r,c) in self.char_positions[char]:
                    self.char_positions[char].remove((r, c))
                    if not self.char_positions[char]:
                        del self.char_positions[char]
                else:
                    print(f"CHAR NOT FOUND AT ")
            else:
                self._unpad_intersection(r,c)

        del self.words[word]

    def get_scored_valid_placements(self, word:str):
        """
        Return a list of valid placements (with non-zero score) for the given word
        in the current state of the grid.
        The score is based on how many intersections with already placed words this
        placement creates. 

        Returns:
            list[((row, col), direction, score)]
        """
        valid_placements = []
        # iterate through each char in word to find matching chars in the grid
        for index, char in enumerate(word):
            matches = self.find_char_positions(char)
            for match in matches:
                h_col = match[1] - index
                h_row = match[0] 
                h_score = self._placement_score(word, h_row, h_col, HORIZONTAL)
                if h_score > 0:
                    valid_placements.append(((h_row, h_col), HORIZONTAL, h_score)) 
                
                v_col = match[1]
                v_row = match[0] - index
                v_score = self._placement_score(word, v_row, v_col, VERTICAL)
                if v_score > 0:
                    valid_placements.append(((v_row, v_col), VERTICAL, v_score))
        return valid_placements

    def _placement_score(self, word:str, row:int, col:int, direction:str):
        # word must fit
        if not self._fits_in_grid(word, row, col, direction):
            return 0

        # the square before the start of word and after the end of word should be empty
        if direction == HORIZONTAL:
            prev_empty_or_edge = col == 0 or self.grid[row][col-1] in [EMPTY, FILLER]
            next_empty_or_edge = col + len(word) == len(self.grid) or self.grid[row][col + len(word)] in [EMPTY, FILLER]
        else: # vertical
            prev_empty_or_edge = row == 0 or self.grid[row-1][col] in [EMPTY, FILLER]
            next_empty_or_edge = row + len(word) == len(self.grid) or self.grid[row + len(word)][col] in [EMPTY, FILLER]
        if not (prev_empty_or_edge and next_empty_or_edge):
            return 0

        # calculate score based on overlaps
        score = 0
        for i, letter in enumerate(word):
            if direction == HORIZONTAL:
                cell = self.grid[row][col + i]
            else:
                cell = self.grid[row + i][col]
            if cell == letter:
                score += 1
            elif cell == EMPTY:
                continue
            else:
                return 0
            
        return score

    def get_center_placement(self, word:str, direction:str):
        """
        Return the (row, col) coordinates to place the first word centered on the grid.

        This method assumes the grid is empty and returns a placement such that
        the word appears as close as possible to the visual center, either horizontally
        or vertically depending on the specified direction.

        Args:
            word (str): The word to place.
            direction (str): Either HORIZONTAL or VERTICAL.

        Returns:
            tuple[int, int]: Starting (row, col) for placement.
        """
        if len(word) > len(self.grid):
            raise ValueError(f'word: "{word}" does not fit the grid')
        center_col = center_row = math.floor(len(self.grid)/2)
        if direction == HORIZONTAL:
            col_offset = math.floor(len(word)/2)
            return (center_row, center_col - col_offset)
        if direction == VERTICAL:
            row_offset = math.floor(len(word)/2)
            return (center_row-row_offset, center_col)
    
    def find_char_positions(self, char:str):
        """
        Return a list of all positions (row, col) where the specified character appears in the grid.

        Args:
            char (str): The character to search for.

        Returns:
            list[tuple[int, int]]: List of (row, col) tuples indicating occurrences of char.
        """
        positions = self.char_positions.get(char, set())
        return list(positions)

    def display(self):
        """
        Print a visualization of the grid to the terminal.
        Empty cells are shown as '-'.
        """
        for row in self.grid:
            [print(char or "-", end=" ") for char in row]
            print()
        print()
    
    def get_grid(self):
        """
        returns grid matrix
        """
        return self.grid
    
    def get_words(self):
        """
        returns a list of words
        """
        return self.words.keys()
    
    def _place_chars(self, word:str, row:int, col:int, direction:str):
        """
        Place the characters of the word onto the grid at the specified row and column,
        in the given direction (HORIZONTAL or VERTICAL). Modifies the grid in-place.
        Adds placed char to char_positions map.
        """
        if not self._fits_in_grid(word, row, col, direction):
            raise ValueError(f'word {word} does not fit in grid')
        
        for i, letter in enumerate(word):
            if direction == VERTICAL:
                char_row = row + i
                char_col = col
            if direction == HORIZONTAL:
                char_row = row
                char_col = col + i

            self.grid[char_row][char_col] = letter
            
            # add letter to char_positions map
            if letter not in self.char_positions:
                self.char_positions[letter] = set()
            self.char_positions[letter].add((char_row, char_col)) 

    def _pad_word(self, word:str, row:int, col:int, direction:str):
        """
        Add FILLER character immediately before and after the word on the grid to separate
        it from adjacent words. Does nothing if the padding cell is out of grid bounds.
        Modifies the grid in-place.
        """
        if direction == HORIZONTAL:
            if col > 0:
                self.grid[row][col-1] = FILLER
            if col + len(word) < len(self.grid):
                self.grid[row][col + len(word)] = FILLER

        elif direction == VERTICAL:
            if row > 0:
                self.grid[row-1][col] = FILLER
            if row + len(word) < len(self.grid):
                self.grid[row + len(word)][col] = FILLER
    
    def _unpad_intersection(self, row:int, col:int):
        # up-left
        if row > 0 and col > 0 and self.grid[row-1][col-1] == FILLER:
            self.grid[row-1][col-1] = EMPTY
        #up-right
        if row > 0 and col < len(self.grid)-1 and self.grid[row-1][col+1] == FILLER:
            self.grid[row-1][col+1] = EMPTY
        #down-left
        if row < len(self.grid)-1 and col > 0 and self.grid[row+1][col-1] == FILLER:
            self.grid[row+1][col-1] = EMPTY
        #down-right
        if row < len(self.grid)-1 and col < len(self.grid)-1 and self.grid[row+1][col+1] == FILLER:
            self.grid[row+1][col+1] = EMPTY

    def _pad_intersection(self, row:int, col:int):
        """
        Add FILLER characters diagonally adjacent to the cell at (row, col) if those cells are EMPTY,
        to prevent unintended word connections around intersections. Modifies the grid in-place.
        """
        # up-left
        if row > 0 and col > 0 and self.grid[row-1][col-1] == EMPTY:
            self.grid[row-1][col-1] = FILLER
        #up-right
        if row > 0 and col < len(self.grid)-1 and self.grid[row-1][col+1] == EMPTY:
            self.grid[row-1][col+1] = FILLER
        #down-left
        if row < len(self.grid)-1 and col > 0 and self.grid[row+1][col-1] == EMPTY:
            self.grid[row+1][col-1] = FILLER
        #down-right
        if row < len(self.grid)-1 and col < len(self.grid)-1 and self.grid[row+1][col+1] == EMPTY:
            self.grid[row+1][col+1] = FILLER 
    
    def _fits_in_grid(self, word:str, row:int, col:int, direction:str):
        """
        Check if word fits in grid starting at (row,col) in the specified direction (HORIZONTAL, or VERTICAL)
        
        Returns:
            bool: True if word fits, False otherwise.
        """
        if row < 0 or col < 0:
            return False
        
        if direction == VERTICAL:
            if row + len(word) > len(self.grid):
                return False
            
        if direction == HORIZONTAL:
            if col + len(word) > len(self.grid[0]):
                return False
        return True
    
    def _intersections(self, word:str, row:int, col:int, direction:str):
        """
        Return a list of tuples (row, col) where word intersects with other words
        placed in the opposing direction on the grid.
        """
        def word_range(word,row,col,direction):
            """
            Return a list of tuples representing each cell occupied by word
            """
            if direction == VERTICAL:
                return [(row + i, col) for i in range(len(word))]
            if direction == HORIZONTAL:
                return [(row, col + i) for i in range(len(word))]
          
        word1_range = word_range(word, row, col, direction)

        if direction == VERTICAL:
            perpendicular = [w for w in self.words if self.words[w][1] == HORIZONTAL]
        else:
            perpendicular = [w for w in self.words if self.words[w][1] == VERTICAL]

        intersections = []

        for word_2 in perpendicular:
            word2_row, word2_col = self.words[word_2][0]
            word2_direction = self.words[word_2][1]
            
            word2_range = word_range(word_2,word2_row, word2_col, word2_direction)
            for position in word1_range:
                if position in word2_range:
                    intersections.append(position)
        return intersections

    def export(self):
        """
        Create and return a Crossword instance representing the current grid state.

        Returns:
            Crossword: A Crossword object initialized with the current grid and word placements.
        """
        return Crossword(self.grid, self.words)