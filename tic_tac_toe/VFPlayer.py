#######################################################################
# Copyright (C)                                                       #
# 2020 solitone (https://github.com/solitone)                         #
#                                                                     #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################

import numpy as np
from typing import Dict, List
from enum import Enum
from tic_tac_toe.Board import Board, GameResult, NAUGHT, CROSS
from tic_tac_toe.Player import Player

WIN_VALUE = 1.0  # type: float
DRAW_VALUE = 0.5  # type: float
LOSS_VALUE = 0.0  # type: float

class MoveStrategy(Enum):
    """
    Enum to encode different player's move strategies. A VFPlayer may exploit
    her current knowledge to choose her next move (EXPLOITATION) or try a
    random move to explore board states not yet encountered (EXPLORATION).
    """
    EXPLOITATION = 0
    EXPLORATION = 1

class VFPlayer(Player):
    """
    A Tic Tac Toe player, implementing the Value Funcition method
    described in Reinforcement Learning — An Introduction
    by Richard S. Sutton and Andrew G. Barto, paragraph 1.5
    """

    def __init__(self, name: str = "VFPlayer", learning_rate=0.1, exploration_rate=0.01, v_draw=DRAW_VALUE, v_init=0.6):
        """
        Called when creating a new TQPlayer. Accepts some optional parameters to define its learning behaviour
        :param learning_rate: step-size parameter, needs to be larger than 0 and smaller than 1
        :param exploration_rate: probability to choose a random exploratory move, needs to be larger than 0 and smaller than 1
        :param v_draw: The value of draw states,  needs to be between 0 and 1
        :param v_init: The initial value for each state, apart from winning states
        """
        self.side = None
        self.v = {}  # type: Dict[int, np.ndarray]
        self.move_history = []  # type: List[(int, int)]: (state_hash, move)
        self.alpha = learning_rate
        self.epsilon = exploration_rate
        self.move_strategy = MoveStrategy.EXPLOITATION
        self.v_win = WIN_VALUE
        self.v_draw = v_draw
        self.v_loss = LOSS_VALUE
        self.v_init = v_init
        super().__init__(name)

    def set_exloration_rate(self, exploration_rate: float):
        """
        Allows to change the exploration rate
        :param exploration_rate: probability to choose a random exploratory move, needs to be larger than 0 and smaller than 1
        """
        self.epsilon = exploration_rate

    def get_v(self, board: Board) -> np.ndarray:
        """
        Returns all values when moving from current state of 'board'
        :param board: The current board state
        :return: List of values of all possible next board states
        """
        # We build the value dictionary in a lazy manner, only adding a state when it is actually used for the first time
        #
        board_hash = board.hash_value() # needed because value dictionary maps *hashed* state to values
        if board_hash in self.v:
            vals = self.v[board_hash]
        else:
            vals = np.full(9, self.v_init) # default initial value
            # set values for winning states to WIN_VALUE
            # (player cannot end up in a losing state after a move
            # so losing states need not be considered):
            for pos in range(vals.size): # vals.size = BOARD_SIZE
                if board.is_legal(pos):
                    b = Board(board.state)
                    b.move(pos, self.side)
                    if b.check_win():
                        vals[pos] = self.v_win
                    elif b.num_empty() == 0:
                        # if it is not a win, and there are no other positions
                        # available, then it is a draw
                        vals[pos] = self.v_draw
            # Update dictionary:
            self.v[board_hash] = vals
#            print("v[{}]={}".format(board_hash, self.v[board_hash]))
        return vals

    def get_move(self, board: Board) -> int:
        """
        Return the next move given the board `board` based on the current values of next states
        :param board: The current board state
        :return: The next move based on the current values of next states, starting from input state
        """
        if self.move_strategy == MoveStrategy.EXPLORATION:
            # exploratory random move
            m = board.random_empty_spot()
            _ = self.get_v(board) # just to ensure we have values for our board state
            return m
        else:
            # greedy move: exploiting current knowledge
            vals = self.get_v(board)  # type: np.ndarray
            while True:
                maxv_idxs = np.argwhere(vals == np.amax(vals)) # positions of max values in array
                m = np.random.choice(maxv_idxs.flatten().tolist())    # type: int
                #m = np.argmax(vals)  # type: int # this instead would return 1st occurance
                if board.is_legal(m):
#                    print("vals=", end='')
#                    print(vals)
#                    print("m={}".format(m))
                    return m
                else:
                    vals[m] = -1.0

    def move(self, board: Board):
        """
        Makes a move and returns the game result after this move and whether the move ended the game
        :param board: The board to make a move on
        :return: The GameResult after this move, Flag to indicate whether the move finished the game
        """
        # Select strategy to choose next move: exploit known or explore unknown?
        if np.random.uniform(0, 1) <= self.epsilon:
            self.move_strategy = MoveStrategy.EXPLORATION
        else:
            self.move_strategy = MoveStrategy.EXPLOITATION

        m = self.get_move(board)
        self.move_history.append((board.hash_value(), m))
        self.backup_value()
#        print("v={}".format(self.v))
        _, res, finished = board.move(m, self.side)
        return res, finished

    def backup_value(self):
        """
        Updates previous state value according to chosen next state value.
        Refer to figure 1.1 in Sutton and Barto's book.

        """
#        print("move_strategy={}".format(self.move_strategy))
#        print("move_history={}".format(self.move_history))
        if self.move_strategy == MoveStrategy.EXPLOITATION and len(self.move_history) > 1:
            # Exlopratory move do not result in any learning.
            # Value update needed only if already played at least 2 moves.
            # Contrary to figure 1.1 in the book, if opponent plays first,
            # there is no need to update the initial state (empty board) value,
            # since the VFPLayer has not to choose any move from that position.
            prev_state_hash = self.move_history[-2][0]
            prev_move = self.move_history[-2][1]
            prev_value = self.v[prev_state_hash][prev_move]
#            print("prev_hash={}, prev_move={}, prev_val={}".format(prev_state_hash, prev_move, prev_value))

            next_state_hash = self.move_history[-1][0]
            next_move = self.move_history[-1][1]
            next_value = self.v[next_state_hash][next_move]
#            print("next_hash={}, next_move={}, next_val={}".format(next_state_hash, next_move, next_value))

            # Update rule:
            prev_value += self.alpha * (next_value - prev_value)
            # Update value dictionary
            self.v[prev_state_hash][prev_move] = prev_value
#            print("new prev_val={}".format(self.v[prev_state_hash][prev_move]))

    def final_result(self, result: GameResult):
        """
        If opponent last move results in a loss or a draw, we need to update
        the value of our last move (the penultimate overall move). If we
        have the last move in a game, nothing is needed here, we learn *during*
        the game after each of our moves, and not *at the end* of the game.
        :param result: The result of the game that just finished
        """
        if (result == GameResult.NAUGHT_WIN and self.side == NAUGHT) or (
                result == GameResult.CROSS_WIN and self.side == CROSS):
            # do nothing
            return
        if (result == GameResult.NAUGHT_WIN and self.side == CROSS) or (
                result == GameResult.CROSS_WIN and self.side == NAUGHT):
            final_value = self.v_loss  # type: float
        elif result == GameResult.DRAW:
            final_value = self.v_draw  # type: float
        else:
            raise ValueError("Unexpected game result {}".format(result))

        last_state_hash = self.move_history[-1][0]
        last_move = self.move_history[-1][1]
        # Update value dictionary
        self.v[last_state_hash][last_move] = final_value
 #       print("final v={}".format(self.v))

    def new_game(self, side):
        """
        Called when a new game is about to start. Store which side we will play and reset our internal game state.
        :param side: Which side this player will play
        """
        self.side = side
        self.move_history = []
