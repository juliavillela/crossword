import math
from .constants import *
from .helpers import trim, clean

class CrosswordGrid:
    """
    Represents a squre crosswordGrid that can place words according to constraints.

    Words is a dict containing all the words that have been placed in the grid
    and their respective position: a tuple of ints (row, col) for the first char in word, 
    and direction: VERTICAL or HORIZONTAL
 
    Grid is a two-dimentional list of rows and columns where each item represents a cell in the puzzle.
    """
    def __init__(self, initial:int):
        """
        Initializes an empty crossword with max width and length equal to initial.
        """
        self.words = {}
        self.grid = [[EMPTY for _ in range(initial)] for _ in range(initial)]

    def place_word(self, word:str, row:int, col:int, direction:str):
        """
        Adds word and position to self.words.
        updates grid to contain word at placement
        as well as necessary padding

        This method does not check if placement is allowed before altering the grid.
        """
        self.words[word] = ((row,col), direction)
        self._place_chars(word, row, col, direction)
        self._pad_word(word, row, col, direction)
        intersections = self._intersections(word, row, col, direction)
        for (row,col) in intersections:
            self._pad_intersection(row, col)
   
    def can_place_vertical(self, word:str, row:int, col:int):
        """
        Return True if word can be placed at position (row,col) vertically, else False.
        The constraints for placement are:
        1. word must fit the grid
        2. word must be preceded and followed by an empty square
        3. word cannot change any of the characters that have already been placed
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
        Return True if word can be placed at position (row,col) horizontally, else False.
        The constraints for placement are:
        1. word must fit the grid
        2. word must be preceded and followed by an empty square
        3. word cannot change any of the characters that have already been placed
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
        Return a tuple (row, col) for word placement that results in 
        word being placed as close to the center of the grid as possible.
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
        Return a list of tuples (row,col) with each occurence of char in grid
        """
        positions = []
        for row_i, row in enumerate(self.grid):
            for col_i, cell in enumerate(row):
                if char == cell:
                    positions.append((row_i, col_i))
        return positions
       
    def display(self):
        """
        Prints visualization of grid to terminal
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
        Updates grid to contain word characters at placement.
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
        Adds FILLER char to start and end of word
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
        Adds FILLER char around intersections
        """
        # up-left
        if row > 0 and col > 0 and self.grid[row-1][col-1] == EMPTY:
            self.grid[row-1][col-1] = FILLER
        #up-rigth
        if row > 0 and col < len(self.grid)-1 and self.grid[row-1][col+1] == EMPTY:
            self.grid[row-1][col+1] = FILLER
        #down-left
        if row < len(self.grid)-1 and col > 0 and self.grid[row+1][col-1] == EMPTY:
            self.grid[row+1][col-1] = FILLER
        #down-rigth
        if row < len(self.grid)-1 and col < len(self.grid)-1 and self.grid[row+1][col+1] == EMPTY:
            self.grid[row+1][col+1] = FILLER 
    
    def _fits_in_grid(self, word:str, row:int, col:int, direction:str):
        """
        Returns True if word fits in grid starting at row column,
        in direction = direction, else False.
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
        Returns a list of tupples (row,col) - each tuple represents a cell
        where word intersects with another word in the oposing direction.
        """
        def word_range(word,row,col,direction):
            """
            Returns a list of tuples for each cell occupied by word
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
        Returns an instance of Crossword from current grid
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
        cell_size = 50
        cell_border = 2
        interior_size = cell_size - 2 * cell_border

        img = Image.new(
            "RGBA",
            ( self.width() * cell_size,
            self.height() * cell_size),
            "white"
        )

        font = ImageFont.load_default(40)
        draw = ImageDraw.Draw(img)

        for row in range(self.height()):
            for col in range(self.width()):
                # Calculate coordinates for the cell
                x0 = col * cell_size
                y0 = row * cell_size
                x1 = (col + 1) * cell_size
                y1 = (row + 1) * cell_size


                # Get the character in the cell
                char = self.key[row][col]

                # Ignore EMPTY and WORD_BOUNDRY
                if char is not EMPTY:

                    # Draw cell border
                    draw.rectangle([x0, y0, x1, y1], fill="white", outline="black")
                    # Calculate text size and position
                    # text_size = draw.textsize(char, font=font)
                    text_x = x0 + (interior_size - 25) / 2
                    text_y = y0 + (interior_size - 45) / 2

                    # Draw the character in the cell
                    draw.text((text_x, text_y), char, fill="black", font=font)

        img.save(filename)

    def save_blank_img(self, filename):

        cell_size = 50
        cell_border = 2
        interior_size = cell_size - 2 * cell_border

        img = Image.new(
            "RGBA",
            ( self.width() * cell_size,
            self.height() * cell_size),
            "white"
        )

        font = ImageFont.load_default(20)
        draw = ImageDraw.Draw(img)

        for row in range(self.height()):
            for col in range(self.width()):
                # Calculate coordinates for the cell
                x0 = col * cell_size
                y0 = row * cell_size
                x1 = (col + 1) * cell_size
                y1 = (row + 1) * cell_size


                # Get the character in the cell
                char = self.blank[row][col]

                # Ignore EMPTY and WORD_BOUNDRY
                if char is not EMPTY:

                    # Draw cell border
                    draw.rectangle([x0, y0, x1, y1], fill="white", outline="black")
                    # Calculate text size and position
                    # text_size = draw.textsize(char, font=font)
                    text_x = x0 + (interior_size - 25) / 2
                    text_y = y0 + (interior_size - 45) / 2

                    # Draw the character in the cell
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