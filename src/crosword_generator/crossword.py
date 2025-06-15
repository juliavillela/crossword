from .constants import *
from .helpers import trim, clean
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