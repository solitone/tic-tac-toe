#######################################################################
# Copyright (C)                                                       #
# 2020 solitone (https://github.com/solitone)                         #
# 2018 Carsten Friedrich (Carsten.Friedrich@gmail.com).               #
#                                                                     #
# Permission given to modify the code as long as you keep this        #
# declaration at the top                                              #
#######################################################################
#
# 2020.04.09 solitone
# Added this new class to allow human user to play
#
import time
from tic_tac_toe.Board import Board, GameResult
from tic_tac_toe.Player import Player

class HumanPlayer(Player):
    """
    This player plays the game of Tic Tac Toe by using the moves chosen by a human user.
    """

    def __init__(self, name: str = "Human"):
        """
        Getting ready for playing tic tac toe.
        """
        self.side = None
        self.keys = ['q', 'w', 'e', 'a', 's', 'd', 'z', 'x', 'c']
        # keys array maps positions to keyboard keys that user chooses:
        # index is position, value is key
        self.print_instructions()
        time.sleep(2)
        super().__init__(name)

    def move(self, board: Board) -> (GameResult, bool):
        """
        Make move corresponding to key pressed by user
        :param board: The board to make a move on
        :return: The result of the move
        """
        print()
        while True:
            key = input("Your move? ")
            if key in self.keys:
                break
        position = self.keys.index(key)

        _, res, finished = board.move(position, self.side)
        return res, finished

    def final_result(self, result: GameResult):
        """
        Does nothing.
        :param result: The result of the game that just finished
        :return:
        """
        pass

    def new_game(self, side: int):
        """
        Setting the side for the game to come. Noting else to do.
        :param side: The side this player will be playing
        """
        self.side = side

    def print_instructions(self):
        """
        Print out how user can enter moves
        """
        print("To move press key corresponding to position chosen:")
        print(" q | w | e ")
        print("-----------")
        print(" a | s | d ")
        print("-----------")
        print(" z | x | c ")
