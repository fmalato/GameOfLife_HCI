# Conway's Game of Life
A simple Python "Conway's Game of Life" implementation with PyQt5.
The game implements a finite grid and comes with a bunch of features such as pattern loading, variable framerate and cells history.
For further information about the project structure or the strategies that I've been using, read the _GOF.pdf_ report.

## Requirements
I've been using an Anaconda environment with the following packages:
- Pyton 3.x
- PyQt 5.9.2
- numpy 1.18.1

## Installation
To run this project, just clone it, set the virtual environment and run _main.py_.

## Known issues
Being defined over a two dimensional grid, the game will slow down on complex patterns when setting large grids.
