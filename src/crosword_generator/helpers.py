from .constants import *

def clean(grid:list[list]):
    """
    Returns a copy of the given grid where all occurrences of FILLER are replaced with EMPTY.

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
    Returns a copy of the grid with all-empty rows and columns removed.

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