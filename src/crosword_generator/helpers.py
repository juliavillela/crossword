from src.crosword_generator.constants import *

def clean(grid:list[list]):
    """
    Returns a copy of grid matrix where FILLER is replaced with None
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
    Returns a copy of grid matrix where empty columns and empty rows have been removed 
    An empty line is a line where all values == EMPTY

    If called on an empty grid: returns empty grid unchanged.
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