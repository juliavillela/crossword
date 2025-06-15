import math
from .constants import *
from .helpers import trim, clean

class CrosswordGrid:
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

    def place_word(self, word:str, row:int, col:int, direction:str):
        """
        Place a word in the grid and update internal state.

        Add the word and its position to self.words.
        Update the grid to include the word at the specified position and direction,
        adding filler characters before, after, and around intersections as needed.

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
    
    def match_many_char(self, char:str):
        """
        Return a list of all positions (row, col) where the specified character appears in the grid.

        Args:
            char (str): The character to search for.

        Returns:
            list[tuple[int, int]]: List of (row, col) tuples indicating occurrences of char.
        """
        positions = []
        for row_i, row in enumerate(self.grid):
            for col_i, cell in enumerate(row):
                if char == cell:
                    positions.append((row_i, col_i))
        return positions
       
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
        """
        if not self._fits_in_grid(word, row, col, direction):
            raise ValueError(f'word {word} does not fit in grid')
        
        if direction == HORIZONTAL:
            for i, letter in enumerate(word):
                self.grid[row][col + i] = letter

        elif direction == VERTICAL:
            for i, letter in enumerate(word):
                self.grid[row + i][col] = letter

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
    
from PIL import Image, ImageDraw, ImageFont #used in Crossword.save_blank_img and .save_key_img

class Crossword:
    """
    Represents a finalized Crossword puzzle
    """
    def __init__(self, grid:list[list], words:dict) -> None:
        self.grid = clean(grid)

        # Assign a number to each word according to theirs starting row or columns
        # and map cell position to number
        self.positon_number_map = {}

        horizontal_words = list(filter(lambda w: words[w][1]==HORIZONTAL, words))
        # sort horizontal words by row index
        horizontal_words.sort(key= lambda w: words[w][0][0])
        vertical_words = list(filter(lambda w: words[w][1]==VERTICAL, words))
        # sort vertical words by col index
        vertical_words.sort(key= lambda w: words[w][0][1])
        
        for index, word in enumerate(horizontal_words):
            position = words[word][0]
            number = index + 1
            self.positon_number_map[position] = str(number)

        for index, word in enumerate(vertical_words):
            position = words[word][0]
            number = len(horizontal_words) + index + 1
            # account for possibility that 2 words start at the same square
            if self.positon_number_map.get(position):
                self.positon_number_map[position] += f"/{number}"
            else:
                self.positon_number_map[position] = str(number)

        self.blank = self._get_blank_grid()
        self.key = self._get_key_grid()
    
    def _get_blank_grid(self):
        """
        Returns a trimmed blank version of grid where EMPTY cells remain EMPTY,
        letters are replaced with BLANK and the starting position for 
        each word is replaced with the corresponding number.
        """
        blank = []
        for row_i, row in enumerate(self.grid):
            blank_row = []
            for col_i, cell in enumerate(row):
                if (row_i, col_i) in self.positon_number_map:
                    blank_row.append(self.positon_number_map[(row_i, col_i)])
                elif cell is not EMPTY:
                    blank_row.append(BLANK)
                else:
                    blank_row.append(EMPTY)
            blank.append(blank_row)
        return trim(blank)
    
    def _get_key_grid(self):
        """
        Returns a trimmed version of the key grid containing words and EMPTY
        """
        return trim(self.grid)

    def display_key_grid(self):
        """
        Prints visualization of grid to terminal
        """
        for row in self.key:
            [print(char or "-", end=" ") for char in row]
            print()
        print()
    
    def display_blank_grid(self):
        """
        Prints visualization of grid to terminal
        """
        for row in self.blank:
            [print(char or "-", end=" ") for char in row]
            print()
        print()
    
    def save_key_img(self, filename):
        self._save_image(self.key, 40, filename)

    def save_blank_img(self, filename):
        self._save_image(self.blank, 20, filename )

    def _save_image(self, grid, font_size, filename):
        cell_size = 50
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        
        #create image dimentions
        img = Image.new(
            "RGBA",
            ( (self.width() * cell_size) + cell_border,
            (self.height() * cell_size) + cell_border),
            "white"
        )

        font = ImageFont.load_default(font_size)
        draw = ImageDraw.Draw(img)

        for row in range(self.height()):
            for col in range(self.width()):
                # Calculate coordinates for the cell
                x0 = col * cell_size
                y0 = row * cell_size
                x1 = (col + 1) * cell_size
                y1 = (row + 1) * cell_size

                # Get the character in the cell
                char = grid[row][col]
                
                # Ignore EMPTY
                if char is not EMPTY:
                    # draw rectangle
                    coordinates = [x0, y0, x1, y1]
                    draw.rectangle(coordinates, fill="white", outline="black")

                    #draw characters
                    text_x = x0 + (interior_size - 25) / 2
                    text_y = y0 + (interior_size - 45) / 2
                    draw.text((text_x, text_y), char, fill="black", font=font)
            
            img.save(filename)

    def height(self):
        """
        Returns int number of rows in grid
        """
        return len(self.key)

    def width(self):
        """
        Returns int number of columns in grid
        """
        return len(self.key[0])