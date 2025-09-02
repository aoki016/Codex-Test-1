#!/usr/bin/env python3
"""Console-based Othello (Reversi) game.

This program lets a human player compete against a simple computer
opponent.  The board is the standard 8x8 grid.  The human player uses
black discs (B) and moves first.  The computer uses white discs (W).

The computer opponent uses a greedy strategy: it evaluates all legal
moves and selects the move that flips the most opponent discs.  When no
legal moves are available for a player, the turn passes to the other
player.  The game ends when neither player can move.  The final score is
then displayed.

The program is intentionally self-contained and uses only the Python
standard library.  It is written for clarity rather than raw efficiency.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Tuple

BOARD_SIZE = 8
EMPTY = "."
BLACK = "B"
WHITE = "W"

Move = Tuple[int, int]
MoveFlips = Dict[Move, List[Move]]


def init_board() -> List[List[str]]:
    """Create the initial Othello board."""
    board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
    mid = BOARD_SIZE // 2
    board[mid - 1][mid - 1] = WHITE
    board[mid][mid] = WHITE
    board[mid - 1][mid] = BLACK
    board[mid][mid - 1] = BLACK
    return board


def print_board(board: List[List[str]]) -> None:
    """Display the board with coordinates."""
    header = "  " + " ".join(chr(ord("A") + i) for i in range(BOARD_SIZE))
    print(header)
    for i, row in enumerate(board):
        print(f"{i + 1} " + " ".join(row))
    print()


def on_board(x: int, y: int) -> bool:
    return 0 <= x < BOARD_SIZE and 0 <= y < BOARD_SIZE


def opponent(player: str) -> str:
    return WHITE if player == BLACK else BLACK


def valid_moves(board: List[List[str]], player: str) -> MoveFlips:
    """Return a mapping of valid moves to the list of discs flipped."""
    moves: MoveFlips = {}
    opp = opponent(player)
    directions = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),         (0, 1),
        (1, -1),  (1, 0),  (1, 1),
    ]

    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] != EMPTY:
                continue
            flips: List[Move] = []
            for dx, dy in directions:
                nx, ny = x + dx, y + dy
                path: List[Move] = []
                while on_board(nx, ny) and board[nx][ny] == opp:
                    path.append((nx, ny))
                    nx += dx
                    ny += dy
                if path and on_board(nx, ny) and board[nx][ny] == player:
                    flips.extend(path)
            if flips:
                moves[(x, y)] = flips
    return moves


def make_move(board: List[List[str]], player: str, move: Move, flips: List[Move]) -> None:
    """Place a disc and flip the captured discs."""
    x, y = move
    board[x][y] = player
    for fx, fy in flips:
        board[fx][fy] = player


def greedy_choice(moves: MoveFlips) -> Optional[Move]:
    """Choose the move that flips the most discs."""
    if not moves:
        return None
    max_flips = max(len(flips) for flips in moves.values())
    best_moves = [move for move, flips in moves.items() if len(flips) == max_flips]
    return random.choice(best_moves)


def scores(board: List[List[str]]) -> Tuple[int, int]:
    b = sum(row.count(BLACK) for row in board)
    w = sum(row.count(WHITE) for row in board)
    return b, w


def parse_move(raw: str) -> Optional[Move]:
    """Parse user input of the form 'row col', e.g. '3 4'."""
    parts = raw.strip().split()
    if len(parts) != 2:
        return None
    try:
        r, c = int(parts[0]) - 1, int(parts[1]) - 1
    except ValueError:
        return None
    if on_board(r, c):
        return r, c
    return None


def main() -> None:
    board = init_board()
    player = BLACK
    skipped = 0

    while True:
        moves = valid_moves(board, player)
        if not moves:
            skipped += 1
            if skipped == 2:
                break
            print(f"{player} has no valid moves and must pass.\n")
            player = opponent(player)
            continue
        skipped = 0

        if player == BLACK:
            print_board(board)
            print("Enter your move as 'row col' (1-8) or 'q' to quit:")
            user_input = input().strip()
            if user_input.lower() == "q":
                print("Game aborted.")
                return
            move = parse_move(user_input)
            if move is None or move not in moves:
                print("Invalid move. Try again.\n")
                continue
            make_move(board, player, move, moves[move])
        else:
            move = greedy_choice(moves)
            assert move is not None
            make_move(board, player, move, moves[move])
            print(f"Computer plays {move[0] + 1} {move[1] + 1}.\n")

        player = opponent(player)

    print_board(board)
    b, w = scores(board)
    print(f"Final score - Black: {b}, White: {w}")
    if b > w:
        print("You win!")
    elif w > b:
        print("Computer wins!")
    else:
        print("It's a draw!")


if __name__ == "__main__":
    main()
