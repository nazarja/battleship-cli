from __future__ import annotations
from .leaderboard import Leaderboard
from .helpers import heading
from typing import Dict, List
from random import choice


class Battleship:
    def __init__(self, board: Dict[str, List[int]], leaderboard: Leaderboard):
        self.leaderboard: Leaderboard = leaderboard
        self.height: int = board["height"][2]
        self.width: int = board["width"][2]
        self.ships: int = board["ships"][2]
        self.user_board: List[List[str]] = []
        self.hits_board: List[List[str]] = []
        self.cpu_board: List[List[str]] = []
        self.create_boards()

    def create_boards(self) -> None:
        for y in range(self.height):
            self.user_board.append(['.' for x in range(self.width)])
            self.hits_board.append(['.' for x in range(self.width)])
            self.cpu_board.append(['.' for x in range(self.width)])

        self.print_boards()

    def print_boards(self) -> None:
        print(heading(self.leaderboard.username))
        
        print(
            ' ' * self.width, 'Your Board',
            ' ' * (self.width * 3), 'CPU Board', '\n'
        )

        print(
            ' ' * 3, ''.join(f'{str(x):3s}' for x in range(self.width)),
            ' ' * 5,
            ' ' * 3, ''.join(f'{str(x):3s}' for x in range(self.width)),
        )

        for i, row in enumerate(zip(self.user_board, self.hits_board)):
            print(
                f'{str(i):3s}', ''.join(f'{y:3s}' for y in row[0]),
                ' ' * 5,
                f'{str(i):3s}', ''.join(f'{y:3s}' for y in row[1]),
            )

        print('\n')

    def create_ships(self):
        for i in range(self.ships):
            pass


class Colors:
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    ORANGE = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
