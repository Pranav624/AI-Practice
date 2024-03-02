import numpy as np, random, time, gym
from Connect4.Connect4 import *

class C4Env:
    def __init__(self, board, turn, win_reward, lose_reward, invalid_move_reward):
        self.__board = board
        self.__turn = turn
        self.__win_reward = win_reward
        self.__lose_reward = lose_reward
        self.__invalid_move_reward = invalid_move_reward
        self.__win_table = create_win_table()

    def reset(self):
        self.__board = [['.' for _ in range(7)] for _ in range(6)]

    def step(self, action):
        reward = 0
        try:
            next_state = make_move(action, self.__turn, self.__board)
            self.__board = next_state
        except:
            reward += self.__invalid_move_reward
            raise ValueError

        game_over, turn = end_test(self.__board, self.__win_table)
        score = heuristic(self.__board, self.__turn, self.__win_table, 0)
        reward += score
        return self.__board, reward, game_over
    
    def render(self):
        print(display(self.__board))