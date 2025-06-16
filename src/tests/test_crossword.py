import pytest
from crosword_generator.constants import *
from crosword_generator.crossword import clean, trim, Crossword

def test_clean_replaces_filler():
    grid = [["A", FILLER], [FILLER, "B"]]
    cleaned = clean(grid)
    assert cleaned == [["A", EMPTY], [EMPTY, "B"]]

def test_trim_removes_empty_edges():
    grid = [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, "A", EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]
    trimmed = trim(grid)
    assert trimmed == [["A"]]
    
def test_trim_keeps_full_grid_with_content():
    grid = [["A", "B"], ["C", EMPTY]]
    assert trim(grid) == grid

# test different aspects of class initialization.
@pytest.fixture
def crossword_setup():
    words = {
        'CATS': ((1, 1), HORIZONTAL), 
        'MAT': ((0, 2), VERTICAL), 
        'SPA': ((1, 4), VERTICAL)
        }
    
    grid = [
        [EMPTY, FILLER, 'M', FILLER, FILLER],
        [FILLER, 'C', 'A', 'T', 'S'], 
        [EMPTY, FILLER, 'T', FILLER, 'P'], 
        [EMPTY, EMPTY, FILLER, EMPTY, 'A'], 
        [EMPTY, EMPTY, EMPTY, EMPTY, FILLER]
        ]
    
    crossword = Crossword(grid, words)
    return crossword

def test_cleaned_grid(crossword_setup):
    crossword = crossword_setup
    expected_cleaned_grid = [
        [EMPTY, EMPTY, 'M', EMPTY, EMPTY],
        [EMPTY, 'C', 'A', 'T', 'S'], 
        [EMPTY, EMPTY, 'T', EMPTY, 'P'], 
        [EMPTY, EMPTY, EMPTY, EMPTY, 'A'], 
        [EMPTY, EMPTY, EMPTY, EMPTY, EMPTY]
        ]
    
    assert crossword.grid == expected_cleaned_grid

def test_position_number_map(crossword_setup):
    crossword = crossword_setup
    expected_position_number_map = {
        (1,1): '1',
        (0,2): '2',
        (1,4): '3'
    }

    assert crossword.positon_number_map == expected_position_number_map

def test_key_grid(crossword_setup):
    crossword = crossword_setup
    expected_key_grid = [
        [EMPTY, 'M', EMPTY, EMPTY],
        ['C', 'A', 'T', 'S'], 
        [EMPTY, 'T', EMPTY, 'P'], 
        [EMPTY, EMPTY, EMPTY, 'A'], 
        ]
    
    assert crossword.key == expected_key_grid

def test_blank_grid(crossword_setup):
    crossword = crossword_setup
    expected_blank_grid = [
        [EMPTY, '2', EMPTY, EMPTY],
        ['1', BLANK, BLANK, '3'], 
        [EMPTY, BLANK, EMPTY, BLANK], 
        [EMPTY, EMPTY, EMPTY, BLANK], 
        ]

    assert crossword.blank == expected_blank_grid

def test_width_and_height(crossword_setup):
    crossword = crossword_setup
    assert crossword.width() == 4
    assert crossword.height() == 4