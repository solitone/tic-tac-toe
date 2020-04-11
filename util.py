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
# Minor changes to Carsten Friedrich's code
#
import time
#from IPython.display import HTML, display
import matplotlib
import matplotlib.pyplot as plt
import numpy as np

from tic_tac_toe.Board import Board, GameResult, CROSS, NAUGHT, EMPTY
from tic_tac_toe.Player import Player

## HTML output
# def print_board(board):
#     display(HTML("""
#     <style>
#     .rendered_html table, .rendered_html th, .rendered_html tr, .rendered_html td {
#       border: 1px  black solid !important;
#       color: black !important;
#     }
#     </style>
#     """+board.html_str()))

# ASCII output
def print_board(board):
    board.print_board()

def play_game(board: Board, player1: Player, player2: Player, silent: bool = True):
    player1.new_game(CROSS)
    player2.new_game(NAUGHT)
    board.reset()

    if not silent:
        print()
        board.print_board()
        time.sleep(1)

    finished = False
    while not finished:
        # player1 move
        result, finished = player1.move(board)
        if not silent:
            print()
            print("{} move:".format(player1.name))
            board.print_board()
            time.sleep(1)
        if finished:
            if result == GameResult.DRAW:
                final_result = GameResult.DRAW
            else:
                final_result =  GameResult.CROSS_WIN
        else:
            # player 2 move
            result, finished = player2.move(board)
            if not silent:
                print()
                print("{} move:".format(player2.name))
                board.print_board()
                time.sleep(1)
            if finished:
                if result == GameResult.DRAW:
                    final_result =  GameResult.DRAW
                else:
                    final_result =  GameResult.NAUGHT_WIN

    player1.final_result(final_result)
    player2.final_result(final_result)

    if not silent:
        print()
        if final_result == GameResult.CROSS_WIN:
            print("{} wins!".format(player1.name))
        elif final_result == GameResult.NAUGHT_WIN:
            print("{} wins!".format(player2.name))
        else:
            print("Draw!")
    return final_result

def battle(player1: Player, player2: Player, num_games: int = 100000, silent: bool = False):
    board = Board()
    draw_count = 0
    cross_count = 0
    naught_count = 0
    if not silent:
        print("Battling", end = "", flush = True)

    for _ in range(1, num_games+1):
        result = play_game(board, player1, player2)
        if result == GameResult.CROSS_WIN:
            cross_count += 1
        elif result == GameResult.NAUGHT_WIN:
            naught_count += 1
        else:
            draw_count += 1
        if not silent and _ % 1000 == 0:
            print(".", end = "", flush = True)

    if not silent:
        print()
        print("After {} game we have draws: {}, {} wins: {}, and {} wins: {}.".format(num_games, draw_count,
                                                                                            player1.name, cross_count,
                                                                                            player2.name, naught_count))

        print("Which gives percentages of draws: {:.2%}, {} wins: {:.2%}, and {} wins:  {:.2%}".format(
            draw_count / num_games, player1.name, cross_count / num_games, player2.name, naught_count / num_games))
        print()

    return cross_count, naught_count, draw_count

def eval_players(p1 : Player, p2 : Player, num_battles : int, games_per_battle = 100, loc='best'):
    p1_wins = []
    p2_wins = []
    draws = []
    count = []

    for i in range(num_battles):
        p1win, p2win, draw = battle(p1, p2, games_per_battle, True)
        p1_wins.append(p1win*100.0/games_per_battle)
        p2_wins.append(p2win*100.0/games_per_battle)
        draws.append(draw*100.0/games_per_battle)
        count.append(i*games_per_battle)
        p1_wins.append(p1win*100.0/games_per_battle)
        p2_wins.append(p2win*100.0/games_per_battle)
        draws.append(draw*100.0/games_per_battle)
        count.append((i+1)*games_per_battle)

    plt.ylabel('Game outcomes in %')
    plt.xlabel('Game number')

    plt.plot(count, draws, 'r-', label='Draw')
    plt.plot(count, p1_wins, 'g-', label=p1.name + ' wins')
    plt.plot(count, p2_wins, 'b-', label=p2.name + ' wins')
    plt.legend(loc=loc, shadow=True, fancybox=True, framealpha =0.7)

    plt.show()
