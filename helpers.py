import os 
from .crosword_generator.constants import *

def validate_word_list(word_list):
    """
    Raises an error if word list does not meet any of the criteria

    A word_list is valid if:
    - it has more than MIN_WORDS and less than MAX_WORDS.
    - no words in list are either too long or too short
    - each word has at least one char in common with another word.
    """
    # word list is of adequate length
    if len(word_list) > MAX_WORDS or len(word_list) < MIN_WORDS:
        message = f"word list should have between {MIN_WORDS} and {MAX_WORDS}, not {len(word_list)}"
        return (False, message)
    # no words are too long
    too_long = [w for w in word_list if len(w)>MAX_WORD_LEN]
    if len(too_long):
        message = f"word list contains words that are longer than {MAX_WORD_LEN}: {too_long}"
        return (False, message)
    
    # no words are too short
    too_short = [w for w in word_list if len(w)<MIN_WORD_LEN]
    if len(too_short):
        message = f"word list contains words that are shorter than {MIN_WORD_LEN}: {too_short}"
        return (False, message)
        
    # words should have at least one char in common with another word        
    for i, word1 in enumerate(word_list):
        found_common = False
        for j, word2 in enumerate(word_list):
            if i != j:  # Skip comparing the word with itself
                if any(char in word2 for char in word1):
                    found_common = True
                    break
        if not found_common:
            message = f"word list is impossible. word '{word1}' has no chars in common with other words"
            return (False, message)    
    return (True, "will generate puzzle")

def clean_word_list_input(word_list):
    return [word.lower() for word in word_list]

def delete_session_files(session, media_folder):
    key_file = os.path.join(media_folder, f'{session.get("session_id")}key.png')
    if os.path.exists(key_file):
        os.remove(key_file)
    
    blank_file = os.path.join(media_folder, f'{session.get("session_id")}blank.png')
    if os.path.exists(blank_file):
        os.remove(blank_file)