import pytest
from crosword_generator.constants import *
from crosword_generator.generate import CrosswordGenerator
from crosword_generator.crossword import Crossword
from crosword_generator.word_placement_grid import WordPlacementGrid

def test_initialization():
    generator = CrosswordGenerator(["bat","cats"])

    # make sure words are sorted by descending length
    assert generator.words == ["cats", "bat"]

    # make sure grid size is larger than or equal to largest word
    assert generator.grid_size >= 4

# tests on easy word lists should return a sucessfull grid
def test_attempt_build_grid_returns_WordPlacementGrid():
    wordlist = [
        "aaa", "aaaa", "aaaaa"
    ]
    generator = CrosswordGenerator(wordlist)
    result = generator._attempt_grid_build()
    # make sure result is an instance of WordPlacementGrid
    assert isinstance(result, WordPlacementGrid)
    
    # make sure all words have been placed
    placed_words = set(result.get_words())
    assert placed_words == set(wordlist)

def test_retry_grid_builds_returns_WordPlacementGrid():
    wordlist = [
        "aaa", "aaaa", "aaaaa"
    ]
    generator = CrosswordGenerator(wordlist)
    result = generator._retry_grid_builds()

    # make sure result is an instance of WordPlacementGrid
    assert isinstance(result, WordPlacementGrid)
    
    # make sure all words have been placed
    placed_words = set(result.get_words())
    assert placed_words == set(wordlist)

def test_generate_returns_Crossword():
    wordlist = [
        "aaa", "aaaa", "aaaaa"
    ]
    generator = CrosswordGenerator(wordlist)
    result = generator.generate()
    assert isinstance(result, Crossword)

# tests on impossible word list should return none
def test_attempt_build_grid_returns_incomplete_grid_for_impossible_word_list():
    wordlist = [
        "aaa", "bbb", "ccc"
    ]
    generator = CrosswordGenerator(wordlist)
    result = generator._attempt_grid_build()
    
    # make sure result is an instance of WordPlacementGrid
    assert isinstance(result, WordPlacementGrid)
    
    # make sure only first word was placed
    placed_words = result.get_words()
    assert len(placed_words) == 1

def test_retry_grid_builds_returns_none_for_impossible_word_list():
    wordlist = [
        "aaa", "bbb", "ccc"
    ]
    generator = CrosswordGenerator(wordlist)
    result = generator._retry_grid_builds()

    assert result == None

def test_generate_returns_none_for_impossible_word_list():
    wordlist = [
        "aaa", "bbb", "ccc"
    ]
    generator = CrosswordGenerator(wordlist)
    result = generator.generate()

    assert result == None