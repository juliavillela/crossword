import pytest
from crosword_generator.constants import *
from crosword_generator.generate import RecursiveCrosswordGenerator
from crosword_generator.crossword import Crossword
from crosword_generator.word_placement_grid import WordPlacementGrid

def test_initialization():
    generator = RecursiveCrosswordGenerator(["bat","cats"])

    # make sure words are sorted by descending length
    assert generator.words == ["cats", "bat"]

    # make sure grid size is larger than or equal to largest word
    assert generator.grid_size >= 4

# tests on easy word lists should return a sucessfull grid
def test_recursive_place_words_returns_WordPlacementGrid():
    wordlist = [
        "aaaaa", "aaaa", "aaa", 
    ] #sorted by length

    generator = RecursiveCrosswordGenerator(wordlist)
    
    # manually place the first word (to mimic build_grid logic)
    first_word = wordlist[0]
    grid = WordPlacementGrid(generator.grid_size)
    (row,col) = grid.get_center_placement(first_word, HORIZONTAL)
    grid.place_word(first_word, row, col, HORIZONTAL)
    
    # run recursive placement on remaining words
    result = generator.recursively_place_words(wordlist[1:], grid)
    
    # make sure analilitic data was collected
    assert generator.recursion_counter > 0
    assert generator.max_recursion_depth > 0

    # make sure result is an instance of WordPlacementGrid
    assert isinstance(result, WordPlacementGrid)
    
    # make sure all words have been placed
    placed_words = set(result.get_words())
    assert placed_words == set(wordlist)

def test_build_grid_returns_WordPlacementGrid():
    wordlist = [
        "aaa", "aaaa", "aaaaa"
    ]
    generator = RecursiveCrosswordGenerator(wordlist)
    result = generator.build_grid()

    # make sure result is an instance of WordPlacementGrid
    assert isinstance(result, WordPlacementGrid)
    
    # make sure all words have been placed
    placed_words = set(result.get_words())
    assert placed_words == set(wordlist)

def test_generate_returns_Crossword():
    wordlist = [
        "aaa", "aaaa", "aaaaa"
    ]
    generator = RecursiveCrosswordGenerator(wordlist)
    result = generator.generate()

    # make sure result is an instance of WordPlacementGrid
    assert isinstance(result, Crossword)

# tests on impossible word list should return none
def test_recursive_place_words_returns_false_for_impossible_word_list():
    wordlist = [
        "aaaa", "bbb", "ccc", 
    ] #sorted by length

    generator = RecursiveCrosswordGenerator(wordlist)
    
    # manually place the first word (to mimic build_grid logic)
    first_word = wordlist[0]
    grid = WordPlacementGrid(generator.grid_size)
    (row,col) = grid.get_center_placement(first_word, HORIZONTAL)
    grid.place_word(first_word, row, col, HORIZONTAL)
    
    # run recursive placement on remaining words
    result = generator.recursively_place_words(wordlist[1:], grid)
    
    # make sure analilitic data was collected
    assert generator.recursion_counter > 0 # the function was called at least once
    assert generator.max_recursion_depth == 0 # no valid placements, therefore no recursion depth

    # make sure result is false
    assert result == False

def test_build_grid_returns_false_for_impossible_word_list():
    wordlist = [
        "aaa", "bbb", "ccc"
    ]
    generator = RecursiveCrosswordGenerator(wordlist)
    result = generator.build_grid()
    
    # make sure result is false
    assert result == False

def test_generate_returns_None_for_impossible_word_list():
    wordlist = [
        "aaa", "bbb", "ccc"
    ]
    generator = RecursiveCrosswordGenerator(wordlist)
    result = generator.generate()
    
    # make sure result is false
    assert result == None