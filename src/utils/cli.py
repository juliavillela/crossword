import os
from ..crosword_generator import CrosswordGenerator
from ..helpers import validate_word_list, clean_word_list_input

def get_desktop_path():
    home = os.path.expanduser("~")
    desktop = os.path.join(home, "Desktop")
    if os.path.isdir(desktop):
        return desktop
    return home  # fallback

def get_valid_wordlist():
    while True:
        raw_input = input("words for puzzle (eg: kitten, mice): ")
        wordlist = raw_input.split(",")
        wordlist = clean_word_list_input(wordlist)
        (valid, message) = validate_word_list(wordlist)
        print(message)
        if valid:
            return wordlist

def get_valid_export_path():
    while True:
        default_path = get_desktop_path()
        path_input = input(f"insert the path to folder where images should be saved (default: {default_path}): ")
        path_input = path_input.strip()
        if not path_input:
            return default_path
        if path_input:
            if not os.path.isdir(path_input):
                print(f"path:'{path_input}' is not a valid folder.")
            else:
                return path_input

def generate_until_satisfied(wordlist:list[str]):
    generator = CrosswordGenerator(wordlist)
    crossword = generator.generate()
    print()
    crossword.display_key_grid()
    while True:
        regenerate = input("generate another option?(Y/N): ")
        regenerate = regenerate.lower() == "y"
        if regenerate:
            crossword = generator.generate()
            print()
            crossword.display_key_grid()
        else:
            return crossword

def save_images(path, crossword):
    if not path.endswith(os.sep):
        path += os.sep
    
    key_path = os.path.join(path, "crossword_key.png")
    blank_path = os.path.join(path, "crossword_blank.png")
    crossword.save_key_img(key_path)
    print(f"key saved to '{key_path}'.")
    crossword.save_blank_img(blank_path)
    print(f"blank puzzle saved to '{blank_path}'")

def main():
    print()
    print("-"*12)
    print("Let's generate a crossword puzzle!\n")
    
    wordlist = get_valid_wordlist()
    crossword = generate_until_satisfied(wordlist)
    export = input("\ndo you want to export crossword as images?(Y/N) ")
    export = export.lower() == "y"
    
    if export:
        path = get_valid_export_path()
        save_images(path, crossword)
    
    print("exiting. goodbye!")
    print("-"*12)
    print()

if __name__ == "__main__":
    main()