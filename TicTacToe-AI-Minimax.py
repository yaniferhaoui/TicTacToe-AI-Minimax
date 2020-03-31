#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 15 14:30:20 2020

@author: Yani Ferhaoui et Raphael Feher
"""

from math import inf as infinity
from enum import Enum
import random

class Result(Enum):
    LOSE = 1
    WIN = 2
    DRAW = 3
    CONTINUE = 4

class TicTacToe:

    def __init__(self) :
        self.opponent = "o"
        self.computer = "x"
        self.matrix = [
                ["_", "_", "_"],
                ["_", "_", "_"],
                ["_", "_", "_"]
                ]

    def print_matrix(self) :
        print("\n ", "0", "1", "2", "X")
        for i in range(len(self.matrix)):
            print(str(i), self.matrix[i][0], self.matrix[i][1], self.matrix[i][2])
        print("Y")

    def actions(self) :
        actions = []
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[i])):
                if self.matrix[i][j] == "_" :
                    actions.append((i, j))
        random.shuffle(actions)
        return actions

    def result(self, position, player):
        self.matrix[position[0]][position[1]] = player
        
    def is_empty(self):
        for line in self.matrix:
            for elem in line:
                if elem != "_":
                    return False
        return True

    def is_full(self):
        for line in self.matrix:  
            if "_" in line :
                return False
        return True
    
    def win_indexes(self, n):
    
        # Rows
        for r in range(n):
            yield [(r, c) for c in range(n)]
        # Columns
        for c in range(n):
            yield [(r, c) for r in range(n)]
        # Diagonal top left to bottom right
        yield [(i, i) for i in range(n)]
        # Diagonal top right to bottom left
        yield [(i, n - 1 - i) for i in range(n)]
    
    def is_winner(self, decorator):
        for indexes in self.win_indexes(len(self.matrix)):
            if all(self.matrix[r][c] == decorator for r, c in indexes):
                return True
        return False
    
    def terminal_test(self):
    
        # If opponent Win
        if self.is_winner(self.opponent) == True:
            return Result.LOSE
        
        # If the computer Win
        if self.is_winner(self.computer) == True:
            return Result.WIN
        
        # If Draw
        if self.is_full() == True:
            return Result.DRAW
        
        # Else Continue
        return Result.CONTINUE
    
    # depth allow to calculate the best result with the the less actions
    def calculate_score(self, res, depth):
        if res == Result.LOSE:
            return -10 + depth
        elif res == Result.WIN:
            return 10 - depth
        return 0

    def max_value(self, depth = 0):
        
        res = self.terminal_test()
        if res != Result.CONTINUE:
            return self.calculate_score(res, depth), None
        
        # Default start value
        v = -infinity   
        for action in self.actions():
            
            self.result(action, self.computer)
            res = self.min_value(depth + 1)[0]

            # Undo the last action
            self.result(action, "_")
            if res > v :
                v, best_action = res, action

        return v, best_action
    
    def min_value(self, depth = 0) :
        
        res = self.terminal_test()
        if res != Result.CONTINUE:
            return self.calculate_score(res, depth), None
        
        # Default start value
        v = +infinity
        for action in self.actions():

            self.result(action, self.opponent)
            res = self.max_value(depth + 1)[0]

            # Undo the last action
            self.result(action, "_")
            if res < v :
                v, least_action = res, action
                
        return v, least_action
    
    # To play
    def is_valid_cell(self, x, y):
        
        if self.matrix[y][x] != "_":
            print("This cell is already used !")
            return False
        return True
    
    def play(self):
        
        print("\nComputer choices are optimized by minimax algorithm and randomized (if equals) !\n")
        starter = ask_valid_boolean("Do you begin ? [Y/n] :")
        
        if starter == False:
            print("\nThe first computer choice is slow because lot of possibilities (~= 10seconds) !\n")
        
        while game.terminal_test() == Result.CONTINUE:
            
            if starter == True:
                game.print_matrix()
                pos = None
                while pos is None:
                    x = ask_valid_int(0, len(self.matrix) - 1, "Enter X: ")
                    y = ask_valid_int(0, len(self.matrix) - 1, "Enter Y: ")
                    
                    if self.is_valid_cell(x, y):
                        pos = (y, x)
                game.result(pos, game.opponent)
                starter = False
                
            else:
                print("The computer is playing...")
			
                bestMove = game.max_value()[1]
                game.result(bestMove, game.computer)
                starter = True
        
        print("\n\nEnd ! Computer result => " + str(game.terminal_test()))
        game.print_matrix()    
        

def ask_valid_int(the_min, the_max, title):
    
    nb = None
    while nb is None:
        input_value = input(title)
        try:
            nb = int(input_value)
        except ValueError:
            # tell the user off
            print(f"{input_value} is not a number, please enter a int only !")
        
        if nb is not None and (nb < the_min or nb > the_max):
            nb = None
            print(f"Please select number between {the_min} and {the_max} !")
    return nb

def ask_valid_boolean(title):
    
    yes = {'yes','y', 'ye'}
    no = {'no','n'}
    res = None
    
    while res is None:
        choice = input(title).lower()
        if choice in yes:
            res = True
        elif choice in no:
            res = False
    return res

  
game = TicTacToe()
game.play()