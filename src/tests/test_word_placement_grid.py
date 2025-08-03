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
    # check char position dict
    assert grid.char_positions["C"] == {(1,1)}
    assert grid.char_positions["A"] == {(1,2)}
    assert grid.char_positions["T"] == {(1,3)}


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
    # check char position dict
    assert grid.char_positions["C"] == {(1,1)}
    assert grid.char_positions["A"] == {(2,1)}
    assert grid.char_positions["T"] == {(3,1)}


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
    grid.place_word("X", 2, 2, HORIZONTAL)
    grid.place_word("X", 4, 0, HORIZONTAL)
    positions = grid.find_char_positions("X")
    assert (2, 2) in positions
    assert (4, 0) in positions
    assert len(positions) == 2

def test_fits_in_grid():
    grid = WordPlacementGrid(4)
    assert grid._fits_in_grid("WORD", 0, 0, HORIZONTAL) == True
    assert grid._fits_in_grid("WORD", 0, 0, VERTICAL) == True
    assert grid._fits_in_grid("WORD", 0, 1, HORIZONTAL) == False
    assert grid._fits_in_grid("WORD", 1, 0, VERTICAL) == False

def test_intersections():
    grid = WordPlacementGrid(5)
    grid.place_word("CATS", 1, 1, HORIZONTAL)
    grid.place_word("MAT", 0, 2, VERTICAL) # will intersect at (1,2)
    grid.place_word("SPA", 1, 4, VERTICAL) # will intersect at (1, 4)

    intersections = grid._intersections("CATS", 1,1, HORIZONTAL)
    
    assert (1,2) in intersections
    assert (1,4) in intersections
    assert len(intersections) == 2

def test_placement_score():
    grid = WordPlacementGrid(6)
    # doesn't fit
    assert grid._placement_score("LONGWORD", 0, 0, HORIZONTAL) == 0
    # valid, but no overlap
    assert grid._placement_score("CATS", 0, 0, HORIZONTAL) == 0

    # vertical overlap on "A"
    grid.place_word("CATS", 1, 1, HORIZONTAL)
    assert grid._placement_score("MATTE", 0, 2, VERTICAL) == 1
    
    grid.place_word("MATTE", 0, 2, VERTICAL)
    # horizontal overlap on "E"
    assert grid._placement_score("DREAM", 4, 0, HORIZONTAL) == 1
    grid.place_word("DREAM", 4, 0, HORIZONTAL)
    # double overlap on "S" and "M"
    assert grid._placement_score("STEM", 1, 4, VERTICAL) == 2
    
def test_get_scored_valid_placements():
    grid = WordPlacementGrid(6)

    # empty grid has no valid placements
    assert grid.get_scored_valid_placements("CATS") == []

    grid.place_word("CATS", 1, 1, HORIZONTAL)

    # word "MAT" can only be placed at "A" intersection
    assert grid.get_scored_valid_placements("MAT") == [((0,2), VERTICAL, 1)]

    # Word "AT" can be placed intersecting "A" or "T"
    valid = grid.get_scored_valid_placements("AT")
    assert len(valid) == 2
    # intersecting "A"
    scored_position_1 = ((1, 2), VERTICAL, 1)
    # intersecting "T"
    scored_position_2 = ((0,3), VERTICAL, 1)
    assert scored_position_1 in valid
    assert scored_position_2 in valid
