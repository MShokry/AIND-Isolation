#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Feb 14 09:33:45 2018

@author: mshokry
"""


import unittest
import timeit

import isolation
import game_agent


class IsolationTest(unittest.TestCase):
   
   def create_clock(self, time_limit=150):
       time_millis = lambda: 1000 * timeit.default_timer()
       start = time_millis()
       return lambda: start + time_limit - time_millis()

   def test_alphabeta(self):
       player = game_agent.AlphaBetaPlayer()
       player.time_left = self.create_clock()

       # we are only interested in player 1 here, so we do not initialize player 2
       board = isolation.Board(player, None, 9, 9)
       player_loc = (6, 6)
       player_loc_encoded = player_loc[0] + player_loc[1] * 9

       # the last row contains information about the current player and both players' current locations
       board._board_state = [0, 0, 1, 0, 0, 0, 0, 0, 0,
                             0, 0, 0, 1, 0, 0, 0, 0, 0,
                             0, 1, 0, 1, 1, 1, 0, 0, 0,
                             0, 0, 1, 1, 1, 1, 1, 0, 0,
                             0, 0, 1, 1, 1, 1, 1, 0, 0,
                             0, 0, 0, 1, 0, 0, 1, 0, 0,
                             0, 0, 1, 1, 1, 1, 1, 0, 0,
                             0, 0, 0, 0, 1, 0, 0, 0, 0,
                             0, 0, 0, 0, 0, 0, 0, 0, 0,
                             0, 21, player_loc_encoded]

       # search depth 1
       best_move = player.alphabeta(board, 1)
       self.assertEquals((7, 4), best_move, 'best move: ' + str(best_move))

if __name__ == '__main__':
   unittest.main()