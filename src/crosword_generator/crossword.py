from .constants import *
from PIL import Image, ImageDraw, ImageFont #used in Crossword.save_blank_img and .save_key_img

def clean(grid:list[list]):
    """
    Return a copy of the given grid where all occurrences of FILLER are replaced with EMPTY.

    Args:
        grid (list[list]): A 2D list representing the crossword grid.

    Returns:
        list[list]: A new grid with FILLER cells replaced by EMPTY.
    """
    clean_grid = []
    for row in grid:
        clean_row = []
        for cell in row:
            if cell == FILLER:
                clean_row.append(EMPTY)
            else:
                clean_row.append(cell)
        clean_grid.append(clean_row)
    return clean_grid

def trim(grid:list[list]):
    """
    Return a copy of the grid with all-empty rows and columns removed.

    An empty row or column is one where all cells are equal to EMPTY.

    Args:
        grid (list[list]): A 2D list representing the crossword grid.

    Returns:
        list[list]: A trimmed grid with no empty rows or columns around the edges.
    """
    # Find the range of rows and columns with non-empty cells
    # grids are assumed to be square
    min_row = min_col = len(grid)
    max_row = max_col = 0
    for row_i, row in enumerate(grid):
        for col_i, cell in enumerate(row):
            if cell is not EMPTY:
                min_row = min(min_row, row_i)
                max_row = max(max_row, row_i)
                min_col = min(min_col, col_i)
                max_col = max(max_col, col_i)

    # Create a new trimmed grid
    trimmed_grid = []
    for row in grid[min_row:max_row + 1]:
        trimmed_grid.append(row[min_col:max_col + 1])

    return trimmed_grid

# This class is typically instantiated from a fully populated WordPlacementGrid

class Crossword:
    """
    Represents a finalized crossword puzzle built from a completed grid and
    a set of placed words.

    This class generates two versions of the puzzle:
    - A blank grid, with clue numbers and hidden letters, for players to solve.
    - A key grid, with all the correct letters filled in.

    It also provides functionality to visualize and save these grids.

    Attributes:
        grid (list[list[str]]): The original completed crossword grid containing letters and EMPTY cells.
        positon_number_map (dict): A mapping of word starting positions (row, col) to their assigned clue number(s).
                                   If two words start at the same cell (one horizontal and one vertical), the number
                                   is formatted as "X/Y".
        blank (list[list[str]]): A grid where letters are hidden (replaced with BLANK),
                                 and word starting positions are marked with their clue number.
        key (list[list[str]]): A solution grid showing all placed words, with no clue numbers.

    """
    def __init__(self, grid:list[list], words:dict) -> None:
        """
        Initializes a Crossword object from a finalized grid and a dictionary of words.

        This method cleans the given grid by replacing special filler characters with EMPTY,
        assigns sequential numbers to words based on their starting positions,
        distinguishing between horizontal and vertical words, and creates a mapping
        from cell positions to their corresponding clue numbers for display purposes.

        It also generates trimmed versions of the grid: a "blank" version for the player
        to fill in, and a "key" version containing the complete answers.

        Args:
            grid (list[list]): 2D matrix representing the finalized crossword grid,
                containing letters and EMPTY/FILLER markers.
            words (dict): Dictionary where keys are words (strings) and values are tuples
                containing the starting position (row, column) and the direction
                (HORIZONTAL or VERTICAL).
        """
        self.grid = clean(grid)
        self.positon_number_map = self._assign_numbers(words)
        self.blank = self._get_blank_grid()
        self.key = self._get_key_grid()
    
    def _get_blank_grid(self):
        """
        Return a trimmed version of the grid for the puzzle to be solved.

        In this version:
        - EMPTY cells remain EMPTY
        - Letters are replaced with BLANK symbols
        - The starting position of each word is replaced with its assigned clue number
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
        Return a trimmed version of the solution grid.

        This grid contains the full words placed in the crossword,
        representing the completed puzzle (the answer key).
        """
        return trim(self.grid)

    def _assign_numbers(self, words:dict):
        """
        Assigns sequential clue numbers to word starting positions in the grid.

        Horizontal words are numbered first, top to bottom by row index.
        Vertical words are numbered next, left to right by column index.
        If a horizontal and vertical word share the same starting cell, both numbers are combined as a string (e.g., "3/10").

        Args:
            words (dict): A dictionary mapping each word to a tuple:
                (starting_position: tuple[int, int], direction: str)

        Returns:
            dict: A mapping of starting grid positions (row, col) to clue numbers as strings.
        """
        positon_number_map = {}
        horizontal_words = list(filter(lambda w: words[w][1]==HORIZONTAL, words))
        # sort horizontal words by row index
        horizontal_words.sort(key= lambda w: words[w][0][0])
        vertical_words = list(filter(lambda w: words[w][1]==VERTICAL, words))
        # sort vertical words by col index
        vertical_words.sort(key= lambda w: words[w][0][1])
        
        for index, word in enumerate(horizontal_words):
            position = words[word][0]
            number = index + 1
            positon_number_map[position] = str(number)

        for index, word in enumerate(vertical_words):
            position = words[word][0]
            number = len(horizontal_words) + index + 1
            # account for possibility that 2 words start at the same square
            if positon_number_map.get(position):
                positon_number_map[position] += f"/{number}"
            else:
                positon_number_map[position] = str(number)

        return positon_number_map

    def display_key_grid(self):
        """
        Print a visual representation of the solution (key) grid to the terminal.
        
        Each cell shows its character; EMPTY cells are displayed as '-'.
        """
        for row in self.key:
            [print(char or "-", end=" ") for char in row]
            print()
        print()
    
    def display_blank_grid(self):
        """
        Print a visual representation of the blank puzzle grid to the terminal.
        """
        for row in self.blank:
            [print(char or "-", end=" ") for char in row]
            print()
        print()
    
    def save_key_img(self, filename):
        """
        Save an image file representing the solution (key) grid of the crossword.

        Parameters:
            filename (str): The path to save the image file.
        """
        self._save_image(self.key, 40, filename)

    def save_blank_img(self, filename):
        """
        Save an image file representing the blank crossword grid (with numbered clues).

        Parameters:
            filename (str): The path to save the image file.
        """
        self._save_image(self.blank, 20, filename )

    def _save_image(self, grid, font_size, filename):
        """
        Save an image representation of the crossword grid to a file.

        Parameters:
            grid (list[list]): 2D list representing the crossword grid to render.
            font_size (int): Font size to use for rendering text in cells.
            filename (str): Path to the file where the image will be saved.

        The method draws each cell as a white rectangle with a black border,
        and renders the character inside the cell, skipping EMPTY cells.
        """
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
        Return int number of rows in grid
        """
        return len(self.key)

    def width(self):
        """
        Return int number of columns in grid
        """
        return len(self.key[0])