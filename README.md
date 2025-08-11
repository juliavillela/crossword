# Crossword Generator

A web-based crossword puzzle generator built with Python and Flask.
Users submit a list of words, and the app generates a crossword layout by placing words on a grid based on shared letters and optimal placement logic.

Try the [live demo](https://juliavillela.pythonanywhere.com/)!

## Features

- Recursive backtracking algorithm for efficient word placement
- Grid scoring system to prioritize overlapping intersections
- Front-end form validation
- Image rendering of finalized crossword puzzles using Pillow
- Unit tests using pytest for core logic components

## Installation and usage

Clone repo and install requirements.

```bash
git clone https://github.com/juliavillela/crossword.git
cd crossword-generator/src
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run the flask aplication
Run the flask application from `crossword-generator/src/`:
```bash
flask run
```
Then go to http://127.0.0.1:5000 in your browser.

### Run the CLI application
From crossword/ (project root):
```bash
python3 -m src.utils.cli
```

### Run tests
From `crossword-generator/src/`:
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
│   └── evaluate.py               # Script for performance and memory evaluation
│
└── requirements.txt           # Python dependencies
```