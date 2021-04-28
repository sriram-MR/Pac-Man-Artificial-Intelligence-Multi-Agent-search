# Pac-Man-Artificial-Intelligence-Multi-Agent-search

This is a part of Artificial Intelligience course in ASU CSE571. THis was taken in Spring 2020.

Code to run the game.

Reflex agent

python pacman.py -p ReflexAgent -l testClassic

With different layout

python pacman.py {frameTime 0 -p ReflexAgent -k 1
python pacman.py {frameTime 0 -p ReflexAgent -k 2

Minimax agent

python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3
python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4


Alpha-beta pruning

python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic

Expectimax search

python pacman.py -p ExpectimaxAgent -l minimaxClassic -a depth=3

python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10
python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10
