from crosword_generator.constants import *
from crosword_generator.word_placement_grid import WordPlacementGrid

def test_initialization():
    grid = WordPlacementGrid(5)
    assert len(grid.grid) == 5
    assert all(len(row) == 5 for row in grid.grid)
    assert all(cell == EMPTY for row in grid.grid for cell in row)
    assert grid.words == {}

def test_place_word_horizontal():
    grid = WordPlacementGrid(5)
    word = "CAT"
    row, col = 1, 1
    grid.place_word(word, row, col, HORIZONTAL)
    # check letters placed
    for i, letter in enumerate(word):
        assert grid.grid[row][col + i] == letter
    # check padding before and after
    assert grid.grid[row][col - 1] == FILLER
    assert grid.grid[row][col + len(word)] == FILLER
    # check words dict
    assert grid.words[word] == ((row, col), HORIZONTAL)

def test_place_word_vertical():
    grid = WordPlacementGrid(5)
    word = "CAT"
    row, col = 1, 1
    grid.place_word(word, row, col, VERTICAL)
    # check letters placed
    for i, letter in enumerate(word):
        assert grid.grid[row + i][col] == letter
    # check padding before and after
    assert grid.grid[row - 1][col] == FILLER
    assert grid.grid[row + len(word)][col] == FILLER
    # check words dict
    assert grid.words[word] == ((row, col), VERTICAL)

def test_can_place_vertical_boundaries():
    grid = WordPlacementGrid(4)
    word = "WORD"
    # should fit exactly vertically at 0,0
    assert grid.can_place_vertical(word, 0, 0) is True
    # one beyond bottom edge
    assert grid.can_place_vertical(word, 1, 0) is False

def test_can_place_horizontal_boundaries():
    grid = WordPlacementGrid(4)
    word = "WORD"
    # should fit exactly horizontally at 0,0
    assert grid.can_place_horizontal(word, 0, 0) is True
    # one beyond bottom edge
    assert grid.can_place_horizontal(word, 0, 1) is False

def test_can_place_vertical_overlap():
    grid = WordPlacementGrid(5)
    grid.place_word("CAT", 1, 1, HORIZONTAL)
    # Conflict with different letter
    assert grid.can_place_vertical("MOP", 0, 2) is False
    # try to place overlapping word with matching letter
    assert grid.can_place_vertical("MAT", 0, 2) is True
    grid.place_word("MAT", 0, 2, VERTICAL)
    # check padded intersections
    assert grid.grid[0][1] == grid.grid[0][3] == grid.grid[2][1] == grid.grid[2][3] == FILLER

def test_can_place_horizontal_overlap():
    grid = WordPlacementGrid(5)
    grid.place_word("CAT", 0, 2, VERTICAL)
    # Conflict with different letter
    assert grid.can_place_horizontal("MOP", 1, 1) is False
    # try to place overlapping word with matching letter
    assert grid.can_place_horizontal("MAT", 1, 1) is True
    grid.place_word("MAT", 1, 1, HORIZONTAL)
    # check padded intersections
    assert grid.grid[0][1] == grid.grid[0][3] == grid.grid[2][1] == grid.grid[2][3] == FILLER

def test_find_char_positions():
    grid = WordPlacementGrid(5)
    grid.grid[2][2] = "X"
    grid.grid[4][0] = "X"
    positions = grid.find_char_positions("X")
    assert (2, 2) in positions
    assert (4, 0) in positions
    assert len(positions) == 2
