# SnakeQlearning
Implementation of Q-learning with the game of snake.

## Dependencies<br>
Code is written in python 3.<br>
The only extra dependecies are:
- Pygame
```
pip3 install pygame
```
- Depending on the Python version, may need to install dataclasses
```
pip3 install dataclasses
```

## To Run
1. First Initialize the Q Table. This will create a text file <i>qvalues.json</i> that is in json format.
```
python3 InitializeQvalues.py
```
2. Run <i>snake.py</i>.<br>
In <i>snake.py</i> there is a constant FRAMESPEED that is set to 50000 to speed up training and play more games faster.
Set this to a smaller number (20-30) to better watch the snake's movements.
```
python3 snake.py
```
