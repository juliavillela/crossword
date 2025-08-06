# Crossword Generator

Generate crossword puzzles from a custom list of words.
Try the [live demo](https://juliavillela.pythonanywhere.com/)!

## Features

- Crossword generation from user-provided word lists
- Recursive word placement with score-based sorting and backtracking
- Puzzle rendering as an image using PIL
- Simple web interface powered by Flask

## Project Structure
src/
│
├── app.py # Flask app entry point
|–– helpers.py 
├── templates/ # Jinja2 templates for frontend
├── static/ # CSS / images
├── crosword_generator/
│ ├── word_placement_grid.py # WordPlacementGrid: manages the puzzle grid
│ ├── generate.py # RecursiveCrosswordGenerator and logic
│ ├── crossword.py # Crossword: exports puzzle + renders to image
│ ├── constants.py # Word list validation logic
└── requirements.txt
