"""
This module is intended for internal development diagnostics.
It is not invoked during normal crossword generation or user-facing functionality.

It allows performance comparisons between different crossword generation strategies
(e.g., recursive vs. iterative), tracking metrics like execution time, memory usage,
and operation counts.

Meant to be run manually for evaluation purposes.
"""

import time
import tracemalloc

from crosword_generator.generate import RecursiveCrosswordGenerator, IterativeCrosswordGenerator

short_word_list = ["CATS", "STEM", "MATTE", "DREAM"] # 4 short words
average_word_list = ["CATS", "PRIORITY", "DRIVER", "PIPE", "CARS", "DREAM", "EVOLVE", "BEST", "AVERAGE", "STORM", "FOUNTAIN"]
long_word_list = ["CATS", "PRIORITY", "DRIVER", "PIPE", "CARS", "DREAM", "EVOLVE", "BEST", "AVERAGE", "STORM", "FOUNTAIN"
                  "DIGEST", "MACROBIOTIC", "ABSOLUTE", "DERIVED", "ANGUISH", "AMBIGUOUS", "DEVELOP", "WINDOW", "PENCIL",
                  "ABSTRACT", "TERRIBLE" 
                  ]
very_long_word_list = ["CATS", "PRIORITY", "DRIVER", "DREADFULL", "STRATEGY", "DAMSEL", "EVOLVE", "DURABILITY", "AVERAGE", "STORM", "FOUNTAIN"
                  "DIGEST", "MACROBIOTIC", "ABSOLUTE", "DERIVED", "ANGUISH", "AMBIGUOUS", "DEVELOP", "WINDOW", "PENCIL",
                  "ABSTRACT", "TERRIBLE", "IDIOTIC", "TREMBLE", "ANTHONY", "ABSRTRACT", "DINOSSAUR", "SKYLIGHT", "TREACHERY", "DEFENSE", "FORMATIVE"
                  ]


class Evaluate:
    def __init__(self, generator):
        self.generator_class = generator
        self.time = None
        self.peak_memory = None
        self.current_memory = None

    def run(self,word_list):
        self.word_count = len(word_list)
        self.generator = self.generator_class(word_list)
        start = time.time()
        tracemalloc.start()
        self.generator.generate()
        self.current_memory, self.peak_memory = tracemalloc.get_traced_memory()
        end = time.time()
        tracemalloc.stop()
        self.time = end - start
        
    def results(self):
        print()
        print("-"*5, self.generator_class.__name__, f"({self.word_count} words)", "-"*5)
        print(f"time elapsed: {round(self.time,4)}")
        print(f"peak memory usage: {(self.peak_memory//1000)}KB")
        print(f"current memory usage: {self.current_memory//1000}KB")
        if isinstance(self.generator, RecursiveCrosswordGenerator):
            print(f"operations count: {self.generator.recursion_counter}")
            print(f"max recursion depth: {self.generator.max_recursion_depth}")
        else:
           print(f"operations count: {self.generator.iteration_count}") 


def evaluate(generator_class):
    eval = Evaluate(generator_class)
    lists= [short_word_list, average_word_list, long_word_list, very_long_word_list]
    for list in lists:
        eval.run(list)
        eval.results()