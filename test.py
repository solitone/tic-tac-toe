from tic_tac_toe.Board import Board, GameResult
from tic_tac_toe.RandomPlayer import RandomPlayer
from tic_tac_toe.MinMaxAgent import MinMaxAgent
from tic_tac_toe.RndMinMaxAgent import RndMinMaxAgent
from tic_tac_toe.HumanPlayer import HumanPlayer
from tic_tac_toe.TQPlayer import TQPlayer
from tic_tac_toe.VFPlayer import VFPlayer
from util import *

# battle(RandomPlayer("RandomPlayer1"), RandomPlayer("RandomPlayer2"), num_games=10000)
# battle(MinMaxAgent(), RandomPlayer(), num_games=10000)
# battle(RandomPlayer(), MinMaxAgent(), num_games=10000)
# battle(MinMaxAgent(), RndMinMaxAgent(), num_games=10000)
#play_game(Board(), RndMinMaxAgent(), HumanPlayer(), silent=False)

#play_game(Board(), VFPlayer(), MinMaxAgent(), silent=False)

player1 = VFPlayer("VFPlayer1", learning_rate=0.1, exploration_rate=0.01, v_init=0.6)
#player1 = TQPlayer()
eval_players(player1, RndMinMaxAgent(), 50)
player1.set_exloration_rate(0.0)
eval_players(player1, RndMinMaxAgent(), 50)
while True:
    play_game(Board(), player1, HumanPlayer(), silent=False)
