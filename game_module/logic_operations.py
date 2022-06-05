import numpy as np
import itertools

import networkx as nx

from game_module.game_constants import *


def xy_to_col_row(x, y, size):
    inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (size - 1)
    x_dist = x - BOARD_BORDER
    y_dist = y - BOARD_BORDER
    col = int(round(x_dist / inc))
    row = int(round(y_dist / inc))
    return col, row


def col_row_to_xy(col, row, size):
    inc = (BOARD_WIDTH - 2 * BOARD_BORDER) / (size - 1)
    x = int(BOARD_BORDER + col * inc)
    y = int(BOARD_BORDER + row * inc)
    return x, y


def has_no_liberties(board, group):
    for x, y in group:
        if x > 0 and board[x - 1, y] == 0:
            return False
        if y > 0 and board[x, y - 1] == 0:
            return False
        if x < board.shape[0] - 1 and board[x + 1, y] == 0:
            return False
        if y < board.shape[0] - 1 and board[x, y + 1] == 0:
            return False
    return True


def get_stone_groups(board, color):
    size = board.shape[0]
    color_code = 1 if color == "black" else 2
    xs, ys = np.where(board == color_code)
    graph = nx.grid_graph(dim=[size, size])
    stones = set(zip(xs, ys))
    all_spaces = set(itertools.product(range(size), range(size)))
    stones_to_remove = all_spaces - stones
    graph.remove_nodes_from(stones_to_remove)
    return nx.connected_components(graph)


def is_valid_move(col, row, board):
    if col < 0 or col >= board.shape[0]:
        return False
    if row < 0 or row >= board.shape[0]:
        return False
    return board[col, row] == 0


def make_grid(size):
    start_points, end_points = [], []

    # vertical start points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    ys = np.full(size, BOARD_BORDER)
    start_points += list(zip(xs, ys))

    # horizontal start points (constant x)
    xs = np.full(size, BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    start_points += list(zip(xs, ys))

    # vertical end points (constant y)
    xs = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    ys = np.full(size, BOARD_WIDTH - BOARD_BORDER)
    end_points += list(zip(xs, ys))

    # horizontal end points (constant x)
    xs = np.full(size, BOARD_WIDTH - BOARD_BORDER)
    ys = np.linspace(BOARD_BORDER, BOARD_WIDTH - BOARD_BORDER, size)
    end_points += list(zip(xs, ys))

    return start_points, end_points
