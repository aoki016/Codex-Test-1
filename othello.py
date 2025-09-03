#!/usr/bin/env python3
"""Graphical Othello (Reversi) game using Pygame.

A human player (black) competes against a simple greedy computer
opponent (white).  Click on a square to place a black stone.  The
computer automatically responds with its move.  The game ends when
neither player can move; the final score is printed to the console.
"""

from __future__ import annotations

import random
from typing import Dict, List, Optional, Tuple

import pygame

BOARD_SIZE = 8
CELL_SIZE = 60
BOARD_PIXELS = BOARD_SIZE * CELL_SIZE
BOARD_COLOR = (34, 139, 34)
LINE_COLOR = (0, 0, 0)
BLACK = "B"
WHITE = "W"
EMPTY = "."

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


def draw_board(screen: pygame.Surface, board: List[List[str]]) -> None:
    screen.fill(BOARD_COLOR)
    for i in range(BOARD_SIZE + 1):
        pygame.draw.line(screen, LINE_COLOR, (i * CELL_SIZE, 0), (i * CELL_SIZE, BOARD_PIXELS))
        pygame.draw.line(screen, LINE_COLOR, (0, i * CELL_SIZE), (BOARD_PIXELS, i * CELL_SIZE))
    for x in range(BOARD_SIZE):
        for y in range(BOARD_SIZE):
            if board[x][y] == BLACK:
                color = (0, 0, 0)
            elif board[x][y] == WHITE:
                color = (255, 255, 255)
            else:
                continue
            pygame.draw.circle(
                screen,
                color,
                (y * CELL_SIZE + CELL_SIZE // 2, x * CELL_SIZE + CELL_SIZE // 2),
                CELL_SIZE // 2 - 4,
            )
    pygame.display.flip()


def main() -> None:
    pygame.init()
    screen = pygame.display.set_mode((BOARD_PIXELS, BOARD_PIXELS))
    pygame.display.set_caption("Othello")
    board = init_board()
    player = BLACK
    skipped = 0
    running = True
    clock = pygame.time.Clock()

    while running:
        moves = valid_moves(board, player)
        if not moves:
            skipped += 1
            if skipped == 2:
                break
            player = opponent(player)
            continue
        skipped = 0

        draw_board(screen, board)
        if player == BLACK:
            waiting = True
            while waiting and running:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                        waiting = False
                    elif event.type == pygame.MOUSEBUTTONDOWN:
                        row = event.pos[1] // CELL_SIZE
                        col = event.pos[0] // CELL_SIZE
                        move = (row, col)
                        if move in moves:
                            make_move(board, player, move, moves[move])
                            player = opponent(player)
                            waiting = False
                clock.tick(60)
        else:
            pygame.time.delay(300)
            move = greedy_choice(moves)
            if move:
                make_move(board, player, move, moves[move])
            player = opponent(player)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            clock.tick(60)

    draw_board(screen, board)
    b, w = scores(board)
    print(f"Final score - Black: {b}, White: {w}")
    if b > w:
        print("You win!")
    elif w > b:
        print("Computer wins!")
    else:
        print("It's a draw!")
    pygame.time.delay(2000)
    pygame.quit()


if __name__ == "__main__":
    main()
