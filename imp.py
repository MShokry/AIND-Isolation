#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Jan 13 08:27:53 2018

@author: mshokry
"""
from copy import deepcopy

xlim, ylim = 3,2

class GameState:
    """
        This Class is to keep track of the Game state
        including
        _state : current game state "open and close points"
                0 is clear 1 is blocked => block (2,1)
        _turn : who is playing
            0 computer : 1 player 2
        _current_location : Each player current position 
            array with two tubles []
    
    """
    def __init__(self):
        self._board = [[0]*ylim for i in range(xlim)]
        self._board[-1][-1] = 1 #lower corner 
        self._turn = 0
        self._current_location = [None,None]
    
    def forecast_move(self, move):
        """ Return a new board object with the specified move
        applied to the current game state.
        
        Parameters
        ----------
        move: tuple
            The target position for the active player's next move
        """
        if move not in self.get_legal_moves():
            raise RuntimeError("Attempted forecast of illegal move")
        last_Board = deepcopy(self)
        last_Board._board[move[0]][move[1]] = 1
        last_Board._current_location[self._turn] = move
        last_Board._turn ^= 1 #Xor inver current value 
        return last_Board
    
    def get_legal_moves(self):
        """ Return a list of all legal moves available to the
        active player.  Each player should get a list of all
        empty spaces on the board on their first move, and
        otherwise they should get a list of all open spaces
        in a straight line along any row, column or diagonal
        from their current position. (Players CANNOT move
        through obstacles or blocked squares.) Moves should
        be a pair of integers in (column, row) order specifying
        the zero-indexed coordinates on the board.
        """
        last = self._current_location[self._turn]
        if not last : #first move 
            return self.blank()#empty board
        moves = []
        directions = [ (-1, -1), (-1, 0), (-1, 1),
                        (0, -1),          (0,  1),
                        (1, -1), (1, 0), (1, 1)]
        for dirx,diry in directions: #avialble directions
            x,y = last #get last location
            while 0 <= x+dirx < xlim and 0 <= y+diry < ylim: #while inside the board
                x,y = x+dirx,y+diry #take a step
                if self._board[x][y]:
                    break #move untill hit a used box
                moves.append((x,y)) #else its a valid move 
        return moves
        
    def blank(self):
        return [(x,y) for y in range(ylim) for x in range(xlim) if self._board[x][y] == 0]
    
#%%
print("Creating empty game board...")
g = GameState()

print("Getting legal moves for player 1...")
p1_empty_moves = g.get_legal_moves()
print("Found {} legal moves.".format(len(p1_empty_moves or [])))

print("Applying move (0, 0) for player 1...")
g1 = g.forecast_move((0, 0))

print("Getting legal moves for player 2...")
p2_empty_moves = g1.get_legal_moves()
if (0, 0) in set(p2_empty_moves):
    print("Failed\n  Uh oh! (0, 0) was not blocked properly when " +
          "player 1 moved there.")
else:
    print("Everything looks good!")

print("Applying move (0, 0) for player 1...")
g1 = g1.forecast_move((1, 1))

print("Getting legal moves for player 2...")
p2_empty_moves = g1.get_legal_moves()

#%%
def terminal_test(gameState):
    """ Return True if the game is over for the active player
    and False otherwise.
    """
    return not bool(gameState.get_legal_moves())


def min_value(gameState):
    """ Return the value for a win (+1) if the game is over,
    otherwise return the minimum value over all legal child
    nodes.
    """
    if terminal_test(gameState):
        return 1
    val = float("inf")
    for move in gameState.get_legal_moves():
        val = min(val,max_value(gameState.forecast_move(move)))
        #print("Min",move)
    return val

def max_value(gameState):
    """ Return the value for a loss (-1) if the game is over,
    otherwise return the maximum value over all legal child
    nodes.
    """
    if terminal_test(gameState):
        return -1
    val = float("-inf")
    for move in gameState.get_legal_moves():
        val = max(val,min_value(gameState.forecast_move(move)))
        #print("MAx",move)
    return val
#%%
    
g = GameState()

print("Calling min_value on an empty board...")
v = min_value(g)

if v == -1:
    print("min_value() returned the expected score!")
else:
    print("Uh oh! min_value() did not return the expected score.")
#%%
def minimax_decision(gameState):
    """ Return the move along a branch of the game tree that
    has the best possible value.  A move is a pair of coordinates
    in (column, row) order corresponding to a legal move for
    the searching player.
    
    You can ignore the special case of calling this function
    from a terminal state.
    """
    return max(gameState.get_legal_moves(),key = lambda x: min_value(gameState.forecast_move(x)))
#%% TEST
    
best_moves = set([(0, 0), (2, 0), (0, 1)])
rootNode = GameState()
minimax_move = minimax_decision(rootNode)

print("Best move choices: {}".format(list(best_moves)))
print("Your code chose: {}".format(minimax_move))

if minimax_move in best_moves:
    print("That's one of the best move choices. Looks like your minimax-decision function worked!")
else:
    print("Uh oh...looks like there may be a problem.")