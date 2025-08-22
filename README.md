# Crossword Generator

A web-based crossword puzzle generator built with Python and Flask.
Users submit a list of words, and the app generates a crossword layout by placing words on a grid based on shared letters and optimal placement logic.

Try the [live demo](https://crossword-ekp6.onrender.com/)!

## Features

- Recursive backtracking algorithm for efficient word placement
- Grid scoring system to prioritize overlapping intersections
- Front-end form validation
- Image rendering of finalized crossword puzzles using Pillow
- Unit tests using pytest for core logic components

## Installation and usage

Clone repo, create virtual environment and install requirements.

```bash
git clone https://github.com/juliavillela/crossword.git
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

You can then run the application using flask or the command-line interface script:

### Run the flask application
Run the flask application from `crossword/src/`:
```bash
flask run
```
Then go to http://127.0.0.1:5000 in your browser.

### Run the CLI application
From `crossword/` (project root):
```bash
python3 -m src.utils.cli
```

### Additional scripts

#### Run the CLI evaluation script
This internal script is meant to evaluate the performance and memory usage of crossword generator.
Run the default evaluation with no arguments:
```bash
python3 -m src.utils.evaluate
```
Run the evaluation with a custom word list (space-separated):
```bash
python3 -m src.utils.evaluate WORD1 WORD2 WORD3 ...
```

#### Run tests
From `crossword/src/`:
```bash
pytest
```

## Project Structure
```
src/
│
├── app.py                     # Flask app entry point
├── helpers.py                 # Helper functions used by views to clean user input
├── templates/                 # Jinja2 templates for the frontend
├── static/                    # CSS and images
│
├── crosword_generator/        # Core crossword construction logic
│   ├── word_placement_grid.py    # WordPlacementGrid: manages the puzzle grid
│   ├── generate.py               # RecursiveCrosswordGenerator and logic
│   ├── crossword.py              # Crossword: exports and renders the final puzzle
│   └── constants.py              # Shared constants (e.g., directions, max grid size)
│
├── tests/                     # Unit tests for core logic
│   ├── test_crossword.py
│   ├── test_generate_iterative.py
│   ├── test_generate_recursive.py
│   └── test_word_placement_grid.py
│
├── utils/                     # Internal tools not exposed to users
│   ├── cli.py                    # CLI for generating crossword puzzles from custom word lists
│   └── evaluate.py               # CLI for performance and memory evaluation
│
└── requirements.txt           # Python dependencies
```
